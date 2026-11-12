
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.resume import UserResume
from services.resume_parser import process_resume


router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume Parser"]
)


@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        filename = file.filename or ""

        file_extension = (
            "." + filename.rsplit(".", 1)[-1].lower()
            if "." in filename else ""
        )

        if file_extension not in [".pdf", ".docx"]:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are allowed"
            )

        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        if len(file_bytes) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File size must not exceed 5 MB"
            )

        result = process_resume(
            file_bytes,
            file_extension
        )

        resume_record = UserResume(
            original_filename=filename,
            file_type=file_extension,
            extracted_text=result["extracted_text"],
            extracted_data=result["extracted_data"]
        )

        db.add(resume_record)
        await db.commit()
        await db.refresh(resume_record)

        return {
            "message": "Resume parsed and saved successfully",
            "resume_id": resume_record.id,
            "filename": filename,
            "file_type": file_extension,
            "extracted_data": result["extracted_data"]
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to process and save resume"
        )

    finally:
        await file.close()