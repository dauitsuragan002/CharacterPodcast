import streamlit as st

st.set_page_config(
    page_title="Tulga Podcast",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import asyncio
import os
import datetime
import time
import json
from threading import Thread
from app import CHAR_ID, create_podcast
from modules.func import synthesize_message_tulga
from config import get_message, CHAR_ID

# Language switcher
lang = st.sidebar.selectbox(
    "Тілді таңдаңыз / Select language",
    ["kk", "en"],
    format_func=lambda x: "Қазақша" if x == "kk" else "English"
)

TEMP_FILE = "temp_podcast.json"
HISTORY_FILE = "podcast_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def init_session_state():
    if 'podcast_history' not in st.session_state:
        st.session_state.podcast_history = []
    if 'all_podcasts' not in st.session_state:
        st.session_state.all_podcasts = load_history()
    if 'is_podcast_running' not in st.session_state:
        st.session_state.is_podcast_running = False
    if 'current_podcast_info' not in st.session_state:
        st.session_state.current_podcast_info = None
    if 'settings_expanded' not in st.session_state:
        st.session_state.settings_expanded = True
    if 'show_chat_view' not in st.session_state:
        st.session_state.show_chat_view = False
    if 'current_chars' not in st.session_state:
        st.session_state.current_chars = {'char1': None, 'char2': None}

async def run_podcast_async(char1_name, char2_name, topic, exchanges):
    try:
        podcast, session_id = await create_podcast(char1_name, char2_name, topic, exchanges)
        if podcast and session_id:
            podcast_info = {
                "session_id": session_id,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "char1": char1_name,
                "char2": char2_name,
                "topic": topic,
                "exchanges": exchanges,
                "conversation": podcast,
                "completed": True
            }
            with open(TEMP_FILE, 'w', encoding='utf-8') as f:
                json.dump(podcast_info, f, ensure_ascii=False)
        return podcast, session_id
    except Exception as e:
        error_info = {"error": str(e), "completed": True}
        with open(TEMP_FILE, 'w', encoding='utf-8') as f:
            json.dump(error_info, f, ensure_ascii=False)
        return None, None

def run_podcast_thread(char1_name, char2_name, topic, exchanges):
    async def run():
        try:
            await run_podcast_async(char1_name, char2_name, topic, exchanges)
        except Exception as e:
            error_info = {"error": str(e), "completed": True}
            with open(TEMP_FILE, 'w', encoding='utf-8') as f:
                json.dump(error_info, f, ensure_ascii=False)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(run())
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
            try:
                loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass
    finally:
        try:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
        except Exception:
            pass

def start_podcast(char1_name, char2_name, topic, exchanges):
    st.session_state.podcast_history = []
    st.session_state.is_podcast_running = True
    st.session_state.show_chat_view = True
    st.session_state.current_chars = {'char1': char1_name, 'char2': char2_name}
    st.session_state.selected_podcast = None
    try:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
    except Exception:
        pass
    thread = Thread(target=run_podcast_thread, args=(char1_name, char2_name, topic, exchanges))
    thread.daemon = True
    thread.start()

def show_podcast_messages(messages, char1_name=None, char2_name=None):
    if not messages:
        return
    
    for i, entry in enumerate(messages):
        speaker = entry["speaker"]
        message = entry["message"]
        time.sleep(0.1) if st.session_state.is_podcast_running else None
        if speaker == "Host":
            role = "assistant"
            avatar = "🎙️"
        elif speaker == char1_name:
            role = "user"
            avatar = "🤖"
        elif speaker == char2_name:
            role = "assistant"
            avatar = "🤖"
        else:
            role = "assistant"
            avatar = "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(f"**{speaker}**\n\n{message}")
        if speaker == char1_name and st.button("🔊", key=f"tts_btn_{i}_char1"):
            synthesize_message_tulga(message, voice=char1_name)
        elif speaker == char2_name and st.button("🔊", key=f"tts_btn_{i}_char2"):
            synthesize_message_tulga(message, voice=char2_name)

def show_new_podcast_page():
    st.title(get_message("main_title", lang))
    if not st.session_state.show_chat_view:
        with st.expander("⚙️ " + get_message("generate_button", lang), expanded=st.session_state.settings_expanded):
            col1, col2 = st.columns(2)
            with col1:
                char1_name = st.selectbox(
                    get_message("select_character_1", lang),
                    options=["-"] + [name for name in CHAR_ID.keys() if not name.startswith('#')],
                    key="char1"
                )
                if char1_name == "-":
                    char1_name = None
            with col2:
                char2_name = st.selectbox(
                    get_message("select_character_2", lang),
                    options=["-"] + [name for name in CHAR_ID.keys() if not name.startswith('#')],
                    key="char2"
                )
                if char2_name == "-":
                    char2_name = None
            topic = st.text_input(get_message("enter_topic", lang)) 
            exchanges = st.number_input(get_message("exchanges", lang), min_value=1, max_value=10, value=3)
            start_disabled = (
                st.session_state.is_podcast_running or
                not char1_name or not char2_name or char1_name == char2_name or not topic
            )
            if st.button("🎙️ " + get_message("generate_button", lang), disabled=start_disabled):
                start_podcast(char1_name, char2_name, topic, exchanges)
                st.rerun()

    if st.session_state.show_chat_view or st.session_state.is_podcast_running:
        if st.session_state.is_podcast_running:
            st.info(f"🎙️ {get_message('generation_completed', lang, '')} {st.session_state.current_chars['char1']} {get_message('and', lang) if 'and' in get_message.__globals__['MESSAGES'] else 'and'} {st.session_state.current_chars['char2']}")
            time.sleep(2)
            st.rerun()
        if st.session_state.podcast_history:
            show_podcast_messages(
                st.session_state.podcast_history,
                st.session_state.current_chars['char1'],
                st.session_state.current_chars['char2']
            )
            if not st.session_state.is_podcast_running:
                if st.button("🎙️ " + get_message("generate_button", lang), key="new_podcast_after_completion"):
                    st.session_state.show_chat_view = False
                    st.session_state.settings_expanded = True
                    st.session_state.podcast_history = []
                    st.rerun()

def main():
    init_session_state()
    if os.path.exists(TEMP_FILE):
        try:
            with open(TEMP_FILE, 'r', encoding='utf-8') as f:
                result = json.load(f)
            if result.get("completed", False):
                if "error" in result:
                    st.error(get_message("tts_error", lang, result['error']))
                    st.session_state.is_podcast_running = False
                    st.session_state.show_chat_view = False
                else:
                    history = st.session_state.all_podcasts
                    existing = any(p.get("session_id") == result.get("session_id") for p in history)
                    if not existing:
                        history.insert(0, result)
                        save_history(history)
                        st.session_state.all_podcasts = history
                    st.session_state.podcast_history = result["conversation"]
                    st.session_state.is_podcast_running = False
                    st.success(get_message("generation_completed", lang, ""))
                os.remove(TEMP_FILE)
                st.rerun()
        except Exception as e:
            st.error(get_message("tts_error", lang, str(e)))
            st.session_state.is_podcast_running = False

    with st.sidebar:
        if st.button("➕ " + get_message("generate_button", lang), key="new_chat_btn"):
            st.session_state.selected_podcast = None
            st.session_state.show_chat_view = False
            st.session_state.settings_expanded = True
            st.rerun()
        st.markdown("---")
        if not st.session_state.all_podcasts:
            st.info("📭 " + get_message("no_history", lang))
        else:
            for idx, podcast in enumerate(st.session_state.all_podcasts):
                topic = podcast.get('topic', get_message("enter_topic", lang))
                if st.button(topic, key=f"sidebar_podcast_{idx}"):
                    st.session_state.podcast_history = podcast["conversation"]
                    st.session_state.current_chars = {"char1": podcast["char1"], "char2": podcast["char2"]}
                    st.session_state.show_chat_view = True
                    st.rerun()
    show_new_podcast_page()

if __name__ == "__main__":
    main()
