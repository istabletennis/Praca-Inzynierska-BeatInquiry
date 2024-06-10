from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from models import User, AnalysisData, LyricsRequestData, SongToSave
from db import get_database
from auth import create_access_token, verify_password, get_password_hash, decode_access_token
from fastapi.middleware.cors import CORSMiddleware
from handlers import handle_analysis, handle_text_generation
from config import MONGO_USERS_COLLECTION_NAME
from utils.song_utils import add_song_to_collection, decade_to_release, model_and_decade_to_song_name, model_to_artist, \
    model_to_collection
import logging
import sys

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:3000",
    "http://localhost:5175",
]

app.mount("/static", StaticFiles(directory="./static"), name="static")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('API is starting up')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.post("/register")
async def register(user: User, db=Depends(get_database)):
    existing_user = db[MONGO_USERS_COLLECTION_NAME].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    result = db[MONGO_USERS_COLLECTION_NAME].insert_one(user_dict)
    return {"username": user.username, "id": str(result.inserted_id)}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = db[MONGO_USERS_COLLECTION_NAME].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.options("/token")
async def options_token(response: Response):
    response.headers["Allow"] = "POST, OPTIONS"
    return response


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    username = payload.get("sub")
    return {"username": username}


@app.post("/perform-analysis")
async def perform_analysis(data: AnalysisData, db=Depends(get_database)):
    logger.info(f"Generating analysis from period {data.start_year} - {data.end_year} "
                f"using collection: {data.collection_name}")
    response = handle_analysis(
        db=db,
        collection_name=data.collection_name,
        start_year=data.start_year,
        end_year=data.end_year)
    logger.info(response)
    return response


@app.post("/lyrics")
async def send_lyrics_request_to_chat(lyrics_request: LyricsRequestData):
    response = handle_text_generation(
        decade=lyrics_request.decade,
        model=lyrics_request.model
    )
    logger.info(response)
    return response


@app.put("/save-lyrics")
async def save_lyrics(song_to_save: SongToSave, db=Depends(get_database)):

    response = add_song_to_collection(
        db=db,
        collection_name=model_to_collection(song_to_save.model),
        song_name=model_and_decade_to_song_name(song_to_save.model, song_to_save.decade),
        artist_name=model_to_artist(song_to_save.model),
        spotify_release_year=decade_to_release(song_to_save.decade),
        lyrics_text=song_to_save.lyrics
    )
    logger.info(response)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
