import customtkinter as ctk
import random
import cards

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry('400x240')


def get_random_card():
    return list(random.choice(list(cards.data.items())))[1]

def button_function():
    dealer_card = get_random_card()
    player_card = get_random_card()

    frame = ctk.CTkFrame(root)
    player_label = ctk.CTkLabel(frame, text=f'player card: {player_card}')
    dealer_label = ctk.CTkLabel(frame, text=f'dealer card: {dealer_card}')
    frame.pack(fill="both", expand=1)
    player_label.pack()
    dealer_label.pack()

button = ctk.CTkButton(master=root, text="Play", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


root.mainloop()
