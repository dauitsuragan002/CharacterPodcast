import os
import hashlib
import pygame
from tulgatts import TulgaTTS
from config import char_token, NAME_TO_VOICE_KEY, get_message

def get_voice_id(speaker_name: str, lang: str = "en") -> str | None:
    voice_key = NAME_TO_VOICE_KEY.get(speaker_name)
    if not voice_key:
        print(get_message("no_voice", lang, speaker_name))
        return None
    return voice_key

def synthesize_message_tulga(text: str, voice, folder: str = "audio", lang: str = "en") -> str | None:
    if not text.strip():
        return None

    filename = hashlib.md5(text.encode("utf-8")).hexdigest() + ".mp3"
    filepath = os.path.join(folder, filename)

    # Initialize Pygame mixer
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as e:
        print(get_message("pygame_init_error", lang, e))
        return None

    # If file already exists
    if os.path.exists(filepath):
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
        except pygame.error as e:
            print(get_message("music_playback_error", lang, e))
        return filepath

    # If file does not exist — generate
    if not char_token:
        print(get_message("token_missing", lang))
        return None

    try:
        os.makedirs(folder, exist_ok=True)
        voice_id = get_voice_id(voice, lang)
        print(get_message("voice_match", lang, voice_id))
        if voice_id:
            tts_client = TulgaTTS(api_token=char_token, voice=voice_id)
            tts_client.say(text, output_file=filepath)
            print(get_message("generation_completed", lang, filepath))
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            return filepath
    except Exception as e:
        print(get_message("tts_error", lang, e))
        return None