'''Blackjack game.'''

import copy
import random
import threading
import time

from PIL import Image

import customtkinter as ctk
import pywinstyles
import cards

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    '''Class has functions that create the foundation for my program.'''


    def __init__(self):
        '''Sets up window for GUI and calls functions to build app.'''
        super().__init__()
        self.geometry('700x500')
        self.title("Blackjack")
        self.minsize(700, 500)
        self.maxsize(700,500)

        self.create_new_copy()
        self.start()

    def create_new_copy(self):
        '''Stores new hard copy of cards data.''' 
        self.copied_cards = copy.deepcopy(cards.data)

    def get_random_card(self):
        '''Picks random card from copy of cards and removes it.'''
        def get_key_from_value(dict, v):
            ''''''
            for key, value in dict.items():
                if value == v:
                    return key
            return None
        random_card = list(random.choice(list(self.copied_cards.items())))[1]
        del(self.copied_cards[get_key_from_value(self.copied_cards, 
                                                 random_card)])
        return random_card

    #Menu:
        
    def start(self):
        '''Displays the main menu with options to play, quit, or view help.'''
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(fill="both", expand=1)

        button = ctk.CTkButton(self.menu_frame, text="Play", 
                               command=self.play_button, width=140, 
                               height=40, font=('Impact', 25))
        button.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)

        self.exit = ctk.CTkButton(self.menu_frame, text="Quit", 
                                  command=self.destroy, width=140, height=40, 
                                  font=('Impact', 25))
        self.exit.place(relx=0.5, rely=0.50, anchor=ctk.CENTER)

        help = ctk.CTkButton(self.menu_frame, text="Help", 
                           command=self.help_button, width=140, height=40,
                           font=('Impact', 25))
        help.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

    # Game:

    def check_player_score(self):
        '''Checks if the player's score exceeds 21 and handles bust 
        scenario.'''
        player_total = self.get_player_total()
        if self.get_player_total() > 21:
            self.frame.destroy()
            self.display_game_status(f"You Busted, your score was. " 
                                     f"{player_total}")
            self.create_new_copy()

    def increment_player_score(self):
        '''Adds a card to player's hand and updates the score.'''
        self.player_cards.append(self.get_random_card())
        self.check_player_score()
        
        if self.player_label.winfo_exists():
            self.player_label.configure(text=(f'player card:\n' 
                                              f'{self.add_player_cards()} =' 
                                              f'{self.get_player_total()}'))

    def dealer_check(self):
        '''Handles dealer's actions, ensuring the dealer draws cards
          appropriately.'''
        dealer_total = self.get_dealer_total()
        while dealer_total < 17:
            dealer_hand_summary = f'dealer card: {dealer_total}'
            self.dealer_cards.append(self.get_random_card())
            dealer_total = self.get_dealer_total()
            self.dealer_label.configure(text=dealer_hand_summary)
            time.sleep(1)
        self.finish()

    def increment_dealer_score(self):
        '''Initiates dealer's turn by checking their score.'''
        if not self.can_stand:
            return
        self.can_stand = False
        threading.Thread(target=self.dealer_check).start() 

    def play_button(self):
        '''Starts the game by dealing initial cards and setting up the game 
        interface.'''
        if hasattr(self, "menu_frame"):
            self.menu_frame.destroy()
        image = Image.open("back.jpg")
        background_image = ctk.CTkImage(image, size=(700, 500))
        self.dealer_cards = [self.get_random_card()]
        self.player_cards = [self.get_random_card(), self.get_random_card()]
        self.frame = ctk.CTkFrame(self)
        self.can_stand = True
        label = ctk.CTkLabel(self.frame, image=background_image, text='')
        label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        player_hand_summary = (f'player card: \n{self.add_player_cards()} ' 
                        f'= {self.get_player_total()}')
        
        self.player_label = ctk.CTkLabel(self.frame, 
                                         text=player_hand_summary, 
                                         font=('Helvetica bold', 25))
        pywinstyles.set_opacity(self.player_label, color="#2b2b2b")

        dealer_score_display = f'dealer card:\n {self.get_dealer_total()}'

        self.dealer_label = ctk.CTkLabel(self.frame, 
                                         text=dealer_score_display, width=0.1, 
                                         font=('Helvetica bold', 25))
        pywinstyles.set_opacity(self.dealer_label, color="#2b2b2b")
        self.frame.pack(fill="both", expand=1)
        self.player_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        self.dealer_label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        self.hit = ctk.CTkButton(self.frame, 
                               text="HIT", 
                               command=self.increment_player_score, width=140, 
                               height=40, font=('Impact', 25))
        self.hit.place(relx=0.35, rely=0.5, anchor=ctk.CENTER)
        pywinstyles.set_opacity(self.hit, color="#2b2b2b")
        self.stand=ctk.CTkButton(self.frame, text='STAND', 
                                 command=self.increment_dealer_score, 
                                 width=140, height=40, font=('Impact', 25))
        self.stand.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)
        pywinstyles.set_opacity(self.stand, color="#2b2b2b")
        
    #Endgame:
        
    def end_game_buttons(self):
        '''Displays buttons for replay, returning to menu, or quitting after
          the game ends.'''
        play_again = ctk.CTkButton(text="Play again", 
                                   command=self.restart_game,
            master = self.status_frame, width=170, height=40, 
            font=('Impact', 25))
        play_again.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        return_menu = ctk.CTkButton(text="Return to menu", 
                                    command=self.restart_main, 
                                    master=self.status_frame, width=140, 
                                    height=40, font=('Impact',25))
        return_menu.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        done = ctk.CTkButton(text='Quit', command=self.destroy, 
                             master=self.status_frame, width=170, height=40, 
                             font=('Impact', 25))
        done.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

    def display_game_status(self, message: str):
        '''Shows the game's outcome message and endgame options.'''

        self.frame.destroy()
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(fill="both", expand=1)
        self.status_label = ctk.CTkLabel(self.status_frame, text=message, 
                                         font=('Helvetica bold', 30))
        self.status_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.end_game_buttons()

    def restart_main(self):
        '''Returns to the main menu from the game or help screen.'''
        self.status_frame.destroy()
        self.start()

    def finish(self):
        '''Determines the winner, displays the result, and resets the deck.'''
        dealer_total = self.get_dealer_total()
        player_total = self.get_player_total()
        if dealer_total > 21 or player_total > dealer_total:
            self.display_game_status(f"YOU WIN  The Dealer Got "
                                     f"{dealer_total}")
        elif dealer_total == player_total:
            self.display_game_status(f'TIE   You and the dealer got'
                                     f' {dealer_total}')
        else:
            self.display_game_status(
                (f"YOU LOSE  The Dealer Got {dealer_total}"))
        self.create_new_copy()
        self.end_game_buttons()

    def restart_game(self):
        '''Restarts the game by reinitializing the game interface.'''
        self.status_frame.destroy()
        self.play_button()

    def get_dealer_total(self):
        '''Calculates the dealer's total score.'''
        total = 0
        for card in self.dealer_cards:
            total = total + card
        return total

    def get_player_total(self):
        '''Calculates the player's total score.'''
        total = 0
        for card in self.player_cards:
            total = total + card
        return total

    def add_player_cards(self):
        '''Returns a string representation of player's cards.'''
        cards = ""
        for card in self.player_cards:
            cards = cards + f' {str(card)}'
        return cards
    
    # Help:

    def back1(self):
        '''Navigates back to the main menu from the first help page.'''
        self.help_frame1.destroy()
        self.start()

    def back2(self):
        '''Navigates back to the main menu from the second help page.'''
        self.help_frame1.destroy()
        self.help_frame2.destroy()
        self.start()
    
    def help_button(self):
        '''Displays the first page of help instructions.'''
        self.menu_frame.destroy()
        self.help_frame1 = ctk.CTkFrame(self)
        self.help_frame1.pack(fill="both", expand=1)
        text = ctk.CTkLabel(self.help_frame1, 
                          text = "The goal of blackjack is simple.\nAll one"
                           " needs to do to win is have a higher \nhand value"
                           " than the dealer, without going over \n21. Players"
                        " are dealt two cards and can then choose \nto “hit”"
                        " (receive additional cards) or “stand” \n(keep their"
                           " current hand).", font=('Helvetica bold', 20))
        text.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)
        go_back = ctk.CTkButton(text="Go back", command=self.back1, 
                                master=self.help_frame1, width=140, height=40, 
                                font=('Impact', 25))
        go_back.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)
        page_2 = ctk.CTkButton(text='==>', command=self.pag2, 
            master=self.help_frame1, width=70, height=20, font=('Impact', 25) )
        page_2.place(relx=0.9, rely=0.5, anchor=ctk.CENTER)

    def pag2(self):
        '''Displays the second page of help instructions.'''
        self.help_frame1.destroy()
        self.help_frame2 = ctk.CTkFrame(self)
        self.help_frame2.pack(fill='both', expand=1)
        image = Image.open("back.jpg")
        background_image = ctk.CTkImage(image, size=(700, 500))
        label = ctk.CTkLabel(self.help_frame2, image=background_image, text='')
        label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        go_back = ctk.CTkButton(text="Go back", 
                    command=self.back2, master=self.help_frame2, width=140, 
                    height=40, font=('Impact', 25))
        go_back.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)
        hit=ctk.CTkLabel(self.help_frame2, text="HIT", font=('Impact', 25))
        hit.place(relx=0.35, rely=0.5, anchor=ctk.CENTER)
        stand = ctk.CTkLabel(self.help_frame2, text="STAND", 
                             font=('Impact', 25))
        stand.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)
        hit_ex = ctk.CTkLabel(text='By clicking the hit button,\nyour hand'
                              ' value will increase', 
                              font=('Helvetica bold', 20), 
                              master=self.help_frame2)
        hit_ex.place(relx=0.3, rely=0.4, anchor=ctk.CENTER)
        stand_ex = ctk.CTkLabel(text='By clicking the stand button, \n you '
                                'will not be dealt any more cards', 
                                font=('Helvetica bold', 20), 
                                master=self.help_frame2)
        stand_ex.place(relx = 0.7, rely=0.4, anchor=ctk.CENTER)
        player_score=ctk.CTkLabel(text="PLAYER SCORE:\n Your "
                                  "cards will be displayed here: ", 
                                  master=self.help_frame2, 
                                  font = ('Helvetica bold', 25))
        player_score.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        dealer_score = ctk.CTkLabel(text="DEALER SCORE:\n dealer's" 
                                    " cards will be displayed here", 
                                    master=self.help_frame2, 
                                    font=('Helvetica bold', 25))
        dealer_score.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        pywinstyles.set_opacity(stand, color="#2b2b2b")
        pywinstyles.set_opacity(hit, color="#2b2b2b")
        pywinstyles.set_opacity(player_score, color="#2b2b2b")
        pywinstyles.set_opacity(dealer_score, color="#2b2b2b")
        pywinstyles.set_opacity(hit_ex, color="#2b2b2b")
        pywinstyles.set_opacity(stand_ex, color="#2b2b2b")
        pywinstyles.set_opacity(go_back, color="#2b2b2b")



if __name__ == "__main__":
    app = App()
    app.mainloop()
    
