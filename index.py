import pyautogui
import keyboard
import pytesseract
import cv2
import pyglet
import torch
from TTS.api import TTS

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

while True:
    try:
        # Using keyboard press as the trigger for the image-to-text conversion for now
        if keyboard.is_pressed('`'):

            # region function parameters are : left, top, width, height
            screenshot = pyautogui.screenshot(region=(356, 818, 1214, 174))
            screenshot.save(r'./screenshot.png')

            img = cv2.imread("screenshot.png")
            # Convert to gray-scale for easier read for the program
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

            # Replace the misidentified characters by the image to text conversion
            cv2.imwrite('thresh.png', thresh)
            threshText = pytesseract.image_to_string('thresh.png')
            threshText = threshText.replace("|", "I")
            threshText = threshText.replace("\n", " ")
            threshText = threshText.replace("L.", "I.")
            threshText = threshText.replace(".l ", ".I ")
            threshText = threshText.strip()
            print('**** THRESH.PNG  *****')
            print(threshText)

            # Get device
            device = "cuda" if torch.cuda.is_available() else "cpu"

            # List available 🐸TTS models
            print(TTS().list_models())

            # Init TTS
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

            # Run TTS
            # Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
            # Text to speech list of amplitude values as output
            wav = tts.tts(text=threshText, speaker_wav="voices/bg3_narrator.mp3", language="en")
            # Text to speech to a file
            tts.tts_to_file(text=threshText, speaker_wav="voices/bg3_narrator.mp3", language="en", file_path="output/output.mp3")

            # Play the audio
            player = pyglet.media.Player()
            source = pyglet.media.StaticSource(pyglet.media.load('output/output.mp3'))
            player.queue(source)
            player.play()

    except:
        break
