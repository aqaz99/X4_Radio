Star Wars Radio Blast Generator
This project generates immersive, Star Wars–themed "radio broadcast" audio segments based on live game state data. It transforms mission logs and faction updates into entertaining, in-universe radio news, complete with character voice, sound effects, and dramatic flair.

Features
Live Game Data Integration: Pulls real-time game state from a local API or JSON file.

AI-Generated Radio Scripts: Uses LLMs (Ollama/Qwen3) to convert raw data into story-driven radio segments, styled after a Star Wars radio host.

Text-to-Speech Synthesis: Converts the AI-generated script into audio using Bark TTS, with selectable speaker voices.

Star Wars Flair: Broadcasts are filled with Huttese slang, ship calls, mock commercials, and never simply "list" information-everything is woven into narrative beats.

Output Management: Saves both the text and audio broadcast, organized by timestamped folders.

How It Works
Fetch Game State:

By default, fetches from http://localhost:8080/api/data (can read from a local JSON file).

Filter and Format Data:

Extracts logbook entries, mission offers, and faction names, filtering out irrelevant or repetitive content.

Generate Radio Script:

Passes the structured data to an LLM prompt, with a detailed system message instructing the AI to:

Speak as Dex Jettster, a smooth-talking Star Wars radio host.

Use Star Wars slang, dramatic delivery, and never list facts-always tell a story.

Structure the broadcast as [BREAKING NEWS] > [COMMERCIAL BREAK] > [BOUNTY BOARD].

Synthesize Audio:

Splits the script into sentences, generates audio for each, and combines them into a single WAV file.

Save Outputs:

Stores input data and generated script for reference.

Setup
Dependencies
Python 3.8+

nltk (for sentence tokenization)

pydub (audio manipulation)

bark (text-to-speech)

ollama (LLM API)

requests (HTTP requests)

scipy (WAV file writing)

numpy (array handling)

IPython (optional, for notebook audio playback)

Install dependencies:

bash
pip install nltk pydub requests scipy numpy bark ollama
Model Setup
Download and preload Bark TTS models as needed.

Ensure Ollama is running locally with the qwen3 model available.

Usage
Configure Data Source:

By default, the script fetches live data from http://localhost:8080/api/data.

To use a local file, pass the file path to getGameStateInfo(local_file_path="yourfile.json").

Run the Script:

bash
python your_script.py
The script will fetch game data, generate a radio script, synthesize audio, and save results in a timestamped folder.

Output:

radio_alerts_<timestamp>/input_game_data.txt: Raw game data used.

radio_alerts_<timestamp>/radio_alert.txt: Generated radio script.

radio_alerts_<timestamp>/radio_alert.wav: Synthesized radio broadcast.

Customization
Speaker Voice:
Change the speaker variable (e.g., "v2/en_speaker_3") to select different Bark voices.

Prompt Tuning:
Modify the system prompt in generate_radio_blast for different radio personalities or broadcast styles.

Audio Playback:
The script plays the generated broadcast automatically using pydub.

Example Radio Broadcast
"Welcome back, spacers! This is Dex Jettster, your source for all things galactic. Stuka! Trouble's brewing in Boonta as Corporate Sector Authority forces mount a defense-traders, keep your eyes peeled..."

Notes
Repetition Avoidance:
The system prompt encourages variety and discourages repetitive broadcasts.

Expandability:
Easily adapt to other games or data sources by modifying the data extraction logic.

License
MIT License

Credits
Inspired by Star Wars universe radio and in-universe news broadcasts.

Built with Bark TTS, Ollama, and the open-source Python ecosystem.
