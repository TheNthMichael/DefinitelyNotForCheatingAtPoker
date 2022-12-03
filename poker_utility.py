class Card:
    suit_mapping = {
        "clubs": 0,
        "diamonds": 1,
        "hearts": 2,
        "spades": 3
    }

    rank_mapping = {
        str(i) for i in range(2,11)
    }
    rank_mapping["ace"] = 14
    rank_mapping["jack"] = 11
    rank_mapping["queen"] = 12
    rank_mapping["king"] = 13

    royals = set(["ace", "king", "queen", "jack", "10"])

    def __init__(self, rank, suit) -> None:
        self._rank = rank
        self._suit = suit

    def is_sequential(self, other):
        """
        Determines if this card is the next sequential card to another card in a straight.
        @param other (Card) - The previous card potentially in a straight.
        @returns True if the card is sequential, False otherwise.
        """
        # Consider both cases for other == ace here.
        if other.rank == "ace":
            return (self.rank_value - other.rank_value) == 1 or (self.rank_value - 1) == 1
        else:
            return (self.rank_value - other.rank_value) == 1

    @property
    def rank_value(self):
        return Card.rank_mapping[self._rank]
    
    @property
    def rank(self):
        return self._rank
    
    @rank.setter
    def rank(self, value):
        self._rank = value

    @property
    def suite_value(self):
        return Card.suit_mapping[self._suit]
    
    @property
    def suite(self):
        return self._suit
    
    @suite.setter
    def suite(self, value):
        self._suite = value

class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards
    
    def add_card(self, card):
        assert type(card) is Card
        self.cards.append(card)
        assert len(self.cards) <= 7
    
    def add_cards(self, cards):
        self.cards.extend(cards)
        assert len(self.cards) <= 7

    def clear_hand(self):
        self.cards = []

    def hand_value(self):
        """
        @returns a tuple containing the order of the hands value and the cards involved. A smaller order means a higher value.
        """
        tests = [
            self.cards_in_royal_flush,
            self.cards_in_straight_flush,
            self.cards_in_four_of_a_kind,
            self.cards_in_full_house,
            self.cards_in_flush,
            self.cards_in_straight,
            self.cards_in_three_of_a_kind,
            self.cards_in_two_pair,
            self.cards_in_pair,
            self.cards_in_high_card
        ]

        for idx, test in enumerate(tests):
            cards = test()
            if len(cards) != 0:
                return (idx, cards)
        # hand must have been empty?
        raise "Error: An empty hands value is undefined." 

    def cards_in_royal_flush(self):
        """
        Get the cards in hand involved with a royal flush.
        @returns a list of Cards involved with a royal flush.
        """
        # There is one suit with more than 5 cards
        cards = [c for c in self.cards_in_flush() if c.rank in Card.royals]
        if len(cards) != 5:
            return []
        return cards

    def cards_in_straight_flush(self):
        """
        Gets the cards involved in a straight flush.
        @returns a list of cards involved in a straight flush.
        """
        flush = self.cards_in_flush()
        hand = self.cards
        
        # temp overwrite hand to test for straight on cards in flush.
        self.cards = flush
        flush = self.cards_in_straight()

        # revert back.
        self.cards = hand
        return flush

    def cards_in_straight(self):
        """
        Gets the cards involved with a straight.
        @returns a list of cards involved with a straight (5 or more sequential cards)
        """
        if len(self.cards) != 5:
            return []
        start = 0
        for i in range(1,len(self.cards)):
            if not self.cards[i].is_sequential(self.cards[i-1]):
                diff = i - 1 - start
                if diff >= 5:
                    return self.cards[start: i-1]
                else:
                    start = i
        if len(self.cards) - start >= 5:
            return self.cards[start:]
        else:
            return []

    def cards_in_flush(self):
        """
        Gets the cards involved with a flush.
        @returns the cards involved with a flush (same suite)
        """
        if len(self.cards) != 5:
            return []

        # Since max hand is 7, only one flush is possible
        suits = {x: [] for x in Card.suit_mapping.keys()}
        for card in self.cards:
            suits[card.suit].append(card)
        suits = [s for s in suits.keys() if len(suits[s]) >= 5]

        if len(suits) > 1:
            raise "Error: invalid count of suites."
        if len(suits) == 0:
            return []
        return suits[0]

    def cards_in_four_of_a_kind(self):
        """
        Gets the cards involved in a four of a kind.
        @returns a list of cards involved in a four of a kind.
        """
        kinds = self.get_card_pairs()
        # 7 cards, impossible to get more than 1x 4 of a kind.
        kinds = [kinds[kind] for kind in kinds.keys() if len(kinds[kind]) == 4]
        if len(kinds) == 0:
            return []
        if len(kinds) > 1:
            raise "Error: invalid kind count."
        return kinds[0]

    def cards_in_full_house(self):
        """
        Gets the cards involved in a full house.
        @returns a list of cards involved in a full house.
        """
        # 3 of a kind and 2 of a kind in one hand
        three_kind = self.cards_in_three_of_a_kind()
        pair = self.cards_in_pair()
        if len(three_kind) != 0 and len(pair) != 0:
            return three_kind.extend(pair)
        else:
            return []

    def cards_in_three_of_a_kind(self):
        """
        Gets the cards involved in a three of a kind. Splits ties based on which 3kind has the higher rank.
        @returns a list of cards involved in a three of a kind splitting ties with the highest rank.
        """
        kinds = self.get_card_pairs()
        # 7 cards, impossible to get more than 1x 4 of a kind.
        kinds = [kinds[kind] for kind in kinds.keys() if len(kinds[kind]) == 3]
        if len(kinds) == 0:
            return []
        if len(kinds) > 2:
            raise "Error: invalid kind count."
        return max(kinds, key=lambda x: x[0].rank_value)

    def cards_in_two_pair(self):
        """
        Gets the cards involved in a two pair. Splits ties based on which two pair has the higher rank.
        @returns a list of cards involved in a two pair splitting ties with the highest rank.
        """
        kinds = self.get_card_pairs()
        # 7 cards, impossible to get more than 1x 4 of a kind.
        kinds = [kinds[kind] for kind in kinds.keys() if len(kinds[kind]) == 2]
        if len(kinds) < 2:
            return []
        if len(kinds) > 3:
            raise "Error: invalid kind count."
        kinds.sort(key=lambda x: x[0].rank_value)
        return kinds[-1].extend(kinds[-2])

    def cards_in_pair(self):
        """
        Gets the cards involved in a pair. Splits ties based on which pair has the higher rank.
        @returns a list of cards involved in a pair splitting ties with the highest rank - doesn't happen in practice since logically this is a two pair.
        """
        kinds = self.get_card_pairs()
        # 7 cards, impossible to get more than 1x 4 of a kind.
        kinds = [kinds[kind] for kind in kinds.keys() if len(kinds[kind]) == 2]
        if len(kinds) == 0:
            return []
        if len(kinds) > 3:
            raise "Error: invalid kind count."
        return max(kinds, key=lambda x: x[0].rank_value)

    def cards_in_high_card(self):
        """
        @returns the card with the highest rank_value.
        """
        return max(self.cards, key=lambda x: x.rank_value)

    def get_card_pairs(self):
        """
        Gets the cards in hand for each rank.
        @returns a dictionary mapping from each rank to a list containing the cards in hand of said rank.
        """
        kinds = {rank: [] for rank in Card.rank_mapping.keys()}
        for card in self.cards:
            kinds[card.rank].append(card)
        return kinds

