import asyncio
from fastapi import FastAPI, Depends, APIRouter
import uvicorn
from database.database import engine
from api.auth_routes import router as auth_router
from api.user_routes import router as user_router
from api.task_routes import router as task_router
from api.news_routes import router as news_router
from api.meet_routes import router as meet_router
from sqladmin import Admin, ModelView
from database.models import User, Company, Department, News
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
router.include_router(auth_router, tags=["Auth"])
router.include_router(user_router, tags=["Users"])
router.include_router(task_router, tags=["Tasks"])
router.include_router(news_router, tags=["News"])
router.include_router(meet_router, tags=["Meetings"])
ADMIN = os.environ.get('ADMIN_URL')
app = FastAPI()
admin = Admin(app, engine, base_url=f"/{ADMIN}")


class UserAdmin(ModelView, model=User):
    column_list = ["id", "email", "full_name", "role", "company", "manager", "department"]
    form_columns = ["email", "hashed_password", "full_name", "role", "company", "manager", "department"]


class CompanyAdminView(ModelView, model=Company):
    column_list = ["id", "name", "admin"]
    form_columns = ["name", "admin"]


class DepartmentAdminView(ModelView, model=Department):
    column_list = ["id", "name", "description", "company", "department_head"]
    form_columns = ["name", "description", "company", "department_head"]


class NewsAdmin(ModelView, model=News):
    column_list = ["id", "head", "description", "date_create"]
    form_columns = ["head", "description", "date_create"]


admin.add_view(UserAdmin)
admin.add_view(CompanyAdminView)
admin.add_view(DepartmentAdminView)
admin.add_view(NewsAdmin)

app.include_router(router)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
