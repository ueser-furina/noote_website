from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import Collection, CollectionNote, Note, User
from ..schemas import (
    CollectionCreate, CollectionUpdate, CollectionResponse,
    CollectionNoteAdd, CollectionNoteReorder, NoteResponse,
    CollectionIntegrationRequest, CollectionIntegrationResponse
)
from ..core import get_current_user, get_current_user_optional
from ..services.ai_integration import ai_service

router = APIRouter(prefix="/collections", tags=["合集"])

@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def create_collection(
    collection_data: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """創建新合集"""
    new_collection = Collection(
        name=collection_data.name,
        description=collection_data.description,
        is_public=collection_data.is_public,
        user_id=current_user.id
    )

    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)

    response = CollectionResponse.from_orm(new_collection)
    response.owner_username = current_user.username
    response.note_count = 0
    return response

@router.get("/", response_model=List[CollectionResponse])
def get_public_collections(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """獲取所有公開合集"""
    collections = db.query(Collection).filter(
        Collection.is_public == True
    ).order_by(Collection.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for collection in collections:
        collection_response = CollectionResponse.from_orm(collection)
        collection_response.owner_username = collection.owner.username
        # 計算筆記數量
        collection_response.note_count = db.query(CollectionNote).filter(
            CollectionNote.collection_id == collection.id
        ).count()
        result.append(collection_response)

    return result

@router.get("/my", response_model=List[CollectionResponse])
def get_my_collections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """獲取當前用戶的所有合集"""
    collections = db.query(Collection).filter(
        Collection.user_id == current_user.id
    ).order_by(Collection.created_at.desc()).all()

    result = []
    for collection in collections:
        collection_response = CollectionResponse.from_orm(collection)
        collection_response.owner_username = current_user.username
        # 計算筆記數量
        collection_response.note_count = db.query(CollectionNote).filter(
            CollectionNote.collection_id == collection.id
        ).count()
        result.append(collection_response)

    return result

@router.get("/{collection_id}", response_model=CollectionResponse)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """獲取單個合集"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查權限
    if not collection.is_public:
        if not current_user or collection.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="此合集為私密合集"
            )

    collection_response = CollectionResponse.from_orm(collection)
    collection_response.owner_username = collection.owner.username
    # 計算筆記數量
    collection_response.note_count = db.query(CollectionNote).filter(
        CollectionNote.collection_id == collection.id
    ).count()

    return collection_response

@router.put("/{collection_id}", response_model=CollectionResponse)
def update_collection(
    collection_id: int,
    collection_data: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新合集"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查是否為合集擁有者
    if collection.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改此合集"
        )

    # 更新合集
    if collection_data.name is not None:
        collection.name = collection_data.name
    if collection_data.description is not None:
        collection.description = collection_data.description
    if collection_data.cover_image is not None:
        collection.cover_image = collection_data.cover_image
    if collection_data.is_public is not None:
        collection.is_public = collection_data.is_public

    db.commit()
    db.refresh(collection)

    collection_response = CollectionResponse.from_orm(collection)
    collection_response.owner_username = current_user.username
    collection_response.note_count = db.query(CollectionNote).filter(
        CollectionNote.collection_id == collection.id
    ).count()

    return collection_response

@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """刪除合集"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查是否為合集擁有者
    if collection.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限刪除此合集"
        )

    db.delete(collection)
    db.commit()

    return None

@router.get("/{collection_id}/notes", response_model=List[NoteResponse])
def get_collection_notes(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """獲取合集內的所有筆記"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查權限
    if not collection.is_public:
        if not current_user or collection.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="此合集為私密合集"
            )

    # 獲取合集中的筆記（按 position 排序）
    collection_notes = db.query(CollectionNote).filter(
        CollectionNote.collection_id == collection_id
    ).order_by(CollectionNote.position).all()

    result = []
    for cn in collection_notes:
        note = cn.note
        # 如果是公開合集，只顯示公開筆記
        if not collection.is_public or note.is_public or (current_user and note.user_id == current_user.id):
            note_response = NoteResponse.from_orm(note)
            note_response.owner_username = note.owner.username
            result.append(note_response)

    return result

@router.post("/{collection_id}/notes", status_code=status.HTTP_201_CREATED)
def add_note_to_collection(
    collection_id: int,
    note_data: CollectionNoteAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加筆記到合集"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查是否為合集擁有者
    if collection.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能添加筆記到自己的合集"
        )

    # 檢查筆記是否存在
    note = db.query(Note).filter(Note.id == note_data.note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="筆記不存在"
        )

    # 檢查筆記是否已在合集中
    existing = db.query(CollectionNote).filter(
        CollectionNote.collection_id == collection_id,
        CollectionNote.note_id == note_data.note_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="筆記已在合集中"
        )

    # 獲取當前最大 position
    max_position = db.query(func.max(CollectionNote.position)).filter(
        CollectionNote.collection_id == collection_id
    ).scalar() or -1

    # 添加筆記到合集
    collection_note = CollectionNote(
        collection_id=collection_id,
        note_id=note_data.note_id,
        position=max_position + 1
    )

    db.add(collection_note)
    db.commit()

    return {"message": "筆記已添加到合集"}

@router.delete("/{collection_id}/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_note_from_collection(
    collection_id: int,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """從合集移除筆記"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查是否為合集擁有者
    if collection.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能從自己的合集移除筆記"
        )

    # 查找關聯記錄
    collection_note = db.query(CollectionNote).filter(
        CollectionNote.collection_id == collection_id,
        CollectionNote.note_id == note_id
    ).first()

    if not collection_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="筆記不在此合集中"
        )

    db.delete(collection_note)
    db.commit()

    return None

@router.put("/{collection_id}/notes/reorder", status_code=status.HTTP_200_OK)
def reorder_collection_notes(
    collection_id: int,
    reorder_data: CollectionNoteReorder,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """重新排序合集中的筆記"""
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查是否為合集擁有者
    if collection.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能排序自己的合集"
        )

    # 更新每個筆記的 position
    for index, note_id in enumerate(reorder_data.note_ids):
        collection_note = db.query(CollectionNote).filter(
            CollectionNote.collection_id == collection_id,
            CollectionNote.note_id == note_id
        ).first()

        if collection_note:
            collection_note.position = index

    db.commit()

    return {"message": "排序已更新"}

@router.post("/{collection_id}/integrate", response_model=CollectionIntegrationResponse)
def integrate_collection_notes(
    collection_id: int,
    request_data: CollectionIntegrationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """使用 AI 整合合集中的所有筆記

    將合集中的多個筆記內容送給 AI 進行整合，生成一份統整後的完整筆記。

    Args:
        collection_id: 合集 ID
        request_data: 包含可選的自訂提示詞
        db: 資料庫 session
        current_user: 當前用戶（可選，用於存取私密合集）

    Returns:
        整合後的筆記內容及相關資訊
    """
    # 檢查合集是否存在
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合集不存在"
        )

    # 檢查權限（私密合集需要是擁有者）
    if not collection.is_public:
        if not current_user or collection.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="此合集為私密合集，無法存取"
            )

    # 獲取合集中的所有筆記（按 position 排序）
    collection_notes = db.query(CollectionNote).filter(
        CollectionNote.collection_id == collection_id
    ).order_by(CollectionNote.position).all()

    if not collection_notes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="合集中沒有筆記，無法進行整合"
        )

    # 準備筆記資料
    notes_data = []
    for cn in collection_notes:
        note = cn.note
        # 如果是公開合集，只處理公開筆記或自己的筆記
        if collection.is_public and not note.is_public:
            if not current_user or note.user_id != current_user.id:
                continue

        notes_data.append({
            "title": note.title,
            "content": note.content
        })

    if not notes_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="合集中沒有可用的筆記進行整合"
        )

    # 呼叫 AI 服務進行整合（使用前端傳入的 API key）
    try:
        from ..services.ai_integration import AIIntegrationService

        # 使用前端傳入的 API key 建立服務實例
        ai_integration_service = AIIntegrationService(api_key=request_data.api_key)

        integrated_content = ai_integration_service.integrate_notes(
            notes_data=notes_data,
            integration_prompt=request_data.custom_prompt
        )

        return CollectionIntegrationResponse(
            integrated_content=integrated_content,
            note_count=len(notes_data),
            created_at=datetime.utcnow()
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
