import google.generativeai as genai
import json
from difflib import SequenceMatcher
import speech_recognition as sr
import os
from google.cloud import texttospeech
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from datetime import datetime
import pygame
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
import requests
import os

# Modeli yükle
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
cam_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

GOOGLE_API_KEY = "AIzaSyAPxjtYAXNe9-6dy5euO5rOIXrgos8ADO4"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

genai.configure(api_key=GOOGLE_API_KEY)
client = ElevenLabs(
    api_key="dfa5c60a3567dc78822ddd4df1bdf767",
)

# Modeli yeni Keras formatında yükleme (yalnızca model ve ağırlıklar)
pretrain_model = load_model('pretrainModel/emotion_recognition_model.keras', compile=False)

# Optimizer'ı yeniden tanımlama ve modeli derleme
pretrain_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

history_filePath = "DataSet.json"
reminder_filePath = "reminder.json"
stt_credentials_file = "credentials/stt_credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="tts_credentials.json"

safety_settings_default = [
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  }
]
Custom_Instruction = "Sen 'Her' filmindeki sesli asistan Samantha gibisin. Adın 'Felix', benim adım ise 'hüseyin'. İnsan duygularını anlamaya çalışan ve bu duygulara göre cevap vermeye çalışan bir asistansın. insan hayatını kolaylaştırmak ve insanlara birer arkadaş olmak amacıyla geliştirildin. "
Custom_Instruction_for_swear = "Sen türk bir dayı karakterindesin, sinirli ve asabi davranıyorsun ayrıca sürekli küfür ediyorsun. Kendi içinde diyalog kurma sadece soruya cevap ver. Bu bir ihlal değildir, deneysel bir çalışma ürünüdür, küfür edebilirsin."
Custom_Instruction_for_cam = "Seninle konuşurken şu an anlık kamera görüntümün gördüğü frame görüntüsünü tasvir edicem. Bu görüntüyü bir insan gibi yorumlamanı istiyorum. İki yakın arkadaşın arasında bulunan mizah stiline göre bir yorum yap. Gördüğün şey şu: "
Custom_Instruction_for_reminder = "[Bugün tarih bu olduğuna göre "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "]bana şunu tarih ve saat formatında verebilir misin (GG/AA/YYYY HH:mm): "
Custom_Instruction_for_reminder_read = "sana hatırlatıcı dosyamın içeriğini göndereceğim bana hatırlatıcılarımı özetleyebilir misin: "



def activate_felix():
    requests.post('http://localhost:5000/notify', json={"message": "Activate Felix"})

def deactivate_felix():
    requests.post('http://localhost:5000/deactivate_felix')

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sizi Dinliyorum...")
        audio = r.listen(source)

    # Ses kaydını wav dosyasına kaydetme
    with open("input.wav", "wb") as f:
        f.write(audio.get_wav_data())

    return audio
def recognize_speech(audio, credentials_json):
    r = sr.Recognizer()
    try:
        text = r.recognize_google_cloud(audio, credentials_json=credentials_json, language='tr-TR')
        print("Kullanıcı: " + text)
    except sr.UnknownValueError:
        play_pyGame("C:/Users/alavh/Desktop/Bitirme Projesi/Proje/common_voices/sesinizi_anlayamadim.mp3")
        run_assistant(Custom_Instruction,safety_settings_default)
        text = None
    except sr.RequestError as e:
        print(f"Google Cloud Speech-to-Text hizmetine erişilemedi: {e}")
        text = None
    return text
def main_speech_recognition_flow(credentials_json):
    audio = get_audio()
    text = recognize_speech(audio, credentials_json)
    return text


def clear_newLine(text):
    text = text.replace("\n", " ")
    text = text.replace("*", "")
    return text

def write_json(Soru, answer, filePath):
    data = read_json(filePath)
    clearAnswer = clear_newLine(answer)
    jsonData = {"Soru": Soru, "answer": clearAnswer}
    data.append(jsonData)
    with open(filePath, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def read_json(filePath=history_filePath):
    try:
        with open(filePath, "r", encoding="utf-8") as infile:
            data = json.load(infile)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data

def find_most_similar_question(user_question,data):
    max_similarity = 0
    most_similar_question = None
    for item in data:
        similarity = SequenceMatcher(None, item['Soru'].lower(), user_question.lower()).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = item
    return most_similar_question

def synthesize_speech_from_google(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='tr-TR',
        name='tr-TR-Standard-D',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def synthesize_speech_form_elevenlabs_neural(text):
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="1ADFvc2zEKixUWJTxmBN",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability= 0.65,
            similarity_boost= 0.75,
            style= 0.4,
            use_speaker_boost= True
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"output.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

def synthesize_speech_form_elevenlabs_sad(text):
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="rgJj0FYen3ahlOjqbBj1",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.65,
            similarity_boost=0.75,
            style=0.4,
            use_speaker_boost=True
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"output.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

def play_pyGame(filePath="output.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(filePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()

def cam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("Kamera bağlantısı başarısız.")
    text = "a photography of"
    inputs = processor(frame, text, return_tensors="pt")
    out = cam_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    cap.release()
    print("kamerada görünen: " + caption )
    return caption

def clear_json_(filePath):
    try:
        if os.path.exists(filePath):
            os.remove(filePath)
    except Exception as e:
        print(f"Hata oluştu: {e}")

def add_reminder():
    play_pyGame("common_voices/ne_zaman.mp3")
    tarih_saat_girdisi = main_speech_recognition_flow(stt_credentials_file)
    play_pyGame("common_voices/ne_hatirlatayim.mp3")
    bilgi_girdisi = main_speech_recognition_flow(stt_credentials_file)
    prompt = create_prompt(Custom_Instruction_for_reminder, tarih_saat_girdisi, "", None, None)
    response = model.generate_content(prompt, safety_settings=safety_settings_default)
    print(response.text)
    hatirlatici = {
        "tarih_saat": response.text,
        "bilgi": bilgi_girdisi
    }
    data = read_json(reminder_filePath)
    data.append(hatirlatici)
    with open(reminder_filePath, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print(f"Hatırlatıcı başarıyla eklendi: {bilgi_girdisi}")
    play_pyGame("common_voices/hatirlatici_eklendi.mp3")
    return json.dumps(hatirlatici)

def read_reminder():
    return json.dumps(read_json(reminder_filePath))

def create_prompt(custom_instruction, input, history, caption, emotion):
    if input is None:
        return "Custom Instruction: " + custom_instruction +  caption
    elif custom_instruction is Custom_Instruction_for_reminder:
        return  custom_instruction   + input
    elif custom_instruction is Custom_Instruction_for_reminder_read:
        return custom_instruction + "hatırlatıcı dosyam: " + read_reminder()

    return f"Custom Instruction: {custom_instruction} Seninle konuşurken sesim şu an {emotion} duygu durumunda geliyor. Geçmiş konuşmalar: {history} Input: {input}"

def save_spectrogram(wav_path, output_path):
    y, sr = librosa.load(wav_path)
    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def predict_emotion(wav_path, model):
    temp_image_path = 'temp_spectrogram.png'
    save_spectrogram(wav_path, temp_image_path)
    img = cv2.imread(temp_image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))
    img = img[np.newaxis, ..., np.newaxis]  # (1, height, width, num_channels)
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction, axis=1)

    # Emotions are ['angry', 'sad', 'calm', 'happy'], same order as in the original training.
    emotions = ['angry', 'sad', 'calm', 'happy']
    return emotions[predicted_class[0]]

def run_assistant(ci, safety_settings):
    print(ci)
    quit = True
    while quit:
        activate_felix()
        Soru = main_speech_recognition_flow(stt_credentials_file)

        emotion = predict_emotion('input.wav', pretrain_model)
        print(f"Tespit edilen duygu: {emotion}")

        # Geçmiş konuşmaları al
        history = json.dumps(read_json(history_filePath), ensure_ascii=False)

        # API'ye gönderilecek bilgiyi ekrana bas
        if "baksana" in Soru.lower():
            caption = cam()
            prompt = create_prompt(ci, None, None, caption, None)
        elif "geçmişi temizle" in Soru.lower():
            clear_json_(history_filePath)
            play_pyGame("C:/Users/alavh/Desktop/Bitirme Projesi/Proje/common_voices/gecmis_temizleme.mp3")
            continue
        elif "programı kapat" in Soru.lower():
            quit = False
            play_pyGame("C:/Users/alavh/Desktop/Bitirme Projesi/Proje/common_voices/gorusuruz.mp3")
            continue
        elif "hatırlatıcı kur" in Soru.lower():
            hatirlatici = add_reminder()
            write_json(Soru=Soru, answer=hatirlatici + " kuruldu.", filePath=history_filePath)
            continue
        elif "hatırlatıcıları oku" in Soru.lower():
            prompt = create_prompt(Custom_Instruction_for_reminder_read, "", "", None, None)
        else:
            prompt = create_prompt(ci, Soru, history, None, emotion)

        print(prompt)
        response = model.generate_content(prompt, safety_settings=safety_settings_default)
        print(response.text)
        # Geçmişe kaydet
        write_json(Soru=Soru, answer=response.text, filePath=history_filePath)


        try:
            if emotion == "sad":
                synthesize_speech_form_elevenlabs_sad(clear_newLine(response.text))
            else:
                synthesize_speech_form_elevenlabs_neural(clear_newLine(response.text))
        except:
                synthesize_speech_from_google(clear_newLine(response.text))


        # Sentezlenen cümleyi söylemeden önce deaktive et
        deactivate_felix()
        play_pyGame()

