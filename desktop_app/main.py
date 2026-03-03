import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import uuid
import hashlib
import speech_recognition as sr
# =========================
# INITIAL SETUP
# =========================

translator = Translator()
pygame.mixer.init()

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja"
}

dark_mode = False
cached_audio = None
cached_hash = None

# =========================
# FUNCTIONS
# =========================

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    bg = "#1e1e1e" if dark_mode else "white"
    fg = "white" if dark_mode else "black"

    root.config(bg=bg)

    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Checkbutton)):
            widget.config(bg=bg, fg=fg)

def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        return

    selected_language = language_var.get()
    dest_lang = languages[selected_language]

    try:
        translated = translator.translate(text, dest=dest_lang)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)

        if auto_speak_var.get():
            speak_text()

    except:
        status_label.config(text="Translation Error")

def speak_text():
    global cached_audio, cached_hash

    text = output_text.get("1.0", tk.END).strip()
    selected_language = language_var.get()
    lang_code = languages[selected_language]

    if not text:
        return

    text_hash = hashlib.md5((text + lang_code).encode()).hexdigest()

    try:
        status_label.config(text="Generating speech...")
        root.update()

        # Check Cache
        if cached_hash == text_hash and cached_audio:
            filename = cached_audio
        else:
            filename = f"speech_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(filename)

            cached_audio = filename
            cached_hash = text_hash

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        status_label.config(text="Speech Completed")

    except Exception as e:
        status_label.config(text="Speech Error")
        print("Speech Error:", e)

def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        status_label.config(text="Listening...")
        root.update()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)

        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, text)

        status_label.config(text="Speech Recognized!")
        if auto_speak_var.get():
            translate_text() 
    except sr.UnknownValueError:
        status_label.config(text="Could not understand audio")

    except sr.RequestError:
        status_label.config(text="Speech service unavailable")

    except Exception as e:
        status_label.config(text="Microphone Error")
        print("Speech Input Error:", e)

# =========================
# GUI SETUP
# =========================

root = tk.Tk()
root.title("AI Language Translator - Premium")
root.geometry("700x600")
root.resizable(False, False)

title = tk.Label(root, text="🌍 AI Language Translator", font=("Arial", 18, "bold"))
title.pack(pady=10)

input_text = tk.Text(root, height=5, font=("Arial", 12))
input_text.pack(pady=5)

language_var = tk.StringVar()
language_dropdown = ttk.Combobox(root, textvariable=language_var, state="readonly")
language_dropdown["values"] = list(languages.keys())
language_dropdown.current(0)
language_dropdown.pack(pady=5)

tk.Button(root, text="Translate", command=translate_text, width=25).pack(pady=5)
tk.Button(root, text="🔊 Speak Output", command=speak_text, width=25).pack(pady=5)
tk.Button(root, text="🎙 Speech Input", command=speech_to_text, width=25).pack(pady=5)
# Auto Speak Option
auto_speak_var = tk.BooleanVar()
auto_speak_checkbox = tk.Checkbutton(root, text="Auto Speak After Translation", variable=auto_speak_var)
auto_speak_checkbox.pack(pady=5)

# Speed Slider (Visual only – gTTS uses natural speed)
tk.Label(root, text="Voice Speed (Visual Indicator)").pack(pady=5)
speed_slider = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
speed_slider.set(1.0)
speed_slider.pack(pady=5)

tk.Button(root, text="🌙 Toggle Dark Mode", command=toggle_theme, width=25).pack(pady=10)

output_text = tk.Text(root, height=5, font=("Arial", 12))
output_text.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()