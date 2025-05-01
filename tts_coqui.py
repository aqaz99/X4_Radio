from datetime import datetime
from bark import generate_audio, SAMPLE_RATE
from bark.generation import (
    preload_models,
)
import numpy as np
import os
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
from pydub import AudioSegment
from pydub.playback import play
import nltk  # we'll use this to split into sentences
nltk.download('punkt')


os.environ['TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD'] = '1'
# download and load all models
preload_models()

radio_text_prompt = """
Good cycle, citizens! Here’s your latest update from across the galaxy:

Corporate Sector Authority forces are mounting a defense in Boonta. All traders and travelers are advised to exercise caution in the area.

Reports indicate increased pirate activity: Corellian Star Shuttles have been harassed by both Corporate Sector Authority and Galactic Empire mercenaries in Celanon, with several ships forced to flee after attacks.

The New Republic remains embroiled in conflicts on multiple fronts, with ongoing wars against the Mandalorian Death Watch, the Imperial Ascendancy, and the Galactic Empire. Volunteers are being sought to help secure the borders and repel incursions.

On the economic front, trade remains brisk. Corellian Star Shuttles continue to move large quantities of silicon wafers, microchips, and advanced electronics, with profits from recent trades exceeding hundreds of thousands of credits per run.

Station managers are calling for urgent restocking of resources at the CSA Ore Refinery in Boonta, aiming to raise supply levels above 50%. Traders willing to take on the challenge are promised generous rewards.

Finally, escort missions remain lucrative, with recent operations netting rewards upwards of 180,000 credits for successful protection of cargo ships across multiple sectors.

Stay tuned for further updates as the situation develops. Safe travels, and may your profits be ever in your favor!
""".replace("\n", " ").strip()

sentences = nltk.sent_tokenize(radio_text_prompt)

SPEAKER = "v2/en_speaker_6"
silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_folder = f"radio_alerts_{timestamp}"
os.makedirs(output_folder, exist_ok=True)

radio_blast_array = []
for index, sentence in enumerate(sentences):
    audio_snippet = (generate_audio(
        sentence, history_prompt=SPEAKER) * 32767).astype(np.int16)
    audio_segment = AudioSegment(
        data=audio_snippet.tobytes(),
        sample_width=2,
        frame_rate=SAMPLE_RATE,
        channels=1
    )
    wav_path = os.path.join(output_folder, f"{index}_radio_alert.wav")

    write_wav(wav_path, SAMPLE_RATE, audio_snippet)
    radio_blast_array.append(audio_segment)

for blast in radio_blast_array:
    play(blast)
