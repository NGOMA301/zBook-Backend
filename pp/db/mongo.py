# app/db/mongo.py
import motor.motor_asyncio
from app.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
db = client.book_summarizer
