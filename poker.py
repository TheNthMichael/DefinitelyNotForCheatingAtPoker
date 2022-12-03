import copy
import random
from poker_utility import *

# Concept, simulate 1000 poker games with x players, removing your hand from the pot.
# Calculate % wins given your hand given the current knowledge (cards revealed)
global_deck = []
for suit in Card.suit_mapping.keys():
    for rank in Card.rank_mapping.keys():
        global_deck.append(Card(rank, suit))

class Player:
    def __init__(self) -> None:
        self.hand = Hand([])
        self.investment = 0
        self.folded = False

class PokerGame:
    # From the current move, simulate the game up until a winner.
    def __init__(self, n: int) -> None:
        self.deck = copy.deepcopy(global_deck)
        self.n = n
        self.players = {
            i: Player()
            for i in range(n)
        }
        self.me = Player()
        self.rounds_played = 0

    def play_simulated(self, card_a, card_b, revealed):
        """
        Play the game assuming you have been dealt card_a and card_b and that cards in the list
        revealed have already been shown and that the round is the same as the number of revealed cards.
        @returns 1 if you win, 0 if you tie, and -1 if you draw.
        """
        self.deal_simulated(card_a, card_b, revealed)
        rounds_left =  max(5 - len(revealed), 0)
        for i in range(rounds_left):
            card = random.choice(self.deck)
            self.deck.remove(card)
            self.me.hand.add_card(card)
            for player in self.players.keys():
                self.players[player].hand.add_card(card)

        return self.check_if_i_win()

    def play_real(self):
        """
        Play the game as normal with no assumptions, being dealt and revealing random cards.
        @returns 1 if you win, 0 if you tie, and -1 if you draw.
        """
        self.deal_real()
        rounds_left = 5
        for i in range(rounds_left):
            card = random.choice(self.deck)
            self.deck.remove(card)
            self.me.hand.add_card(card)
            for player in self.players.keys():
                self.players[player].hand.add_card(card)
        return self.check_if_i_win()

    def deal_real(self):
        """
        Draw two cards for myself and remove from the deck. Let every other player draw two cards as well.
        """
        card1 = random.choice(self.deck)
        self.me.hand.add_card(card1)
        self.deck.remove(card1)

        card2 = random.choice(self.deck)
        self.me.hand.add_card(card2)
        self.deck.remove(card2)

        # Sample cards
        self.other_players_draw()

    def deal_simulated(self, card_a, card_b, revealed):
        """
        Remove the revealed cards from the deck, add my two cards to my hand, and let the other players draw two cards.
        """
        for card in revealed:
            self.me.hand.add_card(card)
            for player in self.players.keys():
                self.players[player].hand.add_card(card)
            self.deck.remove(card)
        self.me.hand.add_card(card_a)
        self.deck.remove(card_a)
        self.me.hand.add_card(card_b)
        self.deck.remove(card_b)
        
        # Sample cards
        self.other_players_draw()

    def other_players_draw(self):
        """
        For each player, draw two cards and remove them from the deck and add them to the players hand. (minus myself)
        """
        for player in self.players:
            card1 = random.choice(self.deck)
            self.players[player].hand.add_card(card1)
            self.deck.remove(card1)

            card2 = random.choice(self.deck)
            self.players[player].hand.add_card(card2)
            self.deck.remove(card2)

    def check_if_i_win(self):
        """
        @returns 1 on a win, 0 on a tie, and -1 on a draw.
        """
        value, cards = self.me.hand.hand_value()
        tie = False
        for player in self.players.keys():
            other_value, other_cards = self.players[player].hand.hand_value()
            if other_value < value:
                #print(self.players[player].hand.cards)
                return -1
            elif other_value == value:
                my_max_card = max(cards, key=lambda x: x.rank_value)
                other_max_card = max(other_cards, key=lambda x: x.rank_value)
                if other_max_card.rank_value > my_max_card.rank_value:
                    #print(self.players[player].hand.cards)
                    return -1
                elif other_max_card.rank_value == my_max_card.rank_value:
                    if other_max_card.suit_value > my_max_card.suit_value:
                        #print(self.players[player].hand.cards)
                        return -1
                    elif other_max_card.suit_value == my_max_card.suit_value:
                        tie = True
        if tie:
            return 0
        else:
            return 1

wins = 0
draws = 0
losses = 0

N = 10000

for i in range(N):
    if i % (N//10) == 0:
        print(f"{i * 100 / N}% complete...")
    a = PokerGame(1)
    #result = a.play_real()
    result = a.play_simulated(Card("2", "hearts"), Card("4", "spades"), [Card("jack", "clubs")])
    if result == 1:
        wins += 1
    elif result == 0:
        draws += 1
    else:
        losses += 1

print(f"wins: {wins * 100 / N}%, draws: {draws * 100 / N}%, losses: {losses * 100 / N}%")