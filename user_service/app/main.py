import asyncio
from fastapi import FastAPI, Depends
import uvicorn
from database.database import engine
from api.routes import router
from sqladmin import Admin, ModelView
from database.models import User, Company, Department, News
import os
from dotenv import load_dotenv

load_dotenv()

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
