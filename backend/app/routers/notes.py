from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..database import get_db
from ..models import Note, User
from ..schemas import NoteCreate, NoteUpdate, NoteResponse
from ..core import get_current_user, get_current_user_optional

router = APIRouter(prefix="/notes", tags=["筆記"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """創建新筆記"""
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        file_type=note_data.file_type,
        is_public=note_data.is_public,
        user_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    # 添加owner_username
    response = NoteResponse.from_orm(new_note)
    response.owner_username = current_user.username
    return response

@router.get("/", response_model=List[NoteResponse])
def get_public_notes(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """獲取所有公開筆記"""
    notes = db.query(Note).filter(Note.is_public == True).order_by(Note.created_at.desc()).offset(skip).limit(limit).all()

    # 添加owner_username
    result = []
    for note in notes:
        note_response = NoteResponse.from_orm(note)
        note_response.owner_username = note.owner.username
        result.append(note_response)

    return result

@router.get("/my", response_model=List[NoteResponse])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """獲取當前用戶的所有筆記"""
    notes = db.query(Note).filter(Note.user_id == current_user.id).order_by(Note.created_at.desc()).all()

    result = []
    for note in notes:
        note_response = NoteResponse.from_orm(note)
        note_response.owner_username = current_user.username
        result.append(note_response)

    return result

@router.get("/search", response_model=List[NoteResponse])
def search_notes(
    q: str,
    scope: str = "public",
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """搜尋筆記

    Args:
        q: 搜尋關鍵字
        scope: 搜尋範圍 (public/my/all)
    """
    if not q or len(q.strip()) == 0:
        return []

    # 建立基礎查詢條件（標題或內容包含關鍵字）
    search_condition = or_(
        Note.title.ilike(f"%{q}%"),
        Note.content.ilike(f"%{q}%")
    )

    # 根據 scope 決定搜尋範圍
    if scope == "public":
        # 搜尋公開筆記
        notes = db.query(Note).filter(
            Note.is_public == True,
            search_condition
        ).order_by(Note.updated_at.desc()).limit(50).all()
    elif scope == "my":
        # 搜尋我的筆記（需要登入）
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="需要登入才能搜尋個人筆記"
            )
        notes = db.query(Note).filter(
            Note.user_id == current_user.id,
            search_condition
        ).order_by(Note.updated_at.desc()).limit(50).all()
    elif scope == "all":
        # 搜尋所有可見筆記（我的 + 公開）
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="需要登入才能使用全域搜尋"
            )
        notes = db.query(Note).filter(
            or_(
                Note.user_id == current_user.id,
                Note.is_public == True
            ),
            search_condition
        ).order_by(Note.updated_at.desc()).limit(50).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無效的搜尋範圍，請使用 public/my/all"
        )

    # 構建返回結果
    result = []
    for note in notes:
        note_response = NoteResponse.from_orm(note)
        note_response.owner_username = note.owner.username
        result.append(note_response)

    return result

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """獲取單個筆記"""
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="筆記不存在"
        )

    # 檢查筆記是否公開
    if not note.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此筆記為私密筆記"
        )

    note_response = NoteResponse.from_orm(note)
    note_response.owner_username = note.owner.username
    return note_response

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新筆記"""
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="筆記不存在"
        )

    # 檢查是否為筆記擁有者
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改此筆記"
        )

    # 更新筆記
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    if note_data.is_public is not None:
        note.is_public = note_data.is_public

    db.commit()
    db.refresh(note)

    note_response = NoteResponse.from_orm(note)
    note_response.owner_username = current_user.username
    return note_response

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """刪除筆記"""
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="筆記不存在"
        )

    # 檢查是否為筆記擁有者
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限刪除此筆記"
        )

    db.delete(note)
    db.commit()

    return None
