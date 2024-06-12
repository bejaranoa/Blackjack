import customtkinter as ctk
from PIL import Image
import random
import cards

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def get_random_card():
    return list(random.choice(list(cards.data.items())))[1]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.minsize(700, 500)
        self.maxsize(700,500)        

        self.dealer_card = get_random_card()
        self.player_card = get_random_card()

        def check_player_score():
            if self.player_card > 21:
                self.frame.destroy()
                self.lost_frame = ctk.CTkFrame(self)
                self.lost_frame.pack(fill="both", expand=1)
                self.lost_label = ctk.CTkLabel(self.lost_frame, text="You lost idiot")
                self.lost_label.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

        def increment_player_score():
            self.player_card = self.player_card + get_random_card()
            check_player_score()
            self.player_label.configure(text=f'playre card: {self.player_card}')

        def increment_dealer_score():
            self.dealer_card = self.dealer_card + get_random_card()

        def play_button():
            self.frame = ctk.CTkFrame(self)
            self.player_label = ctk.CTkLabel(self.frame, text=f'player card: {self.player_card}')
            dealer_label = ctk.CTkLabel(self.frame, text=f'dealer card: {self.dealer_card}',
                                        width=0.1)
            self.frame.pack(fill="both", expand=1)
            self.player_label.place(relx=0.06, rely = 0.5, anchor=ctk.CENTER)
            dealer_label.place(relx= 0.06, rely = 0.02, anchor=ctk.CENTER)
            hit=ctk.CTkButton(self.frame, text="HIT", command=increment_player_score)
            hit.place(relx= 0.5, rely = 0.5, anchor=ctk.CENTER)
        
        button = ctk.CTkButton(master=self, text="Play", command=play_button)
        button.place(relx=0.5, rely=0.40, anchor=ctk.CENTER)

        quit = ctk.CTkButton(master=self, text="Quit", command=self.destroy)
        quit.place(relx=0.5, rely=0.60, anchor=ctk.CENTER)
    
app = App()
app.mainloop()
