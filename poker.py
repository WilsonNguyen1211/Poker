import os
import tkinter as tk
import random
from PIL import Image, ImageTk


class PokerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("High Stakes")
        self.canvas = tk.Canvas(self.master, width=800, height=800, bg="light green")
        self.canvas.pack()
        self.deal_button = tk.Button(self.master, text="Deal", command=self.start_game)
        self.deal_button.pack()
        self.check_button = tk.Button(self.master, text="Check", command=self.check, state=tk.DISABLED)
        self.raise_button = tk.Button(self.master, text="Raise", command=self.raise_bet, state=tk.DISABLED)
        self.fold_button = tk.Button(self.master, text="Fold", command=self.fold, state=tk.DISABLED)
        self.players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6"]
        self.deck = []
        self.player_cards = {player: [] for player in self.players}
        self.dealer_index = 0
        self.card_images = {}
        self.current_bet = 0
        self.pot = 0
        self.chips = {player: 1000 for player in self.players}  # Starting chips for each player

        directory = "PNG-cards-1.3"
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                print("Processing image file:", filename)
                split_filename = filename.split("_")
                if len(split_filename) >= 3:
                    value, suit = split_filename[0], split_filename[2].split(".")[0]
                    value = value.lower()  # Ensure lowercase for consistency
                    suit = suit.capitalize()
                    try:
                        image = Image.open(os.path.join(directory, filename))
                        image = image.resize((72, 96))  # Adjust image size as needed
                        self.card_images[(value, suit)] = ImageTk.PhotoImage(image)
                    except Exception as e:
                        print("Error loading image:", e)
                else:
                    print("Invalid filename format:", filename)

        print("Loaded image keys:", self.card_images.keys())

    def start_game(self):
        self.deck = self.generate_deck()
        self.dealer_index = random.randint(0, len(self.players) - 1)
        self.deal_cards()
        self.enable_player_buttons()

    def generate_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return [(value, suit) for suit in suits for value in values]

    def deal_cards(self):
        random.shuffle(self.deck)
        current_player = self.dealer_index
        for _ in range(2):
            for player in self.players:
                self.player_cards[player].append(self.deck.pop())
            current_player = (current_player + 1) % len(self.players)
        self.show_cards()

    def show_cards(self):
        print("Showing cards...")
        self.canvas.delete("all")
        x = 50
        y = 50
        player = "Player 1"
        self.canvas.create_text(x, y, anchor="nw", text=player)
        y += 20
        for card in self.player_cards[player]:
            value, suit = card
            suit_str = suit.lower()
            image_key = (value, suit)  # Ensure consistency in key format
            print("Checking image key:", image_key)
            if image_key in self.card_images:
                image = self.card_images[image_key]
                # Ensure coordinates are within canvas bounds
                if x < self.canvas.winfo_width() and y < self.canvas.winfo_height():
                    self.canvas.create_image(x, y, anchor="nw", image=image)
                    x += 80  # Adjust spacing between cards
                else:
                    print("Image coordinates out of bounds:", x, y)
            else:
                print("Image not found for key:", image_key)
        self.master.update()


def main():
        root = tk.Tk()
        game = PokerGame(root)
        root.mainloop()


if __name__ == "__main__":
    main()
