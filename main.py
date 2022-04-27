import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

sample = ""
timer = None

try:
    dataframe = pd.read_csv(r"data/words_to_learn.csv")
except FileNotFoundError:
    dataframe = pd.read_csv(r"data/french_words.csv")
finally:
    # sample = dataframe.sample() # random Sample
    to_learn = dataframe.to_dict(orient="records")


def next_card():
    global sample, timer
    sample = random.choice(to_learn)
    sample_f = sample["French"]
    
    canvas.itemconfig(canvas_img, image=card_front_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=sample_f, fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    global sample, timer
    sample_e = sample["English"]

    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=sample_e, fill="white")
    window.after_cancel(timer)


def card_learned():
    to_learn.remove(sample)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv(r"data/words_to_learn.csv", index=False) # Keine Indexnummern schreiben
    next_card()


# Window
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Images
card_back_img = PhotoImage(file=r"images/card_back.png")
card_front_img = PhotoImage(file=r"images/card_front.png")
right_img = PhotoImage(file=r"images/right.png")
wrong_img = PhotoImage(file=r"images/wrong.png")

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="Titel", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


# Buttons
right_button = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=card_learned)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=1, column=0)


next_card()
window.mainloop()
