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
