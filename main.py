from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
card={}
to_learn={}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data= pandas.read_csv("data/SP_EN.csv")
    to_learn=original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records") #[{'Spanish': 'importante', 'English': 'important'}]
#print(to_learn)
def new_card():
    global card, flip_timer
    window.after_cancel(flip_timer)
    card= random.choice(to_learn)
    canvas.itemconfig(card_title, text= "Spanish", fill = "black")
    canvas.itemconfig(card_text, text= card["Spanish"], fill = "black")
    canvas.itemconfig(card_image, image= card_front_image)
    flip_timer= window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=card["English"], fill="white")
    canvas.itemconfig(card_image, image= card_back_image)

def is_known():
    #if user clicks on green tick button, then the card should be removed from to_learn list since they already know it.
    to_learn.remove(card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index= False) #donot create indexes each time
    new_card()

#Creating a new window and configurations
window = Tk()
window.title("Flash Card")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526) #h and w of card image
card_front_image= PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_image= canvas.create_image(400, 263)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_text= canvas.create_text(400, 260, font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column =0, columnspan=2)

wrong_image=PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command= new_card)
wrong_button.grid(column=0, row=1)

right_image=PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command= is_known)
right_button.grid(column=1, row=1)

new_card()
window.mainloop()
