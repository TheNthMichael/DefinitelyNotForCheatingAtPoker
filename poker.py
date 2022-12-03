import copy
import random

# Concept, simulate 1000 poker games with x players, removing your hand from the pot.
# Calculate % wins given your hand given the current knowledge (cards revealed)
suite = [1,2,3,4]
ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]

global_deck = []

for i in suite:
    for j in ranks:
        global_deck.append((i,j))

class Player:
    def __init__(self) -> None:
        self.cards = []
        self.folded = False

class PokerGame:
    # From the current move, simulate the game up until a winner.
    def __init__(self, n, revealed: list, card_a, card_b) -> None:
        self.deck = copy.deepcopy(global_deck)
        self.n = n
        self.players = {
            i: Player()
            for i in range(n)
        }
        self.revealed = revealed
        self.card_a = card_a
        self.card_b = card_b
        self.rounds_played = 0

    def play(self):
        self.deal()
        rounds_left = max(len(self.revealed) - 5, 0)
        for i in range(rounds_left):
            card = random.choice(self.deck)
            self.deck.remove(card)
            self.revealed.append(card)

    def deal(self):
        # Remove known cards
        for card in self.revealed:
            self.deck.remove(card)
        self.deck.remove(self.card_a)
        self.deck.remove(self.card_b)
        
        # Sample cards
        self.other_players_draw()

    def other_players_draw(self):
        for player in self.players:
            card1 = random.choice(self.deck)
            self.players[player].cards.append(card1)
            self.deck.remove(card1)

            card2 = random.choice(self.deck)
            self.players[player].cards.append(card1)
            self.deck.remove(card2)

    def get_max_combo(self, cards):
        