from deck import Deck
import sys
from io import StringIO

""" Texas Hold Em Poker Game.
This module simulates a poker game. 

Author:
    Omar Shammas <omar.shammas@gmail.com>

Editors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin
"""


class Poker:
    """
    Class holding logic for a Texas Hold Em poker game
    """

    def __init__(self, number_of_players, debug=False):
        """
        Constructor for the Poker class.
        :param number_of_players: The number of players in the game
        :param debug: whether or not to print extra messages
        """
        self.deck = Deck()
        if number_of_players < 2 or number_of_players > 10:
            sys.exit(
                "*** ERROR ***: Invalid number of players."
                " It must be between 2 and 10.")
        self.number_of_players = number_of_players
        # This will print out the debug statements during execution
        self.debug = debug
        # Here is were we would extend and add betting, number of players etc..

    def shuffle(self):
        """
        Shuffles the virtual deck of cards.
        """
        self.deck.shuffle()

    def cut(self, amount):
        """
        Cuts the virtual deck of cards.
        :param amount: the amount to cut the deck by
        :return: The cut amount from the deck
        """
        return self.deck.cut(amount)

    def get_flop(self):
        """
        Gets the first three cards in the deck.
        :return: the cards drawn for the flop
        """
        # Burns 3 cards, then returns the flop
        if not self.deck.deal(3):
            return False
        return self.deck.deal(3)

    def get_one(self):
        """
        Gets the next one card in the deck.
        :return: one card from the deck
        """
        # Burns 1 card, then returns the flop
        if not self.deck.deal(1):
            return False
        return self.deck.deal(1)

    def distribute(self):
        """
        Deals cards out to each player.
        :return: a lists of all the hands, which is a list of cards
        """
        # Each player gets 2 cards when playing by Texas Hold Em rules
        number_of_cards = 2
        if number_of_cards * self.number_of_players > self.deck.cards_left():
            return False

        inplay = []
        for i in range(0, self.number_of_players):
            inplay.append([])

        # Deals each player one card at a time
        # Has greater complexity, but simulates real life better
        for i in range(0, number_of_cards):
            for j in range(0, self.number_of_players):
                inplay[j].append(self.deck.deal(1).pop())

        # Returns a lists of all the hands, which is a list of cards
        return inplay

    @staticmethod
    def name_of_hand(type_of_hand):
        """
        Returns the human readable name of
        a hand based on it's numerical index.

        :param type_of_hand: the numerical index of the hand
        :return: the human readable name of the hand
        """
        if type_of_hand == 0:
            return "High Card"
        elif type_of_hand == 1:
            return "Pair"
        elif type_of_hand == 2:
            return "2 Pair"
        elif type_of_hand == 3:
            return "3 of a Kind"
        elif type_of_hand == 4:
            return "Straight"
        elif type_of_hand == 5:
            return "Flush"
        elif type_of_hand == 6:
            return "Full House"
        elif type_of_hand == 7:
            return "Four of a Kind"
        elif type_of_hand == 8:
            return "Straight Flush"
        else:
            return "Royal Flush"

    @staticmethod
    def score(hand):
        """
        Checks the score of a hand. The higher the score, the better the hand.
        :param hand: The hand to be checked
        :return: the score, and the kicker to be used in the event of a tie
        """

        score = 0
        kicker = []

        # ------------------------------------------------
        # -------------Checking for Pairs-----------------
        # ------------------------------------------------
        pairs = {}
        prev = 0

        ''' Keeps track of all the pairs in a dictionary where 
        the key is the pair's card value and the value is the 
        number occurrences. Eg. If there are 3 Kings -> {"13":3} '''
        for card in hand:
            if prev == card.value:
                key = card.value
                if key in pairs:
                    pairs[key] += 1
                else:
                    pairs[key] = 2
            prev = card.value

        '''Keeps track of the number of pairs and sets. 
        The value of the previous dictionary is the key. 
        Therefore, if there is a pair of 4s and 3 kings -> {"2":1,"3":1} '''
        nop = {}
        for k, v in pairs.items():
            if v in nop:
                nop[v] += 1
            else:
                nop[v] = 1

        ''' Here we determine the best possible combination the hand 
        can be knowing if the hand has a four of a kind, 
        three of a kind, and multiple pairs.'''

        if 4 in nop:  # Has 4 of a kind, assigns the score and the value of the
            score = 7
            kicker = list(pairs.keys())
            # ensures the first kicker is the value of the 4 of a kind
            kicker = [key for key in kicker if pairs[key] == 4]
            key = kicker[0]

            # Gets a list of all the cards remaining
            # once the the 4 of a kind is removed
            temp = [card.value for card in hand if card.value != key]
            # Gets the last card in the list which
            # is the highest remaining card to be used in
            # the event of a tie
            card_value = temp.pop()
            kicker.append(card_value)

            # Returns immediately because this is the best possible hand
            # doesn't check get the best 5 card hand
            # if all users have a 4 of a kind
            return [score, kicker]

        elif 3 in nop:  # Has At least 3 of A Kind
            # Has two 3 of a kind, or a pair and 3 of a kind (full house)
            if nop[3] == 2 or 2 in nop:
                score = 6

                # gets a list of all the pairs and reverses it
                kicker = list(pairs.keys())
                kicker.reverse()
                temp = kicker

                # ensures the first kicker is the value
                # of the highest 3 of a king
                kicker = [key for key in kicker if pairs[key] == 3]

                # if there are two 3 of a kinds,
                # take the higher as the first kicker
                if len(kicker) > 1:
                    kicker.pop()  # removes the lower one from the kicker

                # removes the value of the kicker already in the list
                temp.remove(kicker[0])

                # Gets the highest pair or 3 of kind and adds
                # that to the kickers list
                card_value = temp[0]
                kicker.append(card_value)

            else:  # Has Only 3 of A Kind
                score = 3

                # Gets the value of the 3 of a king
                kicker = list(pairs.keys())
                key = kicker[0]

                # Gets a list of all the cards remaining
                # once the three of a kind is removed
                temp = [card.value for card in hand if card.value != key]

                # Get the 2 last cards in the list which
                # are the 2 highest to be used in the event of a tie
                if len(temp) > 1:
                    card_value = temp.pop()
                    kicker.append(card_value)

                    card_value = temp.pop()
                    kicker.append(card_value)

        elif 2 in nop:  # Has at Least a Pair
            if nop[2] >= 2:  # Has at least 2  or 3 pairs
                score = 2

                kicker = list(
                    pairs.keys())  # Gets the card value of all the pairs
                kicker.reverse()  # reverses the key so highest pairs are used

                # if the user has 3 pairs takes only the highest 2
                if len(kicker) == 3:
                    kicker.pop()

                key1 = kicker[0]
                key2 = kicker[1]

                # Gets a list of all the cards remaining
                # once the the 2 pairs are removed
                temp = [card.value for card in hand if
                        card.value != key1 and card.value != key2]

                # Gets the last card in the list which is
                # the highest remaining card to be used in the event of a tie
                if len(temp) > 0:
                    card_value = temp.pop()
                    kicker.append(card_value)

            else:  # Has only a pair
                score = 1

                kicker = list(pairs.keys())  # Gets the value of the pair
                key = kicker[0]

                # Gets a list of all the cards remaining once pair are removed
                temp = [card.value for card in hand if card.value != key]

                if len(temp) > 2:
                    # Gets the last 3 cards in the list which are the
                    # highest remaining cards which will be used
                    # in the event of a tie
                    card_value = temp.pop()
                    kicker.append(card_value)

                    card_value = temp.pop()
                    kicker.append(card_value)

                    card_value = temp.pop()
                    kicker.append(card_value)

        # ------------------------------------------------
        # ------------Checking for Straight---------------
        # ------------------------------------------------
        # Doesn't check for the ace low straight
        counter = 0
        high = 0
        straight = False

        # Checks to see if the hand contains an ace,
        # and if so starts checking for the straight
        # using an ace low
        if hand[len(hand) - 1].value == 14:
            prev = 1
        else:
            prev = None

        ''' Loops through the hand checking for the straight by comparing the 
         current card to the the previous one and tabulates the number of 
         cards found in a row 
         ***It ignores pairs by skipping over cards that are similar to 
         the previous one*** '''
        for card in hand:
            if prev and card.value == (prev + 1):
                counter += 1
                if counter == 4:  # A straight has been recognized
                    straight = True
                    high = card.value
            # ignores pairs when checking for the straight
            elif prev and prev == card.value:
                pass
            else:
                counter = 0
            prev = card.value

        # If a straight has been realized and the hand
        # has a lower score than a straight
        if (straight or counter >= 4) and score < 4:
            straight = True
            score = 4
            # Records the highest card value in the
            # straight in the event of a tie
            kicker = [high]

        # ------------------------------------------------
        # -------------Checking for Flush-----------------
        # ------------------------------------------------
        flush = False
        total = {}

        ''' Loops through the hand calculating the number of cards of each 
        symbol. The symbol value is the key and for every occurrence the
        counter is incremented'''
        for card in hand:
            key = card.symbol
            if key in total:
                total[key] += 1
            else:
                total[key] = 1

        # key represents the suit of a flush if it is within the hand
        key = -1
        for k, v in total.items():
            if v >= 5:
                key = int(k)

        # If a flush has been realized and the hand
        # has a lower score than a flush
        if key != -1 and score < 5:
            flush = True
            score = 5
            kicker = [card.value for card in hand if card.symbol == key]

        # ------------------------------------------------
        # -----Checking for Straight & Royal Flush--------
        # ------------------------------------------------
        if flush and straight:

            # Doesn't check for the ace low straight
            counter = 0
            high = 0
            straight_flush = False

            # Checks to see if the hand contains an ace,
            #  and if so starts checking for the straight
            # using an ace low
            if kicker[len(kicker) - 1] == 14:
                prev = 1
            else:
                prev = None

            '''Loops through the hand checking for the straight by comparing 
            the current card to the the previous one and tabulates the 
            number of cards found in a row
            ***It ignores pairs by skipping over cards that are similar
            to the previous one*** '''
            for card in kicker:
                if prev and card == (prev + 1):
                    counter += 1
                    if counter >= 4:  # A straight has been recognized
                        straight_flush = True
                        high = card
                # ignores pairs when checking for the straight
                elif prev and prev == card:
                    pass
                else:
                    counter = 0
                prev = card

            # If a straight has been realized and the
            # hand has a lower score than a straight
            if straight_flush:
                if high == 14:
                    score = 9
                else:
                    score = 8
                kicker = [high]
                return [score, kicker]

        if flush:  # if there is only a flush then determines the kickers
            kicker.reverse()

            # This ensures only the top 5 kickers are selected and not more.
            length = len(kicker) - 5
            for i in range(0, length):
                # Pops the last card of the list which is the lowest
                kicker.pop()

        # ------------------------------------------------
        # -------------------High Card--------------------
        # ------------------------------------------------
        # If the score is 0 then high card is the best possible hand
        if score == 0:

            # It will keep track of only the card's value
            kicker = [int(card.value) for card in hand]
            # Reverses the list for easy comparison in the event of a tie
            kicker.reverse()
            # Since the hand is sorted it will pop the two lowest
            # cards position 0, 1 of the list
            kicker.pop()
            kicker.pop()
            '''The reason we reverse then pop is because lists are inefficient 
            at popping from the beginning of the list, but fast at popping from
            the end therefore we reverse the list and then pop the last 
            two elements which will be the two lowest cards in the hand'''

        # Return the score, and the kicker to be used in the event of a tie
        return [score, kicker]

    def determine_score(self, community_cards, players_hands):
        """
        Determines the scores for all players in the game.

        :param community_cards: The cards on the table from
                                which all players may use
        :param players_hands: a list of each player's hand
        :return: the list of scores for each player
        """

        for hand in players_hands:
            hand.extend(community_cards)
            hand.sort(key=lambda x: x.value)

        results = []
        if self.debug:  # Outputs the debug statements
            print("---- Determining Scores----")
        for hand in players_hands:

            overall = self.score(hand)
            results.append([overall[0], overall[1]])  # Stores the results

            if self.debug:  # Outputs the debug statements
                text = "Hand -- "
                for c in hand:
                    text += str(c) + "  "

                kicker = ""
                for c in overall.pop(1):
                    try:
                        kicker += str(c) + "  "
                    except:
                        kicker += str(c) + "  "
                print(text + "Score: " + str(
                    overall.pop(0)) + ", Kicker: " + kicker)

        return results

    def determine_winner(self, results):
        """
        Determines a winner based on the scores of each player.

        :param results: the list of scores each player obtained
        :return:
        """
        if self.debug:
            print("---- Determining Winner----")

        # the highest score if found
        high = 0
        for r in results:
            if r[0] > high:
                high = r[0]

            if self.debug:
                print(r)

        kicker = {}
        counter = 0
        # Only the kickers of the player's hands
        # that are tied for the win are analysed
        for r in results:
            if r[0] == high:
                kicker[counter] = r[1]

            counter += 1

        # if the kickers of multiple players are in
        # the list then we have a tie and need
        # to begin comparing kickers
        if len(kicker) > 1:

            if self.debug:  # Outputs the debug statements
                print("---- Tie Breaker ----")
                print("---- Kicker ----")
                for k, v in kicker.items():
                    print(str(k) + " : " + str(v))

            # Iterate through all the kickers
            # It is important to the number of kickers
            # differ based on the type of hand
            number_of_kickers = len(kicker[list(kicker.keys()).pop()])
            for i in range(0, number_of_kickers):
                high = 0
                for k, v in kicker.items():
                    if v[i] > high:
                        high = v[i]

                # only hands matching the highest kicker remain in
                # the list to be compared
                kicker = {k: v for k, v in kicker.items() if v[i] == high}

                if self.debug:  # Outputs the debug statements of which
                    print("---- " + "Round " + str(i) + " ----")
                    for k in kicker:
                        print(k)

                # if only one the kickers of one player remains
                # that they are the winner
                if len(kicker) <= 1:
                    return list(kicker.keys()).pop()

        else:  # A clear winner was found
            return list(kicker.keys()).pop()

        # A tie occurred, a list of the winners is returned
        return list(kicker.keys())

    @staticmethod
    def convert_knowledge_to_dict(knowledge):
        """
        Converts the string of data for the AI to a dictionary

        :param knowledge: the string of data
        :return: a dictionary version of the passed in data
        """
        my_dict = {}
        s = StringIO(knowledge)
        for line in s:
            data = line.strip().split("|")
            my_dict[data[0].strip()] = data[1]
        return my_dict

    def get_winning_odds(self, scores_to_compare, knowledge):
        """
        Calculates the odds of winning based on previous
        games the AI has played.

        :param scores_to_compare: The current scores the AI has
        :param knowledge: The data of previous games played
        :return: the odds of winning at the current phase of the game
        """
        odds = 0
        total = 0
        scores = str(scores_to_compare).split(",")
        for data, percentage in knowledge.items():
            phases = data.split(",")  # Splits something like 0, 0, 1, 3, 0

            # Check to see if our scores are equal to a line of data.
            # If it is, gather the odds of winning, from knowledge.
            if self.compare_records(scores, phases):
                odds += float(percentage)
                total += 1
        if total == 0:
            print("I'm not sure how this happened!  New data point, possibly?")
        else:
            # This is an average, or the odds we have
            # winning at this current phase of the game.
            return odds/total

    @staticmethod
    def compare_records(record_one, record_two):
        """
        Checks to see if a score is equal to a line of data.

        :param record_one: the first record to compare
        :param record_two: the second record to compare
        :return: True if the records are the same; False if otherwise
        """
        i = 0
        while i < len(record_one) and i < len(record_two):
            if int(record_one[i]) != int(record_two[i]):
                break
            i += 1
        if i == len(record_one or i == len(record_two)):
            return True
        else:
            return False

    @staticmethod
    def check_action(action):
        """
        Checks if the user entered a valid command.

        :param action: the command entered by the user
        :return: True if the command is valid; False if otherwise
        """
        if action.strip().lower() == "hold" \
                or action.strip().lower() == "fold" \
                or action.strip().lower() == "call" \
                or action.strip().lower() == "raise":

            return True
        else:
            return False

    def bidding(self, dealer, player_statuses, highest_bid,
                ai_odds, phase_number):
        """
        Handles the bidding logic for the poker game

        :param dealer: the id of the dealer
        :param player_statuses: the current status
                                of each player {money, status}
        :param highest_bid: the highest bid currently out
        :param ai_odds: the calculated odds of the AI winning
        :param phase_number: which phase the game is currently in
        :return: the new bid amount
        """

        # NOTE: Throughout this, Player 0 will be the AI.
        i = dealer
        all_turns = False  # Will keep track if everyone got at least one turn.
        bid_status = False  # Will keep track if all bids are in.
        end_now = False # Will keep track if the human calls the AIs raise

        # Will keep track of what the highest of the
        # previous round was (for ref).
        prev_round_highest = highest_bid

        # Ratio used to determine how valuable our ai_odds are.
        # *TWEEK THESE FOR BETTER AI*
        ratio = 2 / 5
        if phase_number == 0:
            ratio = 2/5
        elif phase_number == 1:
            if ai_odds >= 80:
                ratio = 5/5
            else:
                ratio = 3/5
        elif phase_number == 2:
            if ai_odds >= 80:
                ratio = 6/5
            else:
                ratio = 2/5
        elif phase_number == 3:
            if ai_odds >= 85:
                ratio = 7/5
            else:
                ratio = 1/5

        # The upper-bound is the "limit" at which we begin
        # to fold (if past phase 0).
        upper_bound = int(ratio*ai_odds)*2
        while True:
            j = (i + 1) % len(player_statuses)
            # If you're still playing this round..
            if player_statuses.get(j)[1] != "fold":
                print("PLAYER " + str(j) + "'s TURN")
                if player_statuses.get(j)[0] < highest_bid:
                    if j != 0:  # Make sure it isn't the AI (who is player 0).
                        action = input(
                            "Highest bid is currently " + str(highest_bid)
                            + ".  Please type fold, call, raise.\n")
                    else:
                        action = \
                            self.decision_tree(highest_bid,
                                               prev_round_highest,
                                               player_statuses.get(j)[0],
                                               upper_bound,
                                               phase_number)[0]
                        print("ACTION! " + action)
                    if self.check_action(action):
                        if action.strip().lower() == "raise":
                            if j != 0:
                                new_value = input("Please enter the numerical "
                                                  "amount you'd like to "
                                                  "raise by.\n")
                                try:
                                    highest_bid += int(new_value)
                                except ValueError:
                                    print("Not a valid number.")
                                    j -= 1
                            else:
                                new_value = \
                                    self.decision_tree(highest_bid,
                                                       prev_round_highest,
                                                       player_statuses.get(j)
                                                       [0],
                                                       upper_bound,
                                                       phase_number)[1]
                                highest_bid += new_value
                                print("By: " + str(new_value))
                            player_statuses.get(j)[0] = highest_bid
                            player_statuses.get(j)[1] = "raise"
                        elif action.strip().lower() == "fold":
                            player_statuses.get(j)[1] = "fold"
                            end_now = True
                        else:
                            player_statuses.get(j)[0] = highest_bid
                            player_statuses.get(j)[1] = "call"
                            end_now = True
                    else:
                        # They entered an invalid command.
                        # I'm not really error checking,
                        # cause' who's got time for that.
                        print("Invalid answer.")
                        player_statuses.get(j)[1] = "error"
                        j -= 1

                else:
                    if j != 0:
                        action = input("You're currently matched "
                                       "with the highest bids ("
                                       + str(highest_bid)
                                       + ").  "
                                         "Would you like to fold, "
                                         "hold, or raise?\n")
                    else:
                        action = \
                            self.decision_tree(highest_bid, prev_round_highest,
                                               player_statuses.get(j)[0],
                                               upper_bound,
                                               phase_number)[0]
                        print("ACTION! " + action)
                    if self.check_action(action):
                        if action.strip().lower() == "raise":
                            if j != 0:
                                new_value = input("Please enter the numerical "
                                                  "amount you'd like to "
                                                  "raise by.\n")
                                try:
                                    highest_bid += int(new_value)
                                except ValueError:
                                    print("Not a valid number.")
                                    j -= 1
                            else:
                                new_value = \
                                    self.decision_tree(highest_bid,
                                                       prev_round_highest,
                                                       player_statuses.get(j)
                                                       [0],
                                                       upper_bound,
                                                       phase_number)[1]
                                highest_bid += new_value
                                print("By: " + str(new_value))
                            player_statuses.get(j)[0] = highest_bid
                            player_statuses.get(j)[1] = "raise"
                        elif action.strip().lower() == "fold":
                            player_statuses.get(j)[1] = "fold"
                        else:
                            player_statuses.get(j)[1] = "hold"
                    else:
                        # They entered an invalid command.
                        print("Invalid answer.")
                        player_statuses.get(j)[1] = "error"
                        j -= 1

            else:
                end_now = True
            k = 0
            for player in player_statuses:
                if player_statuses[player][1] != "fold" \
                        and player_statuses[player][1] != "hold":

                    bid_status = False
                    break
                k += 1
            if k == len(player_statuses):
                bid_status = True
            if not all_turns and j == dealer:
                all_turns = True

            # Check to see if everyone's gotten a chance, and bids are matched.
            if not all_turns or not end_now:
                i = j
            else:
                break
        return highest_bid

    @staticmethod
    def decision_tree(highest_bid, prev_round_highest, my_highest_bid,
                      upper_bound, phase_number):
        """
        The decision tree which the AI will use to make its choices.

        :param highest_bid: The current highest bid
        :param prev_round_highest: The highest bid of the last round
        :param my_highest_bid: The highest the AI has bid
        :param upper_bound: the "limit" at which the AI begins to fold
        :param phase_number: the current phase of the game
        :return: the decision made by the AI to raise, hold, call, or fold
        """
        results = []
        if phase_number == 0:

            # Don't fold on first round, too early to call.
            # If the highest bid is less than the previous round
            # highest plus half of my boundaries,
            # and my highest bid is less than the pot highest, then RAISE!
            if prev_round_highest + int(upper_bound/2) > \
                    highest_bid >= my_highest_bid:

                results.append("raise")
                results.append(prev_round_highest + int(upper_bound/2)
                               - highest_bid)

            # If the previous round highest plus half of my
            # boundaries is less than or equal the highest bid and up
            # caught up to date on the bidding, just HOLD!
            elif prev_round_highest + int(upper_bound/2) <= highest_bid \
                    and my_highest_bid == highest_bid:

                results.append("hold")

            # If the previous round highest plus half of my
            # boundaries is less than or equal to the highest bid,
            #  but I'm not caught up, just CALL!
            elif prev_round_highest + int(upper_bound/2) <= highest_bid \
                    and my_highest_bid < highest_bid:

                results.append("call")

        elif phase_number == 1 or phase_number == 2 or phase_number == 3:

            # If the highest bid is less than the previous round highest
            # plus a third of my boundaries and my highest bid is
            #  less than or equal to the highest bid, then RAISE!
            if prev_round_highest + int(upper_bound/3) > \
                    highest_bid >= my_highest_bid:

                results.append("raise")
                results.append(prev_round_highest + int(upper_bound/3)
                               - highest_bid)

            # If the previous round highest plus a third of my
            # boundaries is less than or equal the highest bid,
            # but also less than the previous round highest plus my upper
            # bound, and my highest bid equal to the highest bid, then HOLD!
            elif prev_round_highest + int(upper_bound/3) <= highest_bid \
                    < prev_round_highest + int(upper_bound) \
                    and my_highest_bid == highest_bid:

                results.append("hold")

            # If the previous round highest plus a third of my
            # boundaries is less than or equal the highest bid,
            # but also less than the previous round highest plus my upper
            # bound, and my highest bid isn't hte highest bid, then CALL!
            elif prev_round_highest + int(upper_bound/3) <= highest_bid \
                    < prev_round_highest + upper_bound \
                    and my_highest_bid < highest_bid:
                results.append("call")

            # Else... just FOLD!  Rip.
            else:
                results.append("fold")
        else:
            results.append("n/a")  # Should be unreachable.
        return results

    @staticmethod
    def print_all_hands(players_hands, editor_mode):
        """
        Prints out each player's hand.

        :param players_hands: the hand of each player
        :param editor_mode: whether or not editor mode is on
        """
        i = 0
        for hand in players_hands:
            text = "Player " + str(i) + " - "
            for card in hand:
                text += str(card) + "  "
            if i != 0 or editor_mode:
                print(text)
            i += 1
