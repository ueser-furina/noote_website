from .auth import router as auth_router
from .notes import router as notes_router
from .collections import router as collections_router

__all__ = ["auth_router", "notes_router", "collections_router"]
