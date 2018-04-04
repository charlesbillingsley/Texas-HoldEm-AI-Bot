import random
import sys

from holdem import Poker

# TODO fill in documentation
""" Texas Hold Em AI Poker Bot.
This module . 

Example:
    The program can be run by the following command::
        $ python 
Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin
"""


# NOTE: Our CPU will be player 0 throughout the entire program.
debug = False  # Set to True to see the debug statements
number_of_players = 2
dealer = 0  # Dealer will start by default to be player 0.
game_num = 1  # Will keep track of how many games have been played so far.
knowledge = {}
ai_scores = ""

poker = Poker(number_of_players, debug)
if not poker:
    sys.exit(
        "*** ERROR ***: "
        "Invalid number of players. It must be between 2 and 22."
    )


# Check for an input file
if len(sys.argv) == 2:
    # Use knowledge to play.
    with open(sys.argv[1]) as file:
        knowledge = poker.convert_knowledge_to_dict(file.read())
elif len(sys.argv) < 2:
    print("Too few arguments provided")
    print("On EOS Try: python3 main.py input.txt {targetLevel}")
    sys.exit(2)
elif len(sys.argv) > 2:
    print("Too many arguments")
    print("On EOS Try: python3 main.py input.txt {targetLevel}")
    sys.exit(2)

# Time to play the game!
while True:
    print("Starting game #" + str(game_num) + ".  Dealer is player " + str(dealer) + ".  Entry fee is $50 per player.")
    player_statuses = {}
    i = 0
    for i in range(0, number_of_players):
        player_statuses[i] = [50, "hold"]

    highest_bid = 50

    print("1. Shuffling")
    poker.shuffle()

    print("2. Cutting")
    if not poker.cut(random.randint(1, 51)):
        # Cannot cut 0, or the number of cards in the deck
        sys.exit("*** ERROR ***: Invalid amount entered to cut the deck.")

    print("3. Distributing")
    players_hands = poker.distribute()
    if not players_hands:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")

    print("4. Hands")
    print("-----------------------")
    for hand in players_hands:
        text = "Player - "
        for card in hand:
            text += str(card) + "  "
        print(text)
    ai_scores = str(poker.score(players_hands[0])[0])
    chances_of_winning = poker.get_winning_odds(ai_scores, knowledge)
    print("PHASE ZERO ODDS: " + str(chances_of_winning))

    # Bidding
    highest_bid = poker.bidding(dealer, player_statuses, highest_bid)


    print("-----------------------")
    # Gets and prints the community cards
    print("5. Community Cards")
    print("-----------------------")

    # Gets the flop
    card = poker.get_flop()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards = card

    # Re-print hands.
    for hand in players_hands:
        text = "Player - "
        for card in hand:
            text += str(card) + "  "
        print(text)
    # Print community cards.
    text = "Community - "
    for card in community_cards:
        text += str(card) + "  "
    print(text)

    total = players_hands[0] + community_cards
    total.sort(key=lambda x: x.value)
    ai_scores = ai_scores +  "," + str(poker.score(total)[0])
    chances_of_winning = poker.get_winning_odds(ai_scores, knowledge)
    print("PHASE ONE ODDS: " + str(chances_of_winning))

    # Bidding
    highest_bid = poker.bidding(dealer, player_statuses, highest_bid)

    # Gets the Turn
    card = poker.get_one()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend(card)

    # Re-print hands.
    for hand in players_hands:
        text = "Player - "
        for card in hand:
            text += str(card) + "  "
        print(text)
    # Print community cards.
    text = "Community - "
    for card in community_cards:
        text += str(card) + "  "
    print(text)

    total = players_hands[0] + community_cards
    total.sort(key=lambda x: x.value)
    ai_scores = ai_scores + "," + str(poker.score(total)[0])
    chances_of_winning = poker.get_winning_odds(ai_scores, knowledge)
    print("PHASE TWO ODDS: " + str(chances_of_winning))

    # Bidding
    highest_bid = poker.bidding(dealer, player_statuses, highest_bid)

    # Gets the River
    card = poker.get_one()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend(card)

    # Re-print hands.
    for hand in players_hands:
        text = "Player - "
        for card in hand:
            text += str(card) + "  "
        print(text)
    # Print community cards.
    text = "Community - "
    for card in community_cards:
        text += str(card) + "  "
    print(text)

    total = players_hands[0] + community_cards
    total.sort(key=lambda x: x.value)
    ai_scores = ai_scores + "," + str(poker.score(total)[0])
    chances_of_winning = poker.get_winning_odds(ai_scores, knowledge)
    print("PHASE THREE ODDS: " + str(chances_of_winning))
    temp = community_cards
    temp.sort(key=lambda x: x.value)
    if poker.score(total)[0] == poker.score(temp)[0]:
        ai_scores = ai_scores + "," + str(1)
    else:
        ai_scores = ai_scores + "," + str(0)

    chances_of_winning = poker.get_winning_odds(ai_scores, knowledge)
    print("PHASE FOUR ODDS: " + str(chances_of_winning))

    # Bidding
    highest_bid = poker.bidding(dealer, player_statuses, highest_bid)

    print("-----------------------")
    print("6. Determining Score")
    try:
        results = poker.determine_score(community_cards, players_hands)
    except:
        sys.exit("*** ERROR ***: Problem determining the score.")

    print("7. Determining Winner")
    try:
        winner = poker.determine_winner(results)
    except:
        sys.exit("*** ERROR ***: Problem determining the winner.")

    # Checks to see if the hand has ended in tie and displays the appropriate message
    tie = True
    try:
        len(winner)
    except:
        tie = False

    if not tie:
        counter = 0
        print("-------- Winner has Been Determined --------")
        for hand in players_hands:
            if counter == winner:
                text = "Winner ** "
            else:
                text = "Loser  -- "
            for c in hand:
                text += str(c) + "  "

            text += " --- " + poker.name_of_hand(results[counter][0])
            counter += 1
            print(text)
    else:
        counter = 0
        print("--------- Tie has Been Determined --------")
        for hand in players_hands:
            if counter in winner:
                text = "Winner ** "
            else:
                text = "Loser  -- "
            for c in hand:
                text += str(c) + "  "

            text += " --- " + poker.name_of_hand(results[counter][0])
            counter += 1
            print(text)
            break;

    pot = 0
    for player in player_statuses:
        pot += int(player_statuses[player][0])
    print("Pot won: $" + str(pot) + ".")

    action = input("Keep playing? (y/n)\n")
    if action.strip().lower() == "n":
        break
    elif action.strip().lower() != "y":
        print("I don't know what you typed, but we're just going to play again.")

    # Increment stuff.
    dealer = (dealer + 1) % number_of_players
    game_num += 1
