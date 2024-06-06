import customtkinter as ctk
import random
import cards

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry('400x240')


def get_random_card():
    return list(random.choice(list(cards.data.items())))[1]

def play_button():
    dealer_card = get_random_card()
    player_card = get_random_card()

    frame = ctk.CTkFrame(root)
    player_label = ctk.CTkLabel(frame, text=f'player card: {player_card}')
    dealer_label = ctk.CTkLabel(frame, text=f'dealer card: {dealer_card}')
    frame.pack(fill="both", expand=1)
    player_label.pack(side="left", padx=0.2, pady=0.2, fill="x")
    dealer_label.pack(side="top", padx=0.5, pady=0.5)
    dealer_label.pack()

button = ctk.CTkButton(master=root, text="Play", command=play_button)
button.place(relx=0.5, rely=0.40, anchor=ctk.CENTER)


quit=ctk.CTkButton(master=root, text="Quit", command=root.destroy)
quit.place(relx=0.5, rely=0.60, anchor=ctk.CENTER)


root.mainloop()


