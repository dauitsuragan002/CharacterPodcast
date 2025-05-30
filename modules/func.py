import os
import hashlib
import pygame
from tulgatts import TulgaTTS
from config import char_token, NAME_TO_VOICE_KEY

def get_voice_id(speaker_name: str) -> str | None:
    voice_key = NAME_TO_VOICE_KEY.get(speaker_name)
    if not voice_key:
        print(f"⚠️ No voice match found for '{speaker_name}'.")
        return None
    return voice_key

def synthesize_message_tulga(text: str, voice, folder: str = "audio") -> str | None:
    if not text.strip():
        return None

    filename = hashlib.md5(text.encode("utf-8")).hexdigest() + ".mp3"
    filepath = os.path.join(folder, filename)

    # Initialize Pygame mixer
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as e:
        print(f"❌ Pygame mixer initialization error: {e}")
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
            print(f"❌ Music playback error: {e}")
        return filepath

    # If file does not exist — generate
    if not char_token:
        print("❌ TulgaTTS API token is missing!")
        return None

    try:
        os.makedirs(folder, exist_ok=True)
        voice_id = get_voice_id(voice)
        print(f"🎤 Voice match: {voice_id}")
        if voice_id:
            tts_client = TulgaTTS(api_token=char_token, voice=voice_id)
            tts_client.say(text, output_file=filepath)
            print(f"🎧 Generation completed: {filepath}")
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            return filepath
    except Exception as e:
        print(f"⚠️ TTS error: {e}")
        return None