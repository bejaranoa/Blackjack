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

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(fill="both", expand=1)

        button = ctk.CTkButton(self.menu_frame, text="Play", command=self.play_button)
        button.place(relx=0.5, rely=0.40, anchor=ctk.CENTER)

        self.exit = ctk.CTkButton(self.menu_frame, text="Quit", command=self.destroy)
        self.exit.place(relx=0.5, rely=0.50, anchor=ctk.CENTER)

        aid=ctk.CTkButton(self.menu_frame, text="Help", command=self.help_button)
        aid.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        
    def check_player_score(self):
        if self.get_player_total() > 21:
            self.frame.destroy()
            self.display_game_status("You Busted")

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
            time.sleep(0.4)
        self.finish()

    def play_button(self):
        if hasattr(self, "menu_frame"):
            self.menu_frame.destroy()
        self.dealer_cards = [get_random_card()]
        self.player_cards = [get_random_card(), get_random_card()]
        self.frame = ctk.CTkFrame(self)
        self.player_label = ctk.CTkLabel(self.frame, 
        text=f'player card: {self.add_player_cards()} = {self.get_player_total()}')
        self.dealer_label = ctk.CTkLabel(self.frame, 
                        text=f'dealer card: {self.get_dealer_total()}',width=0.1)
        self.frame.pack(fill="both", expand=1)
        self.player_label.place(relx=0.08, rely = 0.5, anchor=ctk.CENTER)
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
            self.display_game_status(f"YOU WIN  The Dealer Got {dealer_total}")
        else:
            self.display_game_status(f"YOU LOSE  The Dealer Got {dealer_total}")
        play_again = ctk.CTkButton(text="Play again", command=self.restart,
                                   master=self.status_frame)
        play_again.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        done = ctk.CTkButton(text='Quit', command=self.destroy, 
                             master=self.status_frame)
        done.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def restart(self):
        self.status_frame.destroy()
        self.play_button()

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
    
    def help_button(self):
        self.menu_frame.destroy()
        self.help_frame1 = ctk.CTkFrame(self)
        self.help_frame1.pack(fill="both", expand=1)
        text=ctk.CTkLabel(self.help_frame1, 
                          text="The goal of blackjack is simple.\nAll one"
                           " needs to do to win is have a higher \nhand value "
                           "than the dealer, without going over \n21. Players "
                           "are dealt two cards and can then choose \nto “hit” "
                           "(receive additional cards) or “stand” \n(keep their "
                           "current hand)." )
        text.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)




if __name__ == "__main__":
    app = App()
    app.mainloop()
