from utils.analysis_utils import get_words_count_from_list_of_songs, \
    create_bar_chart_out_of_count_object, get_all_words_count_average_from_list_of_songs, \
    get_average_sentiment_subjectivity_from_list_of_songs, get_average_sentiment_polarity_from_list_of_songs
from utils.song_utils import get_songs_from_release_range
from config import STORAGE_PATH, WORDS_COUNT_CHART_SIZE, STORAGE_URL
from random import randint
from utils.gpt_utils import send_prompt


def handle_analysis(db, collection_name, start_year, end_year):
    try:
        list_of_songs = get_songs_from_release_range(db, collection_name, start_year, end_year)

        songs_quantity = len(list_of_songs)

        file_name = f"{STORAGE_PATH}analysis_{randint(10000,99999)}.png"

        words_count = get_words_count_from_list_of_songs(list_of_songs)
        word_chart_title = f"Top {WORDS_COUNT_CHART_SIZE} Words by Quantity"
        word_chart_y_axis_value = 'Word'
        create_bar_chart_out_of_count_object(word_chart_title, word_chart_y_axis_value, words_count,
                                             WORDS_COUNT_CHART_SIZE, file_name)

        top_30_words = ', '.join(list(words_count.keys())[:30])

        word_count_average = get_all_words_count_average_from_list_of_songs(list_of_songs)

        average_subjectivity = get_average_sentiment_subjectivity_from_list_of_songs(list_of_songs)
        average_polarity = get_average_sentiment_polarity_from_list_of_songs(list_of_songs)
        task_result = {
            "message": f"Results from period {start_year} - {end_year}. Based on data from {songs_quantity} songs:\n"
                       f"Average word count: {word_count_average}\n"
                       f"Average subjectivity: {average_subjectivity}\n"
                       f"Average polarity: {average_polarity}\n"
                       f"Top 30 words: {top_30_words}\n",
            "imageUrl": f"{STORAGE_URL + file_name}"
            }

    except Exception as e:
        task_result = f"Failed to create analysis. Problem occured: {e}"

    return task_result


def handle_text_generation(decade, model):
    if decade in ["00s", "10s", "20s"]:
        year = "20" + decade
    else:
        year = "19" + decade
    prompt = f"Can you generate a love songs lyric - {year} style?"
    task_result = send_prompt(prompt, model)
    return task_result