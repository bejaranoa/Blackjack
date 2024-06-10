import customtkinter as ctk
from PIL import Image
import random
import cards

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry('700x500')
root.minsize(700, 500)
root.maxsize(700,500)

root.configure()

ryanpoop = ctk.CTkImage(Image.open("anything.jpg"), size=(200, 200))

def get_random_card():
    return list(random.choice(list(cards.data.items())))[1]

def play_button():
    dealer_card = get_random_card()
    player_card = get_random_card()

    frame = ctk.CTkFrame(root)
    player_label = ctk.CTkLabel(frame, text=f'player card: {player_card}')
    dealer_label = ctk.CTkLabel(frame, text=f'dealer card: {dealer_card}',width=0.1)
    frame.pack(fill="both", expand=1)
    player_label.grid(row=6, column=0)
    dealer_label.grid(row=0, column =0)

    image_label = ctk.CTkLabel(frame, text="", image=ryanpoop)
    image_label.grid(row=1, column=3, padx=10)

button = ctk.CTkButton(master=root, text="Play", command=play_button)
button.place(relx=0.5, rely=0.40, anchor=ctk.CENTER)


quit=ctk.CTkButton(master=root, text="Quit", command=root.destroy)
quit.place(relx=0.5, rely=0.60, anchor=ctk.CENTER)


root.mainloop()