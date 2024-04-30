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
                value, suit = filename.split("_")[0], filename.split("_")[2].split(".")[0]
                value = value.capitalize()  # Capitalize the first letter of value
                suit = suit.capitalize()  # Capitalize the first letter of suit
                key = (value, suit)
                print("Loading image with key:", key)
                try:
                    image = Image.open(os.path.join(directory, filename))
                    image = image.resize((72, 96))  # Adjust image size as needed
                    self.card_images[key] = ImageTk.PhotoImage(image)
                except Exception as e:
                    print("Error loading image:", e)

        print("Loaded image keys:", self.card_images.keys())

    def start_game(self):
        self.deck = self.generate_deck()
        self.dealer_index = random.randint(0, len(self.players) - 1)
        self.deal_cards()

    def generate_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return [(value, suit) for suit in suits for value in values]

    def deal_cards(self):
        random.shuffle(self.deck)
        for _ in range(2):
            for player in self.players:
                self.player_cards[player].append(self.deck.pop())
        self.show_cards("Player 1")

    def show_cards(self, player):
        print("Showing cards for", player)
        self.canvas.delete("all")
        x = 50
        y = 50
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
