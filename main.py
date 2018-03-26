from holdem import Poker
import sys, random

debug = False  # Set to True to see the debug statements
number_of_players = 2

f = open("records.txt","w+")  # Create file of history.


for round in range(0, 1000):
    hand_history = []  # Will keep track of the scores of a hand throughout a game.

    poker = Poker(number_of_players, debug)
    if not poker:
        sys.exit("*** ERROR ***: Invalid number of players. It must be between 2 and 22.")

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
    i=0
    for hand in players_hands:
        text = "Player - "
        for card in hand:
            text += str(card) + "  "
        print(text)
        hand_history.append(str(poker.score(hand)[0]) + ", ")  # Score of just hand.
        i += 1
    print("-----------------------")

    # Gets and prints the community cards
    print("5. Community Cards")
    print("-----------------------")

    # Gets the flop
    card = poker.getFlop()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards = card
    i=0
    for hand in players_hands:
        total = hand + community_cards
        total.sort(key=lambda x: x.value)
        hand_history[i] += str(poker.score(total)[0]) + ", "  # Score of hand + 3 community cards.
        i += 1

    # Gets the Turn
    card = poker.getOne()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend(card)
    i=0
    for hand in players_hands:
        total = hand + community_cards
        total.sort(key=lambda x: x.value)
        hand_history[i] += str(poker.score(total)[0]) + ", "  # Score of hand + 4 community cards.
        i += 1

    # Gets the River
    card = poker.getOne()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend(card)
    i=0
    for hand in players_hands:
        total = hand + community_cards
        total.sort(key=lambda x: x.value)
        hand_history[i] += str(poker.score(total)[0]) + ", "  # Score of hand + 5 community cards.
        hand_history[i] += str(poker.score(community_cards)[0])  # Score of all 5 community cards.
        i += 1

    f.write(hand_history[0] + "\n")
    f.write(hand_history[1] + "\n")
    
    # Displays the Cards
    text = "Community Cards - "
    for card in community_cards:
        text += str(card) + "  "
    print(text)
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

f.close()