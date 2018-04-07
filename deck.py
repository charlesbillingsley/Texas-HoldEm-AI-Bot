from random import shuffle

""" Card and Deck Classes.
This module holds classes which represent both cards and decks. 

Author:
    Omar Shammas omar.shammas@gmail.com>

Editors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin
"""


class Card:
    """
    Class to hold specific card data
    """
    def __init__(self, symbol, value):
        """
        The constructor for a card.

        :param symbol: the pictorial symbol of the card
        :param value: the numeric value of the card
        """
        self.symbol = symbol
        self.value = value

    def __str__(self):
        """
        Gets the human readable symbol of the card.

        :return: The human readable symbol of the card
        """
        text = ""
        if self.value < 0:
            return "Joker"
        elif self.value == 11:
            text = "J"
        elif self.value == 12:
            text = "Q"
        elif self.value == 13:
            text = "K"
        elif self.value == 14:
            text = "A"
        else:
            text = str(self.value)

        if self.symbol == 0:  # D-Diamonds
            text += "D"
        elif self.symbol == 1:  # H-Hearts
            text += "H"
        elif self.symbol == 2:  # S-Spade
            text += "S"
        else:  # C-Clubs
            text += "C"

        return text


class Deck:
    """
    Class to hold specific deck data
    """

    def __init__(self, add_jokers=False):
        """
        Initializes the deck, and adds jokers if specified.

        :param add_jokers: whether or not to add jokers to the deck
        """
        self.cards = []
        self.inplay = []
        self.addJokers = add_jokers
        for symbol in range(0, 4):
            for value in range(2, 15):
                self.cards.append(Card(symbol, value))
        if add_jokers:
            self.total_cards = 54
            self.cards.append(Card(-1, -1))
            self.cards.append(Card(-1, -1))
        else:
            self.total_cards = 52

    def shuffle(self):
        """
        Shuffles the deck
        """

        self.cards.extend(self.inplay)
        self.inplay = []
        shuffle(self.cards)

    def cut(self, amount):
        """
        Cuts the deck by the amount specified.

        :param amount: the amount to cut the deck by
        :return: true if the deck was cut successfully and false otherwise
        """

        if not amount or amount < 0 or amount >= len(self.cards):
            # returns false if cutting by a negative
            # number or more cards than in the deck
            return False

        temp = []
        for i in range(0, amount):
            temp.append(self.cards.pop(0))
        self.cards.extend(temp)
        return True

    def deal(self, number_of_cards):
        """
        Deals a specified number of cards.

        :param number_of_cards: the number of cards to deal
        :return: a data dictionary of the cards in play
        """

        if number_of_cards > len(self.cards):
            return False  # Returns false if there are insufficient cards

        inplay = []
        for i in range(0, number_of_cards):
            inplay.append(self.cards.pop(0))

        self.inplay.extend(inplay)
        return inplay

    def cards_left(self):
        """
        Gets the number of cards left in a deck.

        :return: the number of cards left in a deck
        """

        return len(self.cards)
