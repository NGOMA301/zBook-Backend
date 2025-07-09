# app/api/v1/routes/summarize.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.file_reader import extract_text
from app.core.config import settings
from app.services.summarizer import summarize_with_openrouter
from app.auth.auth_handler import get_current_user
from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
import traceback

router = APIRouter()

@router.post("/")
async def summarize_book(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        text = await extract_text(file)
        if len(text.strip()) < 100:
            raise HTTPException(status_code=400, detail="Text content too small")

        result = await summarize_with_openrouter(text)

        summary_doc = {
            "user_id": ObjectId(user["user_id"]),
            "summary": result["summary"],
            "key_points": result["key_points"],
            "word_count": len(text.split()),
            "file_type": ext,
            "created_at": datetime.utcnow()
        }

        insert_result = await db.summaries.insert_one(summary_doc)

        # Convert ObjectId and datetime to serializable values
        return {
            "id": str(insert_result.inserted_id),
            "user_id": str(summary_doc["user_id"]),
            "summary": summary_doc["summary"],
            "key_points": summary_doc["key_points"],
            "word_count": summary_doc["word_count"],
            "file_type": summary_doc["file_type"],
            "created_at": summary_doc["created_at"].isoformat()
        }

    except Exception as e:
        print("🔥 ERROR OCCURRED 🔥")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summaries")
async def get_user_summaries(user=Depends(get_current_user)):
    cursor = db.summaries.find({"user_id": ObjectId(user["user_id"])}).sort("created_at", -1)
    results = []

    async for doc in cursor:
        results.append({
            "id": str(doc["_id"]),
            "summary": doc["summary"],
            "key_points": doc["key_points"],
            "file_type": doc.get("file_type"),
            "word_count": doc.get("word_count"),
            "created_at": doc["created_at"].isoformat() if "created_at" in doc else None,
            "user_id": str(doc["user_id"]) if "user_id" in doc else None
        })

    return results
