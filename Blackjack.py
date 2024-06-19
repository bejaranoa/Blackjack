import customtkinter as ctk
from PIL import Image
import random
import cards
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def get_key_from_value(dict, v) -> str:
    for key, value in dict.items():
        if value == v:
            return key
    return None

def get_random_card():
    random_card = list(random.choice(list(cards.data.items())))[1]
    del cards.data[get_key_from_value(cards.data, random_card)]
    return random_card

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.minsize(700, 500)
        self.maxsize(700,500)        

        self.dealer_cards = [get_random_card()]
        self.player_cards = [get_random_card(), get_random_card()]

        button = ctk.CTkButton(master=self, text="Play", command=self.play_button)
        button.place(relx=0.5, rely=0.40, anchor=ctk.CENTER)

        self.exit = ctk.CTkButton(master=self, text="Quit", command=self.destroy)
        self.exit.place(relx=0.5, rely=0.60, anchor=ctk.CENTER)

    def check_player_score(self):
        if self.get_player_total() > 21:
            self.frame.destroy()
            self.display_game_status("You Busted ;)")

    def increment_player_score(self):
        self.player_cards.append(get_random_card())
        self.check_player_score()
        self.player_label.configure(text=f'player card: {self.add_player_cards()} = {self.get_player_total()}')

    def increment_dealer_score(self):
        dealer_total = self.get_dealer_total()
        while dealer_total < 17:
            self.dealer_cards.append(get_random_card())
            dealer_total = self.get_dealer_total()
            self.dealer_label.configure(text=f'dealer card: {dealer_total}')
            time.sleep(0.8)
        self.finish()


    def play_button(self):
        self.frame = ctk.CTkFrame(self)
        self.player_label = ctk.CTkLabel(self.frame, 
        text=f'player card: {self.add_player_cards()} = {self.get_player_total()}')
        self.dealer_label = ctk.CTkLabel(self.frame, 
                        text=f'dealer card: {self.get_dealer_total()}',width=0.1)
        self.frame.pack(fill="both", expand=1)
        self.player_label.place(relx=0.06, rely = 0.5, anchor=ctk.CENTER)
        self.dealer_label.place(relx= 0.06, rely = 0.02, anchor=ctk.CENTER)
        hit=ctk.CTkButton(self.frame, text="HIT", command=self.increment_player_score)
        hit.place(relx= 0.35, rely = 0.5, anchor=ctk.CENTER)
        stand=ctk.CTkButton(self.frame, text='STAND', command=self.increment_dealer_score)
        stand.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)

    def display_game_status(self, message: str):
        self.frame.destroy()
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(fill="both", expand=1)
        self.status_label = ctk.CTkLabel(self.status_frame, text=message)
        self.status_label.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

    def finish(self):
        dealer_total = self.get_dealer_total()
        player_total = self.get_player_total()
        if dealer_total > 21 or player_total > dealer_total:
            self.display_game_status("YOU WIN ;P")
        else:
            self.display_game_status(f"""YOU LOSE ;(          The Dealer Got {dealer_total}""")
        play_again = ctk.CTkButton(text="Play again", command=self.status_frame.destroy,
                                   master=self.status_frame)
        play_again.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        done = ctk.CTkButton(text='Quit', command=self.destroy, 
                             master=self.status_frame)
        done.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        
        
        

    def get_dealer_total(self):
        total = 0
        for card in self.dealer_cards:
            total = total + card
        return total

    def get_player_total(self):
        total = 0
        for card in self.player_cards:
            total = total + card
        return total

    def add_player_cards(self):
        cards = ""
        for card in self.player_cards:
            cards = cards + f' {str(card)}'
        return cards
    
    
    
app = App()
app.mainloop()
