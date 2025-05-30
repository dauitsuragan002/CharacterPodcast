import os
import logging

from dotenv import load_dotenv
from PyCharacterAI import Client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("podcast")

load_dotenv()

char_token = os.getenv("char_token")
client = Client()

CHAR_ID = {
    'Н.Назарбаев': 'oUp5SyQp59iHies_Zsl6GIWAhYeOqCSHDQ-KEsL39iA',
    'Қ.Тоқаев': '5gTJSsRjrVpTdEFgQWobgtEJCCl2entlnz1K3APxfOw',
    'П.Дуров': 'f3y4oEjD48xm8qv_cExTHQS72BmHUZq_MRdxdSJhjZ4',
    'Нұрлан Сабуров': 'JU4TqYz_kXilMNLDFMJa8PdMebdmLm6mvxcZH3UJCHQ',
    'В.Путин': 'KO8L-Xvs40hFyfJ_2d4KZeHUPRRYmoJp7rcE3Dsmps4',
    'Скриптонит': 'iTPvqeMQSDoVBxPsXXHR_SsgYisPFzJDxhyWstECCBA',
    'Илон Маск': '6HhWfeDjetnxESEcThlBQtEUo0O8YHcXyHqCgN7b2hY',
    'Альберт Эйнштейн': '6zjXBKxqcTOiFODhflrtmk3VJANGp3L_szVkS43oo48',
}

NAME_TO_VOICE_KEY = {
    'Қ.Тоқаев': 'Tokaev',
    'Н.Назарбаев': 'Nursultan Nazarbaev',
    'П.Дуров': 'Pavel Durov',
    'Нұрлан Сабуров': 'Nurlan Saburov',
    'В.Путин': 'Putin',
    'Скриптонит': 'Skriptonit',
    'Илон Маск': 'Elon Musk',
    'Альберт Эйнштейн': 'Albert E',
}

# Localization messages
MESSAGES = {
    "no_voice": {
        "en": "⚠️ No voice match found for '{}'.",
        "kk": "⚠️ '{}' үшін дауыс сәйкестігі табылмады."
    },
    "pygame_init_error": {
        "en": "❌ Pygame mixer initialization error: {}",
        "kk": "❌ Pygame mixer инициализация қатесі: {}"
    },
    "music_playback_error": {
        "en": "❌ Music playback error: {}",
        "kk": "❌ Музыканы ойнату қатесі: {}"
    },
    "token_missing": {
        "en": "❌ TulgaTTS API token is missing!",
        "kk": "❌ TulgaTTS API токен жоқ!"
    },
    "voice_match": {
        "en": "🎤 Voice match: {}",
        "kk": "🎤 Дауыс сәйкестігі: {}"
    },
    "generation_completed": {
        "en": "🎧 Generation completed: {}",
        "kk": "🎧 Генерация аяқталды: {}"
    },
    "tts_error": {
        "en": "⚠️ TTS error: {}",
        "kk": "⚠️ TTS қатесі: {}"
    },
    "main_title": {
        "en": "CharacterPodcast",
        "kk": "Тұлға Подкаст"
    },
    "select_character_1": {
        "en": "Select the first character",
        "kk": "Бірінші кейіпкерді таңдаңыз"
    },
    "select_character_2": {
        "en": "Select the second character",
        "kk": "Екінші кейіпкерді таңдаңыз"
    },
    "enter_topic": {
        "en": "Enter podcast topic",
        "kk": "Подкаст тақырыбын енгізіңіз"
    },
    "generate_button": {
        "en": "Generate Podcast",
        "kk": "Подкаст құру"
    },
    "history_button": {
        "en": "Show Podcast History",
        "kk": "Подкаст тарихын көрсету"
    },
    "play_audio": {
        "en": "Play Audio",
        "kk": "Аудионы ойнату"
    },
    "podcast_start": {
        "en": "Starting podcast between {} and {}",
        "kk": "{} және {} арасында подкаст басталды"
    },
    "char_not_found": {
        "en": "One or both characters not found in CHAR_ID dictionary",
        "kk": "CHAR_ID сөздігінде кейіпкерлер табылмады"
    },
    "podcast_completed": {
        "en": "Podcast completed with {} messages",
        "kk": "Подкаст {} хабарламамен аяқталды"
    },
    "empty_topic_warning": {
        "en": "Please enter a podcast topic.",
        "kk": "Подкаст тақырыбын енгізіңіз."
    },
    "same_character_warning": {
        "en": "Please select different characters.",
        "kk": "Әр түрлі кейіпкерлерді таңдаңыз."
    },
    "history_title": {
        "en": "Podcast History",
        "kk": "Подкаст тарихы"
    },
    "no_history": {
        "en": "No podcast history found.",
        "kk": "Подкаст тарихы жоқ."
    },
    "exchanges": {
        "en": "Exchanges",
        "kk": "Алмасулар саны"
    }
}

def get_message(key, lang, *args):
    msg = MESSAGES.get(key, {}).get(lang, "")
    return msg.format(*args)
