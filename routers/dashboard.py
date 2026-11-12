
from fastapi import APIRouter, Depends

from routers.profile import get_current_user
from models.user import User


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/student")
async def student_dashboard(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Welcome to Student Dashboard",
        "dashboard": "/dashboard/student",
        "student": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email
        },
        "status": "success"
    }