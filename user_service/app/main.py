import asyncio
from fastapi import FastAPI, Depends
import uvicorn
from database.database import engine
from api.routes import router
from sqladmin import Admin, ModelView
from database.models import User, Company, CompanyAdmin, Department, DepartmentAdmin

app = FastAPI()
admin = Admin(app, engine, base_url="/admin_ui")


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.role]


class CompanyAdminView(ModelView, model=Company):
    column_list = [Company.id, Company.name, Company.admin_id]


class DepartmentAdminView(ModelView, model=Department):
    column_list = [Department.id, Department.name,
                   Department.department_head_id, Department.description, Department.company_id]


class CompanyAdminAdmin(ModelView, model=CompanyAdmin):
    column_list = [CompanyAdmin.user_id, CompanyAdmin.company_id]


class DepartmentAdminAdmin(ModelView, model=DepartmentAdmin):
    column_list = [DepartmentAdmin.user_id, DepartmentAdmin.department_id]


admin.add_view(UserAdmin)
admin.add_view(CompanyAdminView)
admin.add_view(DepartmentAdminView)
admin.add_view(CompanyAdminAdmin)
admin.add_view(DepartmentAdminAdmin)

app.include_router(router)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
