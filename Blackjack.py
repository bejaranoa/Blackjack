import customtkinter as ctk
from PIL import Image
import copy, pywinstyles, time, cards, random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):


    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.minsize(700, 500)
        self.maxsize(700,500)

        self.create_new_copy()
        self.start()

    def create_new_copy(self):
        self.copied_cards = copy.deepcopy(cards.data)

    def get_random_card(self):
        def get_key_from_value(dict, v) -> str:
            for key, value in dict.items():
                if value == v:
                    return key
            return None
        random_card = list(random.choice(list(self.copied_cards.items())))[1]
        del self.copied_cards[get_key_from_value(self.copied_cards, random_card)]
        return random_card

    #Menu:
        
    def start(self):
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(fill="both", expand=1)

        button = ctk.CTkButton(self.menu_frame, text="Play", 
            command=self.play_button, width=140, height=40, font=('Impact', 25))
        button.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)

        self.exit = ctk.CTkButton(self.menu_frame, text="Quit", 
                command=self.destroy, width=140, height=40, font=('Impact', 25))
        self.exit.place(relx=0.5, rely=0.50, anchor=ctk.CENTER)

        help=ctk.CTkButton(self.menu_frame, text="Help", 
            command=self.help_button, width=140, height=40, font=('Impact', 25))
        help.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

    # Game:

    def check_player_score(self):
        player_total = self.get_player_total()
        if self.get_player_total() > 21:
            self.frame.destroy()
            self.display_game_status(f"You Busted, your score was {player_total}")
            self.create_new_copy()

    def increment_player_score(self):
        self.player_cards.append(self.get_random_card())
        self.check_player_score()
        self.player_label.configure(text=f'player card:\n {self.add_player_cards()} = {self.get_player_total()}')

    def increment_dealer_score(self):
        dealer_total = self.get_dealer_total()
        while dealer_total < 17:
            self.dealer_cards.append(self.get_random_card())
            dealer_total = self.get_dealer_total()
            self.dealer_label.configure(text=f'dealer card: {dealer_total}')
            time.sleep(0.4)
        self.finish()

    def play_button(self):
        if hasattr(self, "menu_frame"):
            self.menu_frame.destroy()

      
        image = Image.open("back.jpg")
        background_image = ctk.CTkImage(image, size=(700, 500))

        self.dealer_cards = [self.get_random_card()]
        self.player_cards = [self.get_random_card(), self.get_random_card()]
        self.frame = ctk.CTkFrame(self)

        label = ctk.CTkLabel(self.frame, image=background_image, text='')
        label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.player_label = ctk.CTkLabel(self.frame,
    text=f'player card: \n{self.add_player_cards()} = {self.get_player_total()}', 
    font=('Fixedsys', 20))
        pywinstyles.set_opacity(self.player_label, color="#2b2b2b")

        self.dealer_label = ctk.CTkLabel(self.frame, 
                        text=f'dealer card:\n {self.get_dealer_total()}',
                        width=0.1, font=('Fixedsys', 20))
        pywinstyles.set_opacity(self.dealer_label, color="#2b2b2b")
        self.frame.pack(fill="both", expand=1)
        self.player_label.place(relx=0.1, rely = 0.5, anchor=ctk.CENTER)
        self.dealer_label.place(relx= 0.1, rely = 0.03, anchor=ctk.CENTER)
        hit=ctk.CTkButton(self.frame, text="HIT",
 command=self.increment_player_score, width=140, height=40, font=('Impact', 25))
        hit.place(relx= 0.35, rely = 0.5, anchor=ctk.CENTER)
        stand=ctk.CTkButton(self.frame, text='STAND', 
command=self.increment_dealer_score, width=140, height=40, font=('Impact', 25))
        stand.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)
        
        
    #Endgame:
        
    def end_game_buttons(self):
        play_again = ctk.CTkButton(text="Play again", command=self.restart,
            master=self.status_frame, width=140, height=40, font=('Impact', 25))
        play_again.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        done = ctk.CTkButton(text='Quit', command=self.destroy, 
            master=self.status_frame, width=140, height=40, font=('Impact', 25))
        done.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)


    def display_game_status(self, message: str):
        self.frame.destroy()
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(fill="both", expand=1)
        self.status_label = ctk.CTkLabel(self.status_frame, text=message, font=('Fixedsys', 30))
        self.status_label.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)
        self.end_game_buttons()

    def finish(self):
        dealer_total = self.get_dealer_total()
        player_total = self.get_player_total()
        if dealer_total > 21 or player_total > dealer_total:
            self.display_game_status(f"YOU WIN  The Dealer Got {dealer_total}")
        elif dealer_total == player_total:
            self.display_game_status(f'TIE   You and the dealer got {dealer_total}')
        else:
            self.display_game_status(f"YOU LOSE  The Dealer Got {dealer_total}")
        self.create_new_copy()
        self.end_game_buttons()

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
    
    # Help:

    def back(self):
        self.help_frame1.destroy()
        self.help_frame2.destroy()
        self.start()

    
    def help_button(self):
        self.menu_frame.destroy()
        self.help_frame1 = ctk.CTkFrame(self)
        self.help_frame1.pack(fill="both", expand=1)
        text=ctk.CTkLabel(self.help_frame1, 
                          text="The goal of blackjack is simple.\nAll one"
                           " needs to do to win is have a higher \nhand value"
                           " than the dealer, without going over \n21. Players"
                           " are dealt two cards and can then choose \nto “hit”"
                        " (receive additional cards) or “stand” \n(keep their"
                           " current hand).", font=('Fixedsys', 20))
        text.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)
        go_back = ctk.CTkButton(text="Go back", 
                    command=self.back, master=self.help_frame1, width=140, 
                    height=40, font=('Impact', 25))
        go_back.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        page_2=ctk.CTkButton(text='==>', command=self.pag2, 
            master=self.help_frame1, width=70, height=20, font=('Impact', 25) )
        page_2.place(relx=0.9, rely=0.5, anchor=ctk.CENTER)

    def pag2(self):
        self.help_frame1.destroy()
        self.help_frame2 = ctk.CTkFrame(self)
        self.help_frame2.pack(fill='both', expand=1)
        go_back = ctk.CTkButton(text="Go back", 
                    command=self.back, master=self.help_frame2, width=140, 
                    height=40, font=('Impact', 25))
        go_back.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        hit=ctk.CTkLabel(self.help_frame2, text="HIT", font=('Impact', 25))
        hit.place(relx= 0.35, rely = 0.5, anchor=ctk.CENTER)
        stand=ctk.CTkLabel(self.help_frame2, text="STAND", font=('Impact', 25))
        stand.place(relx= 0.65, rely = 0.5, anchor=ctk.CENTER)
        hit_ex=ctk.CTkLabel(text='By clicking the hit button, \nyour hand value'
                ' will increase', font=('Fixedsys', 20), master=self.help_frame2)
        hit_ex.place(relx= 0.3, rely = 0.4, anchor=ctk.CENTER)
        stand_ex=ctk.CTkLabel(text='By clicking the stand button, \n you will '
'not be dealt any more cards', font=('Fixedsys', 20), master=self.help_frame2)
        stand_ex.place(relx= 0.7, rely = 0.4, anchor=ctk.CENTER)
        player_score=ctk.CTkLabel(text="player score:",
                                master=self.help_frame2, font=('Fixedsys', 20))
        player_score.place(relx=0.12, rely = 0.5, anchor=ctk.CENTER)
        dealer_score=ctk.CTkLabel(text='dealer score:\n your' 
"cards will be displayed here",master=self.help_frame2, font=('Fixedsys', 20))
        dealer_score.place(relx= 0.12, rely = 0.03, anchor=ctk.CENTER)

 
if __name__ == "__main__":
    app = App()
    app.mainloop()