from fastapi import APIRouter
from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .task_routes import router as task_router
from .news_routes import router as news_router
from .meet_routes import router as meet_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/user", tags=["Users"])
router.include_router(task_router, prefix="/tasks", tags=["Tasks"])
router.include_router(news_router, prefix="/news", tags=["News"])
router.include_router(meet_router, prefix="/meet", tags=["Meetings"])
