from random import randint
from config import MONGO_SONGS_COLLECTION_NAME_GPT4, \
    MONGO_SONGS_COLLECTION_NAME_GPT35, MONGO_SONGS_COLLECTION_NAME_BIV2


def get_songs_from_release_range(db, collection_name, lower_range: int, upper_range: int) -> list[dict]:
    result = []
    for song in db[collection_name].find(
            ({"$and": [{"spotify_release": {"$gte": lower_range}}, {"spotify_release": {"$lt": upper_range}}]})):
        result.append(song)
    return result


def get_first_song_with_title(db, collection_name, song_title) -> list[dict]:
    return db[collection_name].find_one({"name": song_title})


def prepare_song_lyrics(lyrics) -> dict:
    return lyrics.replace(r"\u2018", "'").replace(r"\u2019", "'").replace(r"\n", " ")


def add_song_to_collection(db, collection_name, song_name, artist_name, spotify_release_year, lyrics_text):
    song_object = {
        "name": song_name,
        "artist": artist_name,
        "spotify_release": spotify_release_year,
        "lyrics": lyrics_text
    }

    result = {
        "message": f"Added document id: {str(db[collection_name].insert_one(song_object).inserted_id)}, "
                   f"song name: {song_name}"}

    return result


def decade_to_release(decade: str) -> int:
    if decade in ["00s", "10s", "20s"]:
        release = ("20" + decade)[:-1]
    else:
        release = ("19" + decade)[:-1]
    return int(release)


def model_and_decade_to_song_name(model, decade):
    model_to_name_mapper = {
        "ft:gpt-3.5-turbo-0125:personal:bi-0125-v2:9MLSGTSp": "BeatInquiry",
        "gpt-4": "GPT4",
        "gpt-3.5-turbo": "gpt3-5"
    }

    song_id = str(randint(1000, 9999))

    song_name = f"{model_to_name_mapper.get(model, 'GPT')}-{decade[:-1]}-v{song_id}"

    return song_name


def model_to_artist(model):
    model_to_artist_mapper = {
        "ft:gpt-3.5-turbo-0125:personal:bi-0125-v2:9MLSGTSp": "BeatInquiry",
        "gpt-4": "CHATGPT4 PLUS",
        "gpt-3.5-turbo": "CHATGPT3.5 PLUS"
    }

    return model_to_artist_mapper.get(model, "AI")


def model_to_collection(model):
    model_to_collection_mapper = {
        "ft:gpt-3.5-turbo-0125:personal:bi-0125-v2:9MLSGTSp": MONGO_SONGS_COLLECTION_NAME_BIV2,
        "gpt-4": MONGO_SONGS_COLLECTION_NAME_GPT4,
        "gpt-3.5-turbo": MONGO_SONGS_COLLECTION_NAME_GPT35
    }

    return model_to_collection_mapper.get(model, MONGO_SONGS_COLLECTION_NAME_BIV2)
