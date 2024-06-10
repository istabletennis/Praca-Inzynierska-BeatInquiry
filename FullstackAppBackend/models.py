from pydantic import BaseModel
from typing import Optional
from config import MONGO_SONGS_COLLECTION_NAME_REAL_SONGS


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str


class UserLogin(BaseModel):
    username: str
    password: str


class AnalysisData(BaseModel):
    start_year: int
    end_year: int
    collection_name: Optional[str] = MONGO_SONGS_COLLECTION_NAME_REAL_SONGS


class LyricsRequestData(BaseModel):
    decade: str
    model: Optional[str] = 'gpt-4'


class SongToSave(BaseModel):
    lyrics: str
    model: str
    decade: str

