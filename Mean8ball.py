# -----------------------
#
# Mean8ball.py
# Tyson Aramaki
#
# -----------------------

import random
from io import BytesIO
from pygame import mixer
from gtts import gTTS
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition

#set of 8 ball answers
yes_answers = ["It is certain","It is decidedly so","Without a Doubt",
    "You may rely on it", "As i see it, yes", "Most likely"]
no_answers = ["Don't count on it","My sources say no","Very doubtful",
    "The outlook is not good", "No", "The chances are slim to none"]
neutral_answers = ["I cannot answer that", "Ask again later", "Better not tell you that"]

#record question
recognizer=speech_recognition.Recognizer()
with speech_recognition.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source,duration=1)
    print('\nAsk your question...')
    recordedaudio=recognizer.listen(source)
try:
    message = recognizer.recognize_google(recordedaudio,language='en-US')
    print("You asked: "+message)
except Exception as ex:
    print(ex)

#analyze sentiment
Sentence=[str(message)]
analyser=SentimentIntensityAnalyzer()
for i in Sentence:
    v=analyser.polarity_scores(i)

#select answer
if v['compound'] > 0:
    talk = no_answers[random.randint(0,5)]
elif v['compound'] < 0:
    talk = yes_answers[random.randint(0,5)]
else:
    talk = neutral_answers[random.randint(0,2)]

#create text to speech mp3 and play it
mixer.init()
mp3_answer = BytesIO()
tts = gTTS(talk, lang='en')
tts.write_to_fp(mp3_answer)

mixer.music.load(mp3_answer, "mp3")
mixer.music.play()
time.sleep(3)