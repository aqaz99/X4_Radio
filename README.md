# Star Wars Radio Blast Generator

Generates immersive Star Wars-themed "radio broadcasts" based on live game data, transforming mission logs and faction updates into entertaining in-universe radio news with character voices and sound effects.

## Features

- **Live Game Data Integration:** Pulls real-time data from local API or JSON files
- **AI-Generated Scripts:** Uses LLMs (Ollama/Qwen3) to convert data into narrative radio segments
- **Voice Synthesis:** Creates audio using Bark TTS with selectable voices
- **Star Wars Immersion:** Incorporates Huttese slang, ship calls, and mock commercials
- **Complete Output:** Saves both text scripts and audio files

## How It Works

1. **Fetch Game State** from local API (default) or JSON file
2. **Process Data** by extracting logbook entries, missions, and faction information
3. **Generate Script** using LLM with detailed Dex Jettster radio host persona
4. **Synthesize Audio** by converting script to speech with Star Wars flair
5. **Save Results** to timestamped folders for reference

## Setup

### Requirements
- Python 3.8+
- Libraries: `nltk`, `pydub`, `bark`, `ollama`, `requests`, `scipy`, `numpy`, `IPython` (optional)

### Models
- Bark TTS models (preloaded)
- Ollama running with `qwen3` model

## Usage

1. **Configure source:** Use default API endpoint or specify local file
2. **Run script:** Processes data and generates broadcast
3. **Output:** Find results in `radio_alerts_<timestamp>/` folder:
   - Input data, radio script text, and WAV audio file

## Customization

- **Voice:** Change `speaker` variable for different Bark voices
- **Style:** Modify `system` prompt for different broadcast personalities
- **Data Source:** Easily adaptable to other games/data formats

## Example Output

> "Welcome back, spacers! This is Dex Jettster, your source for all things galactic. Stuka! Trouble's brewing in Boonta as Corporate Sector Authority forces mount a defense-traders, keep your eyes peeled..."

## License

MIT License
