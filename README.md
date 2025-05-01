# Star Wars Radio Blast Generator

This project generates immersive, Star Wars–themed "radio broadcast" audio segments based on live game state data. It transforms mission logs and faction updates into entertaining, in-universe radio news, complete with character voice, sound effects, and dramatic flair.

---

## Features

- **Live Game Data Integration:** Pulls real-time game state from a local API or JSON file.
- **AI-Generated Radio Scripts:** Uses LLMs (`Ollama`/`Qwen3`) to convert raw data into story-driven radio segments, styled after a Star Wars radio host.
- **Text-to-Speech Synthesis:** Converts the AI-generated script into audio using Bark TTS, with selectable speaker voices.
- **Star Wars Flair:** Broadcasts are filled with Huttese slang, ship calls, mock commercials, and never simply "list" information-everything is woven into narrative beats.
- **Output Management:** Saves both the text and audio broadcast, organized by timestamped folders.

---

## How It Works

1. **Fetch Game State:**
   - By default, fetches from `http://localhost:8080/api/data` (can read from a local JSON file).

2. **Filter and Format Data:**
   - Extracts logbook entries, mission offers, and faction names, filtering out irrelevant or repetitive content.

3. **Generate Radio Script:**
   - Passes the structured data to an LLM prompt, with a detailed system message instructing the AI to:
     - Speak as Dex Jettster, a smooth-talking Star Wars radio host.
     - Use Star Wars slang, dramatic delivery, and never list facts-always tell a story.
     - Structure the broadcast as `[BREAKING NEWS] > [COMMERCIAL BREAK] > [BOUNTY BOARD]`.

4. **Synthesize Audio:**
   - Splits the script into sentences, generates audio for each, and combines them into a single WAV file.

5. **Save Outputs:**
   - Stores input data and generated script for reference.

---

## Setup

### Dependencies

- Python 3.8+
- [`nltk`](https://www.nltk.org/) (for sentence tokenization)
- [`pydub`](https://github.com/jiaaro/pydub) (audio manipulation)
- [`bark`](https://github.com/suno-ai/bark) (text-to-speech)
- [`ollama`](https://github.com/ollama/ollama) (LLM API)
- [`requests`](https://docs.python-requests.org/en/latest/) (HTTP requests)
- [`scipy`](https://scipy.org/) (WAV file writing)
- [`numpy`](https://numpy.org/) (array handling)
- [`IPython`](https://ipython.org/) (optional, for notebook audio playback)

**Install dependencies:**
