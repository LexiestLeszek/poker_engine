class Card:
    RANKS = (None, '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
    SUITS = {'d': 'Diamonds', 'c': 'Clubs', 's': 'Spades', 'h': 'Hearts'}

    def __init__(self, rank, suit):
        self.rank = self.RANKS[rank]
        self.value = rank
        self.suit = self.SUITS[suit]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value!r}, '{self.suit.lower()[0]}')"

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __hash__(self):
        return hash((self.suit, self.value))

class Deck(list):
    def __init__(self, card_class=Card):
        super().__init__([card_class(v, s) for v in range(1, 14) for s in 'dcsh'])
        self.shuffle()

    def shuffle(self):
        import random
        random.shuffle(self)
        return self

    def draw(self, n):
        return [self.pop(0) for _ in range(n)]

class Hand(list):
    def __init__(self, deck):
        self.deck = deck
        super().__init__(deck.draw(5))
        self.sort()

    def discard(self, indexes):
        self.deck.extend([self.pop(i) for i in indexes])
        return self

    @property
    def score(self):
        vals = [x.value for x in self]
        s = set(vals)
        counts = sorted(zip(map(vals.count, s), s))
        pairs = [self[n:n+2] for n in range(0, len(self)-1)]

        def score_tree(root):
            return tuple([root] + [counts[-x][1] for x in range(1, len(counts)+1)])

        if counts == [(1,1), (1,2), (1,3), (1,4), (1,14)]:
            if all(c.suit == self[0].suit for c in self[1:]):
                return score_tree(8)  # straight flush
            return score_tree(4)  # straight

        if all(c2.value == c1.value+1 for c1, c2 in pairs):
            if all(c.suit == self[0].suit for c in self[1:]):
                return score_tree(8)  # straight flush
        if counts[-1][0] == 4:
            return score_tree(7)  # four of a kind
        if counts[-1][0] == 3:
            if counts[0][0] == 2:
                return score_tree(6)  # full house
        if all(c.suit == self[0].suit for c in self[1:]):
            return score_tree(5)  # flush
        if all(c2.value == c1.value+1 for c1, c2 in pairs):
            return score_tree(4)  # straight
        if counts[-1][0] == 3:
            return score_tree(3)  # three of a kind
        if counts[1][0] == 2:
            return score_tree(2)  # two pair
        if counts[-1][0] == 2:
            return score_tree(1)  # one pair
        return score_tree(0)  # high card

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score

if __name__ == '__main__':
    deck = Deck()

    # Prompt the user for the number of hands they want to play
    num_hands = int(input("Enter the number of hands you want to play: "))
    
    # Create the specified number of hands
    hands = [Hand(deck) for _ in range(num_hands)]
    
    # Print details of each hand and its score
    for i, hand in enumerate(hands, start=1):
        print(f"Hand {i}: {[f'{card}' for card in hand]} Score: {hand.score}")
    
    # Determine and print the winning hand
    import operator
    winner = max(hands, key=lambda hand: hand.score)
    print(f"\nWinner: {[f'{card}' for card in winner]} Score: {winner.score}")

