
from fastapi import FastAPI
from sqlalchemy import text

from database import engine
from routers.resume import router as resume_router
from routers.auth import router as auth_router
from routers.profile import router as profile_router
from routers.dashboard import router as dashboard_router


app = FastAPI(
    title="AI Resume Parser & 2FA",
    description="Secure Student Registration System",
    version="1.0.0"
)

app.include_router(resume_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    return {
        "message": "AI Resume Parser & 2FA API is running",
        "status": "success"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health/database")
async def database_health():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))

            tables = result.scalars().all()

        return {
            "database": "connected",
            "tables": tables,
            "required_tables_created": all(
                table in tables
                for table in [
                    "users",
                    "user_resumes",
                    "otp_challenges"
                ]
            )
        }

    except Exception:
        return {
            "database": "disconnected"
        }