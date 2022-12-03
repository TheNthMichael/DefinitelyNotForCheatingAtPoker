

def has_royal_flush(cards:list):
    # A,K,Q,J,10 with same suite. Oh this is a regex problem lmao, well kind of.
    # Get cards with same suite
    # for each rank in flush, check if it does not exist.
    # (suite, rank)
    ranks = {
        i: [] for i in range(1,5)
    }
    for card in cards:
        ranks[card[0]].append(card[1])

    ranks_with_5 = [r for r in ranks if len(ranks[r]) >= 5]
    if len(ranks_with_5) == 0:
        return False
    elif len(ranks_with_5) > 1:
        raise "What the fuck?"
    else:
        cards = ranks_with_5[0]
        flush = [1, 11, 12, 13, 10]
        for card in cards:
            if card in flush:
                flush.remove(card)
        if len(flush) == 0:
            return True
    return False

def cards_in_straight(cards: list):
    # Returns all cases of 5 increasing cards.
    # if card includes an ace, append 14 to the cards since both count.
    for card in cards:
        if card[1] == 1:
            cards.append((card[0], 14))
            break
    cards.sort()


def has_straight_flush(cards:list):
    # 5 consecutive cards all with the same suite.
