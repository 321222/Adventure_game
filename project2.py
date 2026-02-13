

import random
import json
from typing import Dict



class Player:
    

    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.score = 0
        self.inventory = []

    def add_item(self, item: str) -> None:
        self.inventory.append(item)
        print(f"Item added: {item}")

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        print(f"Health reduced by {amount}. Current health: {self.health}")

    def add_score(self, points: int) -> None:
        self.score += points

    def is_alive(self) -> bool:
        return self.health > 0

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "health": self.health,
            "score": self.score,
            "inventory": self.inventory
        }

    @staticmethod
    def from_dict(data: Dict):
        player = Player(data["name"])
        player.health = data["health"]
        player.score = data["score"]
        player.inventory = data["inventory"]
        return player



class AdventureGame:

    SAVE_FILE = "savegame.json"

    def __init__(self):
        self.player: Player | None = None

    
    def line(self):
        print("-" * 50)

    def get_choice(self, prompt, options):
        while True:
            choice = input(prompt).strip()
            if choice in options:
                return choice
            print("Invalid input. Try again.")

   
    def save_game(self):
        with open(self.SAVE_FILE, "w") as f:
            json.dump(self.player.to_dict(), f)
        print("Game saved successfully.")

    def load_game(self):
        try:
            with open(self.SAVE_FILE, "r") as f:
                data = json.load(f)
            self.player = Player.from_dict(data)
            print("Game loaded successfully.")
            return True
        except FileNotFoundError:
            print("No saved game found.")
            return False

    
    def random_event(self):
        events = [
            ("You found a potion.", "potion"),
            ("You found a gold coin.", "coin"),
            ("Nothing happened.", None),
        ]

        message, item = random.choice(events)
        print(message)

        if item:
            self.player.add_item(item)
            self.player.add_score(10)

    

    def forest(self):
        self.line()
        print("You enter a dense forest.")
        self.random_event()

        print("1. Follow river")
        print("2. Climb tree")

        choice = self.get_choice("Choose: ", ["1", "2"])

        if choice == "1":
            print("You reach a hidden chest containing treasure.")
            self.player.add_score(50)
            return "win"

        print("You fall from the tree.")
        self.player.take_damage(30)
        return "continue"

    def cave(self):
        self.line()
        print("You enter a dark cave.")

        print("1. Light torch")
        print("2. Walk blindly")

        choice = self.get_choice("Choose: ", ["1", "2"])

        if choice == "1":
            print("Safe passage found.")
            self.player.add_score(20)
            return "continue"

        print("You hit a rock and get injured.")
        self.player.take_damage(40)
        return "continue"

    def ruins(self):
        self.line()
        print("You discover ancient ruins.")

        print("1. Open door")
        print("2. Search outside")

        choice = self.get_choice("Choose: ", ["1", "2"])

        if choice == "1":
            print("Treasure chamber discovered.")
            self.player.add_score(100)
            return "win"

        print("You find nothing useful.")
        return "continue"

  
    def show_status(self):
        self.line()
        print(f"Player: {self.player.name}")
        print(f"Health: {self.player.health}")
        print(f"Score: {self.player.score}")
        print(f"Inventory: {self.player.inventory}")
        self.line()

    def start(self):

        self.line()
        print("ADVENTURE QUEST")
        self.line()

        print("1. New Game")
        print("2. Load Game")

        choice = self.get_choice("Choose: ", ["1", "2"])

        if choice == "2" and self.load_game():
            return

        name = input("Enter your name: ")
        self.player = Player(name)

    def main_loop(self):

        while self.player.is_alive():

            self.show_status()

            print("Choose location:")
            print("1. Forest")
            print("2. Cave")
            print("3. Ruins")
            print("4. Save Game")
            print("5. Quit")

            choice = self.get_choice("Choose: ", ["1", "2", "3", "4", "5"])

            if choice == "1":
                result = self.forest()
            elif choice == "2":
                result = self.cave()
            elif choice == "3":
                result = self.ruins()
            elif choice == "4":
                self.save_game()
                continue
            else:
                break

            if result == "win":
                print("You found the treasure. You win.")
                return

        print("Game Over. You lost all health.")



if __name__ == "__main__":
    game = AdventureGame()
    game.start()
    game.main_loop()
