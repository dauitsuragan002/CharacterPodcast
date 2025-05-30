# Tulga Podcast

This project is a Streamlit web application for automatically creating a podcast between two characters. The project generates character dialogues using the [PyCharacterAI](https://github.com/GRVYDEV/PyCharacterAI) library and converts text to speech using [TulgaTTS](https://github.com/dauitsuragan002/tulga-tts).

## Technologies Used

- **PyCharacterAI** — for generating AI character dialogues.
- **TulgaTTS** — for text-to-speech (TTS) conversion.
- **Streamlit** — for building the web interface.

## Installation

1. Clone the repository:
    ```sh
    git clone <repo-url>
    cd <repo-folder>
    ```

2. Install the required dependencies:
    ```sh
    pip install -r tulga-tts PyCharacterAI streamlit
    ```

3. Add your TulgaTTS API token to the `.env` file:
    ```
    1.  **Obtain your token:**
    *   ⚠️ **DO NOT SHARE YOUR TOKEN!** It is required to send requests from your account.
    *   Open link https://character.ai/chat/2WPyJRflV_4nTx6_-tuNrhkiiqhDyOsn9O25BR1sDO8
    *   Open **Developer Tools** in your browser (usually F12).
    *   Go to the **Network** tab.
    *   Refresh the page or send a message to any character.
    *   In the list of network requests, click on any request (for example, to `/settings`).
    ![How to find the Authorization Token](https://github.com/dauitsuragan002/tulgatts/raw/main/img/asset.jpg)
    *   Go to the **Headers** section.
    *   Find the **Authorization** header. It will look like:
        ```
        Authorization: Token <your_token_here>
        ```
    *   Copy only the token part (after `Token `).
    *   Set the `CHARACTER_AI_TOKEN` environment variable or create a `.env` file in the project root and add `CHAR_TOKEN=CHARACTER_AI_TOKEN`.
    
    ```

## Usage

To launch the web application:

```sh
streamlit run tulga_podcast_updated.py
```

## Features

- Select characters and enter a podcast topic
- Automatically generate character dialogues
- Listen to each message via voice
- Save and view podcast history

## Folders and Files

- `app.py` — logic for generating podcast dialogues
- `tulga_podcast_updated.py`, `podcast_web.py` — Streamlit web interfaces
- `modules/func.py` — TTS and audio playback functions
- `config.py` — configuration and character list
- `audio/` — generated audio files
- `podcast_history.json` — podcast history

## Authors

- [PyCharacterAI](https://github.com/GRVYDEV/PyCharacterAI)
- [TulgaTTS](https://github.com/dauitsuragan002/tulga-tts)