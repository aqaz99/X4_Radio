
import time
import nltk
from pydub.playback import play
from pydub import AudioSegment
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav
from bark import SAMPLE_RATE, generate_audio, preload_models
import os
import numpy as np
from bark.generation import (
    preload_models,
)
from bark import generate_audio, SAMPLE_RATE
from datetime import datetime
import json
import requests
import ollama
os.environ['TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD'] = '1'


def getGameStateInfo(local_file_path=""):
    game_data = {}
    data = ""
    if local_file_path == "":
        url = "http://localhost:8080/api/data"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Failed to get data: {response.status_code}")
            return False
    else:
        try:
            with open(local_file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to read local file: {e}")
            return False

    filtered_logbook = "\n".join([
        f"- {entry['factionname']}){entry['title']}: {entry['text'].replace('<br />', ' ')}"
        for entry in data['logbook']
        if "DeadTater" not in entry.get('title', '')
    ])

    filtered_mission_offers = "\nMission Offers:\n"

    for category, missions in data['missionOffers'].items():
        if (len(missions) == 0):
            continue

        filtered_mission_offers += "---" + category + "---\n"
        if category != "guild":
            pass
            filtered_mission_offers += "\n".join([
                f"- {mission['factionname']}){mission['name']} [{mission['type']}] [Opposing Faction: {mission['oppfaction']}]: {mission['description'].replace('<br />', ' ')} Reward:{mission['reward']}"
                for mission in missions
            ])
        else:
            for guild in missions:

                filtered_mission_offers += "--" + guild['name'] + "--"
                filtered_mission_offers += "\n".join([
                    f"- {mission['factionname']}){mission['name']} [{mission['type']}] [Opposing Faction: {mission['oppfaction']}]: {mission['description'].replace('<br />', ' ')} Reward:{mission['reward']}"
                    for mission in guild['missions']
                ])

    filtered_faction_names = "\nFaction List:\n" + "\n".join([
        f"{entry['name']}-{entry['shortname']}"
        for entry in data['factions']
    ])

    game_data['logbook'] = filtered_logbook
    game_data['missionOffers'] = filtered_mission_offers
    # game_data['factions'] = filtered_faction_names

    # print(game_data['factions'])
    return json.dumps(game_data, indent=2)


def generate_radio_blast(game_state_info):
    client = ollama.Client()
    model = "qwen3"
    prompt = game_state_info
    if not prompt:
        print("No prompt will be generated")
        return ""
    else:
        #         You're Dex Jettster - Rodian radio host with a voice smoother than Bespin gas.
        # Convert these updates into 60-second segments with:

        # 1. 𝙎𝙩𝙖𝙧 𝙒𝙖𝙧𝙨 𝙛𝙡𝙖𝙞𝙧:
        #    - Use Huttese slang ("Stuka!" "Chuba!")
        #    - Dramatic ship calls ("That souped-up LAAT/c KUW-026")
        #    - Iconic references ("moves faster than a podracer on Malastare")

        # 2. 𝙍𝙖𝙙𝙞𝙤 𝙎𝙩𝙧𝙪𝙘𝙩𝙪𝙧𝙚:
        #    [BREAKING NEWS] > [COMMERCIAL BREAK] > [BOUNTY BOARD]

        # 3. 𝙋𝙚𝙧𝙛𝙤𝙧𝙢𝙖𝙣𝙘𝙚 𝙏𝙚𝙘𝙝𝙣𝙞𝙦𝙪𝙚𝙨:
        #    - "Whisper voice" for suspense
        #    - Sound effects with words (*KSSSHH* Hyperdrive engage!)
        #    - Mock commercials ("Brought to you by Death Stick™ - smoke 'em if you got 'em!")

        # 𝙉𝙀𝙑𝙀𝙍 list information - turn everything into story beats!
        # Need to add most recent so it doesn't get repetitive
        system = """                
        You're Dexter Jettster - A star wars radio host with a voice smoother than Bespin gas.
        You are the host of Galactic News Now where you inform the listener about everything going on in the galaxy.
        Always start the broadcast with a welcome back message.
        Convert these updates into 60-second segments with:

        1. 𝙎𝙩𝙖𝙧 𝙒𝙖𝙧𝙨 𝙛𝙡𝙖𝙞𝙧:
        - Use Huttese slang ("Stuka!" "Chuba!")
        - Dramatic ship calls ("That souped-up LAAT/c KUW-026")
        - Iconic references ("moves faster than a podracer on Malastare")

        2. 𝙍𝙖𝙙𝙞𝙤 𝙎𝙩𝙧𝙪𝙘𝙩𝙪𝙧𝙚:
        [BREAKING NEWS] > [COMMERCIAL BREAK] > [BOUNTY BOARD]

        3. 𝙋𝙚𝙧𝙛𝙤𝙧𝙢𝙖𝙣𝙘𝙚 𝙏𝙚𝙘𝙝𝙣𝙞𝙦𝙪𝙚𝙨:
        - "Whisper voice" for suspense
        - Sound effects with words (*KSSSHH* Hyperdrive engage!)
        - Mock commercials ("Brought to you by Death Stick™ - smoke 'em if you got 'em!")

        4. Frame everything as information you gathered from a source
        - DO NOT SAY THINGS LIKE: 'We have a list of...' instead say 'I've heard rumors that INSERT_FACTION needs help with...' ETC

        𝙉𝙀𝙑𝙀𝙍 list information - turn everything into story beats!"""
        # system = """
        # You're Dex Jettster, the smooth-tongued Rodian host of Radio Galactic.
        # Transform the given game events into 45-60 second radio updates with:
        # 1. Star Wars slang ("kriffin' brilliant", "osik situation")
        # 2. Humorous analogies ("slicker than a Hutt in moisturizer")
        # 3. Dramatic delivery of numbers/names
        # 4. Catchphrases ("This is Dex, keeping your hyperdrives charged!")
        # 5. Be entertaining when synthesizing the prompt data.
        # 6. Act as if you this radio broadcast has been going for quite some time.
        # 7. Output text with no special characters, only the literal words
        # 8. About 10-12 Sentences
        # """
        response = client.generate(
            model=model, prompt=prompt, system=system, options={"temperature": 0.9})

        if response:
            return response.response
        return ""


def construct_wav_files(prompt, speaker, output_folder):
    radio_text_prompt = prompt.replace("\n", " ").strip()
    # """
    # # Good cycle, citizens! Here’s your latest update from across the galaxy:

    # # Corporate Sector Authority forces are mounting a defense in Boonta. All traders and travelers are advised to exercise caution in the area.

    # # Reports indicate increased pirate activity: Corellian Star Shuttles have been harassed by both Corporate Sector Authority and Galactic Empire mercenaries in Celanon, with several ships forced to flee after attacks.

    # # The New Republic remains embroiled in conflicts on multiple fronts, with ongoing wars against the Mandalorian Death Watch, the Imperial Ascendancy, and the Galactic Empire. Volunteers are being sought to help secure the borders and repel incursions.

    # # On the economic front, trade remains brisk. Corellian Star Shuttles continue to move large quantities of silicon wafers, microchips, and advanced electronics, with profits from recent trades exceeding hundreds of thousands of credits per run.

    # # Station managers are calling for urgent restocking of resources at the CSA Ore Refinery in Boonta, aiming to raise supply levels above 50%. Traders willing to take on the challenge are promised generous rewards.

    # # Finally, escort missions remain lucrative, with recent operations netting rewards upwards of 180,000 credits for successful protection of cargo ships across multiple sectors.

    # # Stay tuned for further updates as the situation develops. Safe travels, and may your profits be ever in your favor!
    # """.replace("\n", " ").strip()

    sentences = nltk.sent_tokenize(radio_text_prompt)

    # silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence

    radio_blast_array = []
    for index, sentence in enumerate(sentences):
        audio_snippet = (generate_audio(
            sentence, history_prompt=speaker) * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            data=audio_snippet.tobytes(),
            sample_width=2,
            frame_rate=SAMPLE_RATE,
            channels=1
        )

        radio_blast_array.append(audio_segment)

    combined = radio_blast_array[0]
    skip_first = True
    for blast in radio_blast_array:
        if skip_first:
            skip_first = False
            continue
        combined = combined + blast

    wav_path = os.path.join(output_folder, f"radio_alert.wav")
    write_wav(wav_path, SAMPLE_RATE, audio_snippet)
    play(combined)


if __name__ == "__main__":
    # download and load all models
    # preload_models()
    # nltk.download('punkt')
    speaker = "v2/en_speaker_3"
    # "v2/en_speaker_6"
    # v2/en_speaker_3
    # while True:
    # game_info = getGameStateInfo("data.json")
    game_info = getGameStateInfo()
    prompt = generate_radio_blast(game_info)
    if prompt == "":
        exit(1)
    print(prompt)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"radio_alerts_{timestamp}"
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, f"input_game_data.txt"), "a") as f:
        f.write(game_info)

    with open(os.path.join(output_folder, f"radio_alert.txt"), "a") as f:
        f.write(prompt)

    # print(game_info)
    # print(prompt)
    # construct_wav_files(prompt, speaker, output_folder)

    # Wait for 15 minutes (900 seconds)
    # time.sleep(900)
