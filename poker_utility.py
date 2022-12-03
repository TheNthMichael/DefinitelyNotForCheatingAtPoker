

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
        