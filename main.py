from tkinter import *
from typing import List

import pandas
import random

# Next card function
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/top_100_kanji.csv")
all_words = data.to_dict(orient="records")
card = {}


def next_card():
    global card, delay
    window.after_cancel(delay)
    card = random.choice(all_words)
    lang = card["Japanese"]
    canvas.itemconfig(card_canvas, image=card_front_img)
    canvas.itemconfig(title_canvas, text="Japanese", fill="black")
    canvas.itemconfig(word_canvas, text=lang, fill="black")
    delay = window.after(3000, flip_card)


# Flip card function

def flip_card():
    english = card["English"]
    canvas.itemconfig(card_canvas, image=card_back_img)
    canvas.itemconfig(title_canvas, text="English", fill="white")
    canvas.itemconfig(word_canvas, text=english, fill="white")


def known():
    try:
        all_words.remove(card)
    except ValueError or IndexError:
        print("You have learnt all words!")
    data = pandas.DataFrame(all_words)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# UI

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

delay = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_canvas = canvas.create_image(400, 263, image=card_front_img)
title_canvas = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_canvas = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=known)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
