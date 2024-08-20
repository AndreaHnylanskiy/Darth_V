import speech_recognition as sr
import time
import pyaudio
import os
import pyttsx3
from fuzzywuzzy import fuzz, process
import datetime
from num2words import *
import webbrowser
import random
import json
from urllib.request import urlopen
import requests
import tempfile
import pygame
from io import BytesIO
from groq import Groq
import threading
import queue
import sys
import sounddevice as sd
import numpy as np

api_meteo = "Your API"
engine = pyttsx3.init()
client = Groq(
    api_key=("Your API"),
)
pygame.init()
screen = pygame.display.set_mode((1280, 800))

# Caricamento dell'immagine
original_image = pygame.image.load("DARTH VADER'S PHOTO")
image = pygame.transform.scale(original_image, (1280, 800))

# Definizione delle classi e delle funzioni

class CustomObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.angle = 0
        self.color = (218, 65, 32)

    def draw(self, surface):
        rotated_image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        rotated_image.fill((0, 0, 0, 0))
        pygame.draw.rect(rotated_image, self.color, (0, 0, self.rect.width, self.rect.height))
        rotated_column = pygame.transform.rotate(rotated_image, self.angle)
        surface.blit(rotated_column, self.rect.topleft)

    def rotate(self, angle):
        self.angle += angle

    def vary_height(self):
        max_height = self.original_height * 1.75
        min_height = self.original_height * 0.25
        variation = random.uniform(-1, 1)
        new_height = self.height_variation + variation
        self.height_variation = max(min_height, min(new_height, max_height))    

class Sparkle:
    def __init__(self, screen_width):
        self.x = random.randint(0, 1280)
        self.y = 1100
        self.speed = random.uniform(0.6, 2.0)
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (2, 2), 2)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.alpha = random.randint(200, 255)

    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.reset()

    def reset(self):
        self.y = 800
        self.x = random.randint(0, 1280)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def generate_sparkles(screen, amount):
    sparkles = []
    for _ in range(amount):
        x = random.randint(0, screen.get_width())
        y = random.randint(-500, -50)
        speed = random.uniform(0.1, 0.9)
        sparkles.append(Sparkle(x, y, speed))
    return sparkles

def draw_sparkles(screen, sparkles):
    for sparkle in sparkles:
        sparkle.move()
        sparkle.draw(screen)

def listen_microphone():
    global text  # Usiamo la variabile globale
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='it-IT')
            except sr.UnknownValueError:
                pass

sparkles = [Sparkle(screen.get_width()) for _ in range(120)]

text_display_time = 0
       

def update_objects(screen, text_q, sound_q):
    running = True
    font = pygame.font.Font(None, 36)
    text_to_display = ""
    sparkles = [Sparkle(screen.get_width()) for _ in range(120)]
    text_display_time = 0

    custom_object1 = CustomObject(25, 650, 50, 40)
    custom_object2 = CustomObject(100, 650, 50, 40)
    custom_object3 = CustomObject(175, 650, 50, 40)

    custom_object4 = CustomObject(1055, 650, 50, 40)
    custom_object5 = CustomObject(1130, 650, 50, 40)
    custom_object6 = CustomObject(1205, 650, 50, 40)
    custom_object_t = CustomObject(300, 625, 700, 150)

    custom_object1.rotate(90)
    custom_object2.rotate(90)
    custom_object3.rotate(90)
    custom_object4.rotate(90)
    custom_object5.rotate(90)
    custom_object6.rotate(90)


    custom_object_t = CustomObject(300, 625, 700, 150)
    custom_object_t.draw(screen)

    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(image, (0, 0))

        custom_object1.draw(screen)
        custom_object2.draw(screen)
        custom_object3.draw(screen)
        custom_object4.draw(screen)
        custom_object5.draw(screen)
        custom_object6.draw(screen)

        for sparkle in sparkles:
            sparkle.move()
            sparkle.draw(screen)

        pygame.display.flip()
        pygame.time.delay(10)

    pygame.quit()
    sys.exit()

def meteo(city):
    Base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = Base_url + "appid=" + api_meteo + "&q=" + city
    response=requests.get(url).json()
    temperature_kelvin = float(response["main"]["temp"])
    temperature_celsius = temperature_kelvin - 273.15
    info_desiderate = {
        "main": response["weather"][0]["main"],
        "description": response["weather"][0]["description"],
        "umidity": response["main"]["humidity"],
        "City": response["name"],
        "temperature": temperature_celsius
    }
    for key, value in info_desiderate.items():
        print(f"{key.capitalize()}: {value}")
    darth_vader(info_desiderate.items())

def Groq(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are darth vader and you are an assistant. you are not allowed to use special caracters, brakets"
            },

            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
    )
    reply=chat_completion.choices[0].message.content
    print(reply)
    darth_vader(reply)

def record_sound():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = r.listen(source)
            try:
                voice = r.recognize_google(audio, language="en-EN").lower()
                va_respond(voice)
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass


def play_mp3(file_path):
    # Inizializza il mixer di pygame
    pygame.mixer.init()
    
    # Carica il file MP3
    pygame.mixer.music.load(file_path)
    
    # Riproduce il file MP3
    pygame.mixer.music.play()
    
    # Attende la fine della riproduzione o l'interruzione
    try:
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()

def darth_vader(text):
    response = requests.request(
    method="POST",
    url="https://api.neets.ai/v1/tts",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "Your API"
    },
    json={
        "text": text,
        "voice_id": "darth-vader",
        "params": {
        "model": "ar-diff-50k"
        }
    }
    )
    # Carica l'audio
    audio_data = BytesIO(response.content)
    # Salva l'audio in un file temporaneo
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
        temp_audio_file.write(audio_data.getbuffer())
        temp_audio_file.seek(0)
        temp_audio_filename = temp_audio_file.name

    # Carica l'audio in pygame
    audio_sound = pygame.mixer.Sound(temp_audio_filename)

    # Riproduci l'audio
    audio_channel = audio_sound.play()

    stop_time = audio_sound.get_length() * 1

    # Attendi 1-2 secondi prima di interrompere la riproduzione
    start_time = time.time()
    while audio_channel.get_busy():
        elapsed_time = time.time() - start_time
        if elapsed_time >= stop_time:  # interrompi 1-2 secondi prima della fine
            audio_channel.stop()
            break

    temp_audio_file.close()

print("Hello")
darth_vader("Hello, my name is Darth Vader")

def va_respond(voice: str):
    cmd = recognize_cmd(filter_cmd(voice))
    if voice.startswith("ripeti"):
        darth_vader(voice)
    else:
        if cmd['percent'] <= 70:
            Groq(voice)
        else:
            print(cmd)
            execute_cmd(cmd['cmd'])

def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd

def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc

def execute_cmd(cmd: str):
    if cmd == 'help':
        text = "I Know: ..."
        text += "Say what time is it ..."
        text += "I know some jokes ..."
        darth_vader(text)
    elif cmd == 'ctime':
        def ctime():
            x = datetime.datetime.now()
            hour = (x.strftime("%H"))
            minute = (x.strftime("%M"))
            text = "it's " + num2words(hour, lang='en') + " and " + num2words(minute, lang='en')
            darth_vader(text)
        ctime()    
    elif cmd == 'joke':
        jokes = ['Getting mythology wrong is my Hercules ankle.',
                'I have an unconscious bias. I’m biased firmly towards being unconscious.',
                'Cats are like strippers – they sit on your lap and make you think they love you.',
                ' The UK is so small, they’ve got to keep all their lakes in one district.',
                'Last year, I had a great joke about inflation. But it’s hardly worth it now.',
                'One of the oddities of Wall Street is that it is the dealer and not the customer who is called broker.',
                'Did you hear they arrested the devil? Yeah, they got him on possession. ',
                'A bird in the hand is bad table manners.',
                'A small boy, reciting the Lord’s Prayer, ended by asking: “…and deliver us from people, amen',
                'How do you stop a bull from charging? Cancel its credit card.']
        darth_vader(random.choice(jokes))
    elif cmd == 'repeat':
        print(record_sound.voice)
    elif cmd == 'meteo':
        print("Oh well, if you ask me, I can help you to know the weather.Where do you live?")
        darth_vader("Oh well, if you ask me, I can help you to know the weather.Where do you live?")
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                voice = r.recognize_google(audio, language="it-IT").lower()
                meteo(voice)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass

        

VA_TBR = ('dici', 'fammi vedere', 'rispondi', 'dici', 'raccontami', 'quanto')

VA_CMD_LIST = {
    "help": ('lista dei commnadi', 'commandi', 'cosa sai fare', 'che sai fare', 'le tue skill', 'quali sono le tue skill', 'cosa puoi','your skills'),
    "ctime": ('Che ore sono', 'Che ore si sono fatte', 'adesso che ora è', 'ore','what time is it', 'time'),
    "meteo": ('che tempo porta oggi', 'meteo', 'meteo oggi', 'temporale','che tempo fa oggi', 'weather', 'there are clouds today'),
    "joke": ('tell me some jokes','some jokes','anneddoto', 'fammi sorridere', 'scherzo', 'dimmi una battuta', 'fammi ridere', 'divertimi','raccontami una balzeletta', 'raccontami un scherzo','dimmi una battuta'),
    "repeat": ('ripeti', 'dici', 'scrivi', 'puoi ripetere',),
}

def callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    sound_queue.put(volume_norm)

def main():
    text_queue = queue.Queue()
    global sound_queue
    sound_queue = queue.Queue()

    listen_thread = threading.Thread(target=listen_microphone, args=(text_queue,), daemon=True)
    listen_thread.start()

    record_sound_thread = threading.Thread(target=record_sound, daemon=True)
    record_sound_thread.start()
    
    stream = sd.InputStream(callback=callback)
    with stream:
        update_objects_thread = threading.Thread(target=update_objects, args=(screen, text_queue, sound_queue), daemon=True)
        update_objects_thread.start()


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            time.sleep(0.1)

if __name__ == "__main__":
    main()