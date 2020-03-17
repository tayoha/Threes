import random

# TODO: enable ability to play multiple of the same cards at once
# TODO: enable choice to pick up the pile

# print card visuals using ascii characters
def print_cards(cards, multiple_cards, mysteries):
    suit_names = ['spades', 'diamonds', 'hearts', 'clubs']
    suit_symbols = ['♠', '♦', '♥', '♣']

    lines = [[] for i in range(9)]
    for card in cards:
        if mysteries:
            lines[0].append('┌─────────┐')
            lines[1].append('│░░░░░░░░░│')
            lines[2].append('│░░░░░░░░░│')
            lines[3].append('│░░░░░░░░░│')
            lines[4].append('│░░░░░░░░░│')
            lines[5].append('│░░░░░░░░░│')
            lines[6].append('│░░░░░░░░░│')
            lines[7].append('│░░░░░░░░░│')
            lines[8].append('└─────────┘')
        else:
            if card.value == '10':
                value = card.value
                space = ''
            elif card.value == 'one-eyed jack':
                value = '1J'
                space = ''
            elif card.value == 'two-eyed jack':
                value = '2J'
                space = ''
            elif card.isHighCard():
                value = card.value[0].capitalize()
                space = ' '
            else:
                value = card.value
                space = ' '
            symbol_idx = suit_names.index(card.suit)
            suit_symb = suit_symbols[symbol_idx]

            lines[0].append('┌─────────┐')
            lines[1].append('│{}{}       │'.format(value, space))
            lines[2].append('│         │')
            lines[3].append('│         │')
            lines[4].append('│    {}    │'.format(suit_symb))
            lines[5].append('│         │')
            lines[6].append('│         │')
            lines[7].append('│       {}{}│'.format(space, value))
            lines[8].append('└─────────┘')

    cards_per_row = 5
    num_rows = 0
    row_start_idx = 0
    while row_start_idx < len(lines[0]):
        min_cards = min(5, len(lines[0]) - row_start_idx)
        if multiple_cards:
            one_line = '   '
            for i in range(row_start_idx, row_start_idx + min_cards):
                if i < 10:
                    one_line = one_line + "Card " + str(i) + "      "
                else:
                    one_line = one_line + "Card " + str(i) + "     "
            print(one_line)

        for i in range(9):
            one_line = ''
            for j in range(row_start_idx, row_start_idx + min_cards):
                one_line = one_line + ' ' + lines[i][j]
            print(one_line)
        num_rows += 1
        row_start_idx = num_rows * cards_per_row

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if self.value == '8' or self.value == '10' or self.value == 'one-eyed jack':
            self.burns = True
        else:
            self.burns = False

    def isHighCard(self):
        if self.value == 'one-eyed jack' or self.value == 'two-eyed jack':
            return True
        elif self.value == 'queen':
            return True
        elif self.value == 'king':
            return True
        elif self.value == 'ace':
            return True
        else:
            return False

    def __eq__(self, other):
        if self.value == other.value:
            return True
        elif self.value == 'one-eyed jack' and other.value == 'two-eyed jack':
            return True
        elif self.value == 'two-eyed jack' and other.value == 'one-eyed jack':
            return True
        else:
            return False

    def __lt__(self, other):
        # if the card values are equal, return false
        if self == other:
            return False
        # compare unequal cards
        elif self.isHighCard():
            # compare two high cards
            if other.isHighCard():
                if self.value == 'one-eyed jack' or self.value == 'two-eyed jack':
                    return True
                elif self.value == 'queen':
                    if other.value == 'one-eyed jack' or other.value == 'two-eyed jack':
                        return False
                    else:
                        return True
                elif self.value == 'king':
                    if other.value == 'ace':
                        return True
                    else:
                        return False
                else:
                    return False
            # compare high card with low card
            else:
                return False
        else:
            # compare low card with high card
            if other.isHighCard():
                return True
            # compare two low cards
            else:
                self_int_value = int(self.value)
                other_int_value = int(other.value)
                if self_int_value < other_int_value:
                    return True
                else:
                    return False

class Deck:
    suits = ['hearts', 'clubs', 'spades', 'diamonds']
    values = ['2', '3', '4', '5', '6',\
        '7', '8', '9', '10', 'one-eyed jack',\
            'two-eyed jack', 'queen', 'king', 'ace']
    cards = []

    def __init__(self):
        for suit in self.suits:
            for value in self.values:
                if value == 'one-eyed jack':
                    if suit == 'hearts' or suit == 'spades':
                        new_card = Card(suit, value)
                        self.cards.append(new_card)
                elif value == 'two-eyed jack':
                    if suit == 'clubs' or suit == 'diamonds':
                        new_card = Card(suit, value)
                        self.cards.append(new_card)
                else:
                    new_card = Card(suit, value)
                    self.cards.append(new_card)
        random.shuffle(self.cards)

class Game:
    card_ranks = {
        '2': 12,
        '3': 11,
        '4': 0,
        '5': 1,
        '6': 2,
        '7': 4,
        '8': 5,
        '9': 3,
        '10': 13,
        'one-eyed jack': 7,
        'two-eyed jack': 6,
        'queen': 8,
        'king': 9,
        'ace': 10
    }

    def __init__(self):
        # play pile
        self.pile = []
        # user cards
        self.user_mysteries = []
        self.user_knowns = []
        self.user_hand = []
        # computer cards
        self.computer_mysteries = []
        self.computer_knowns = []
        self.computer_hand = []
        # game deck
        self.deck = Deck()
        # how many cards have been dealt or played (taken from the deck)
        self.index = 0
        # if a seven (or seven and then three) has just been played
        self.in_reverse = False
        # number of the same value cards played in a row
        self.num_repeats = 0
    
    # deal cards
    def deal(self):
        # deal mystery cards
        for _ in range(3):
            self.user_mysteries.append(self.deck.cards[self.index])
            self.index += 1
            self.computer_mysteries.append(self.deck.cards[self.index])
            self.index += 1
        # deal known (upturned) cards
        for _ in range(3):
            self.user_knowns.append(self.deck.cards[self.index])
            self.index += 1
            self.computer_knowns.append(self.deck.cards[self.index])
            self.index += 1
        # deal hand cards
        for _ in range(3):
            self.user_hand.append(self.deck.cards[self.index])
            self.index += 1
            self.computer_hand.append(self.deck.cards[self.index])
            self.index += 1
    
    # handle user trades between hand and knowns
    def handleUserTrades(self):
        print("These are the cards in your hand:")
        #for i, card in enumerate(self.user_hand):
        #    print("Card " + str(i) + ": " + card.value + " of " + card.suit)
        print_cards(self.user_hand, True, False)
        print()
        print("These are your upturned cards:")
        #for i, card in enumerate(self.user_knowns):
        #    print("Card " + str(i) + ": " + card.value + " of " + card.suit)
        print_cards(self.user_knowns, True, False)
        print()
        hand_to_trade = input("Please select the hand card number you would like to trade. If you do not want to trade any cards, please enter 'p'\n")
        while not self.checkHandTrade(hand_to_trade):
            hand_to_trade = input("Please select the hand card number you would like to trade. If you do not want to trade any cards, please enter 'p'.\n")
        if hand_to_trade != 'p':
            hand_trade_num = int(hand_to_trade)
            known_to_trade = input("Please select the upturned card number you would like to trade that hand card for.\n")
            while not self.checkKnownTrade(known_to_trade):
                known_to_trade = input("Please select the upturned card number you would like to trade that hand card for.\n")
            known_trade_num = int(known_to_trade)
            hand_card = self.user_hand[hand_trade_num]
            known_card = self.user_knowns[known_trade_num]
            self.user_hand.pop(hand_trade_num)
            self.user_knowns.pop(known_trade_num)
            self.user_hand.append(known_card)
            self.user_knowns.append(hand_card)
            return True
        else:
            return False
    
    # check that trade card number is valid
    def checkKnownTrade(self, known_to_trade):
        try:
            trade_num = int(known_to_trade)
        except ValueError:
            print("Not a valid card number!\n")
            return False
        if trade_num < 0 or trade_num >= len(self.user_knowns):
            print("Not a valid card number!\n")
            return False
        return True
    
    # checks that trade card number is valid
    def checkHandTrade(self, hand_to_trade):
        if hand_to_trade == 'p':
            return True
        try:
            trade_num = int(hand_to_trade)
        except ValueError:
            print("Not a valid card number!\n")
            return False
        if trade_num < 0 or trade_num >= len(self.user_hand):
            print("Not a valid card number!\n")
            return False
        return True

    # handles user play; handles valid plays, recursions from burning the pile, and pick ups
    def handleUserPlay(self):
        # display previously played card
        hand = False
        knowns = False
        just_burned = False
        if not self.pile:
            prev_card = Card(None, None)
            print("The pile is empty. You can play anything!\n")
        else:
            prev_card = self.pile[len(self.pile) - 1]
            print("Previously played card:")
            cards_arr = []
            cards_arr.append(prev_card)
            print_cards(cards_arr, False, False)
            print()
        # print cards that user can choose from (hand or knowns)
        pick_up = True
        if self.user_hand:
            hand = True
            # display user hand
            print("Your hand:")
            print_cards(self.user_hand, True, False)
            #for i, card in enumerate(self.user_hand):
            #    print("Card " + str(i) + ": " + card.value + " of " + card.suit)
            print()
            # pick up the pile if none of the user's options are playable
            for card in self.user_hand:
                if self.checkPlay(card, prev_card):
                    pick_up = False
        elif self.user_knowns:
            knowns = True
            # display user knowns
            print("Your upturned cards:")
            print_cards(self.user_knowns, True, False)
            #for i, card in enumerate(self.user_knowns):
            #    print("Card " + str(i) + ": " + card.value + " of " + card.suit)
            print()
            # pick up the pile if none of the user's options are playable
            for card in self.user_knowns:
                if self.checkPlay(card, prev_card):
                    pick_up = False
        if (hand or knowns) and pick_up:
            # pick up the pile
            print("Computer played the " + prev_card.value + " of " + prev_card.suit)
            print()
            print("None of your options are playable! Pick up the pile!\n")
            self.pickUp(True, -1)
            return
        if (not hand) and (not knowns):
            # enumerate user unknowns
            print("Your mystery cards:")
            print_cards(self.user_mysteries, True, True)
            #for i in range(len(self.user_mysteries)):
            #    print("Mystery card " + str(i))
            #print()
        # get user input and check for errors
        play = self.getUserInput(hand, knowns)
        if hand:
            played_card = self.user_hand[play]
        elif knowns:
            played_card = self.user_knowns[play]
        else:
            played_card = self.user_mysteries[play]
            cards_arr = []
            cards_arr.append(played_card)
            print("You chose:")
            print_cards(cards_arr, False, False)
            #print("You chose the " + played_card.value + " of " + played_card.suit)
            print()
        # check that play is valid and set number of repeats
        # if user chooses mystery card that is not playable
        if (not hand) and (not knowns):
            if not self.checkPlay(played_card, prev_card):
                print("Not a valid play! Pick up the pile!\n")
                # pick up the pile
                self.pickUp(True, play)
                return
        while not self.checkPlay(played_card, prev_card):
            print("Not a valid play!\n")
            play = self.getUserInput(hand, knowns)
            if hand:
                played_card = self.user_hand[play]
            elif knowns:
                played_card = self.user_knowns[play]
            else:
                played_card = self.user_mysteries[play]
        if played_card == prev_card:
            self.num_repeats += 1
            # if four repeats, burn the pile
            if self.num_repeats == 4:
                self.pile.clear()
                self.in_reverse = False
                just_burned = True
        else:
            self.num_repeats = 1
        # set reversed status
        if played_card.value == '7':
            self.in_reverse = True
        elif played_card.value != '3':
            self.in_reverse = False
        # if burn card is played, burn the pile
        if played_card.burns == True:
            self.pile.clear()
            self.in_reverse = False
            just_burned = True
        # if burn card not played, add it to the pile
        elif not just_burned:
            self.pile.append(played_card)
        # remove card from user's hand
        if hand:
            self.user_hand.pop(play)
            # take card from deck if user has less than 3 cards in hand
            if (self.index < len(self.deck.cards)) and (len(self.user_hand) < 3):
                self.user_hand.append(self.deck.cards[self.index])
                self.index += 1
        elif knowns:
            self.user_knowns.pop(play)
        else:
            self.user_mysteries.pop(play)
        if just_burned and (self.checkForWin() != 'user'):
            print("You burned the pile and get to play again!\n")
            self.handleUserPlay()

    def handleComputerTrades(self):
        first_deck = ''
        first_index = -1
        first_rank = -1
        second_deck = ''
        second_index = -1
        second_rank = -1
        third_deck = ''
        third_index = -1
        third_rank = -1
        knowns_to_trade = []
        hand_to_trade = []
        for i, card in enumerate(self.computer_knowns):
            rank = self.card_ranks[card.value]
            if rank > first_rank:
                first_deck = 'knowns'
                first_index = i
                first_rank = rank
        for i, card in enumerate(self.computer_hand):
            rank = self.card_ranks[card.value]
            if rank > first_rank:
                first_deck = 'hand'
                first_index = i
                first_rank = rank
        for i, card in enumerate(self.computer_knowns):
            rank = self.card_ranks[card.value]
            if ((first_index != i) or (first_deck != 'knowns')) and rank > second_rank:
                second_deck = 'knowns'
                second_index = i
                second_rank = rank
        for i, card in enumerate(self.computer_hand):
            rank = self.card_ranks[card.value]
            if ((first_index != i) or (first_deck != 'hand')) and rank > second_rank:
                second_deck = 'hand'
                second_index = i
                second_rank = rank
        for i, card in enumerate(self.computer_knowns):
            rank = self.card_ranks[card.value]
            if ((first_index != i) or (first_deck != 'knowns')) and \
                ((second_index != i) or (second_deck != 'knowns')) and \
                    rank > third_rank:
                    third_deck = 'knowns'
                    third_index = i
                    third_rank = rank
        for i, card in enumerate(self.computer_hand):
            rank = self.card_ranks[card.value]
            if ((first_index != i) or (first_deck != 'hand')) and \
                ((second_index != i) or (second_deck != 'hand')) and \
                    rank > third_rank:
                    third_deck = 'hand'
                    third_index = i
                    third_rank = rank
        if first_deck == 'hand':
            hand_to_trade.append(first_index)
        if second_deck == 'hand':
            hand_to_trade.append(second_index)
        if third_deck == 'hand':
            hand_to_trade.append(third_index)
        for i in range(len(self.computer_knowns)):
            if ((first_deck != 'knowns') or (first_index != i)) and \
                ((second_deck != 'knowns') or (second_index != i)) and \
                    ((third_deck != 'knowns') or (third_index != i)):
                    knowns_to_trade.append(i)
        for i, val in enumerate(hand_to_trade):
            hand_trade = self.computer_hand[val]
            known_trade = self.computer_knowns[knowns_to_trade[i]]
            self.computer_hand.pop(val)
            self.computer_knowns.pop(knowns_to_trade[i])
            self.computer_hand.append(known_trade)
            self.computer_knowns.append(hand_trade)
    
    # handles computer play; handles valid plays, recursions from burns, and pick ups
    def handleComputerPlay(self):
        hand = False
        knowns = False
        just_burned = False
        # declare previously played card (card on top of the pile)
        if not self.pile:
            prev_card = Card(None, None)
        else:
            prev_card = self.pile[len(self.pile) - 1]
        pick_up = True
        if self.computer_hand:
            print("Computer playing with " + str(len(self.computer_hand)) + " cards in their hand")
            hand = True
            # pick up the pile if none of the computer's options are playable
            for card in self.computer_hand:
                if self.checkPlay(card, prev_card):
                    pick_up = False
        elif self.computer_knowns:
            print("Computer playing with " + str(len(self.computer_knowns)) + " upturned cards")
            knowns = True
            # pick up the pile if none of the computer's options are playable
            for card in self.computer_knowns:
                if self.checkPlay(card, prev_card):
                    pick_up = False
        if (hand or knowns) and pick_up:
            # pick up the pile
            print("Computer picks up the pile!\n")
            self.pickUp(False, -1)
            return
        # play card with the lowest ranking that results in a valid play
        curr_rank = 14
        play_card = Card(None, None)
        card_idx = -1
        strat2 = False
        if hand:
            if not self.user_hand:
                for i, card in enumerate(self.computer_hand):
                    if ((card.value == '7') or card.isHighCard()) and (self.checkPlay(card, prev_card)):
                        strat2 = True
                        card_idx = i
                        play_card = card
                        break
            if strat2 == False:
                for i, card in enumerate(self.computer_hand):
                    new_rank = self.card_ranks[card.value]
                    if (new_rank < curr_rank) and (self.checkPlay(card, prev_card)):
                        curr_rank = new_rank
                        card_idx = i
                        play_card = card
            # remove card from computer's hand
            self.computer_hand.pop(card_idx)
        elif knowns:
            if not self.user_hand:
                for i, card in enumerate(self.computer_knowns):
                    if ((card.value == '7') or card.isHighCard()) and (self.checkPlay(card, prev_card)):
                        strat2 = True
                        card_idx = i
                        play_card = card
                        break
            if strat2 == False:
                for i, card in enumerate(self.computer_knowns):
                    new_rank = self.card_ranks[card.value]
                    if (new_rank < curr_rank) and (self.checkPlay(card, prev_card)):
                        curr_rank = new_rank
                        card_idx = i
                        play_card = card
            # remove card from computer knowns
            self.computer_knowns.pop(card_idx)
        else:
            print("Computer playing with " + str(len(self.computer_mysteries)) + " mystery cards")
            card_idx = random.randint(0, len(self.computer_mysteries) - 1)
            play_card = self.computer_mysteries[card_idx]
            if not self.checkPlay(play_card, prev_card):
                # computer must pick up the pile
                print("Computer picks up the pile!\n")
                self.pickUp(False, card_idx)
                return
            # remove card from computer mysteries
            self.computer_mysteries.pop(card_idx)
        # set number of card repeats
        if play_card == prev_card:
            self.num_repeats += 1
            # if four repeats, burn the pile
            if self.num_repeats == 4:
                self.pile.clear()
                self.in_reverse = False
                just_burned = True
        else:
            self.num_repeats = 1
        # set reversed status
        if play_card.value == '7':
            self.in_reverse = True
        elif play_card.value != '3':
            self.in_reverse = False
        # if burn card is played, burn the pile
        if play_card.burns:
            self.pile.clear()
            self.in_reverse = False
            just_burned = True
        # if burn card not played, add it to the pile
        elif not just_burned:
            self.pile.append(play_card)
        if hand:
            # take card from deck if computer has less than 3 cards in hand
            if (self.index < len(self.deck.cards)) and (len(self.computer_hand) < 3):
                self.computer_hand.append(self.deck.cards[self.index])
                self.index += 1
        if just_burned and (self.checkForWin() != 'computer'):
            print("Computer burned the pile and gets to play again!\n")
            self.handleComputerPlay()
    
    # pick up the pile
    def pickUp(self, user, mystery_index):
        if user:
            self.user_hand.extend(self.pile)
            if mystery_index >= 0:
                self.user_hand.append(self.user_mysteries[mystery_index])
                self.user_mysteries.pop(mystery_index)
        else:
            self.computer_hand.extend(self.pile)
            if mystery_index >= 0:
                self.computer_hand.append(self.computer_mysteries[mystery_index])
                self.computer_mysteries.pop(mystery_index)
        self.pile.clear()
    
    # get user's card choice
    def getUserInput(self, hand, knowns):
        play = 0
        while (True):
            user_input = input("Please enter the card number you want to play! If you'd like to see the computer's upturned cards, enter 'ck'\n")
            try:
                play = int(user_input)
            except ValueError:
                if user_input == 'ck':
                    print("Computer's upturned cards:")
                    print_cards(self.computer_knowns, True, False)
                else:
                    print("Not a valid card number!\n")
                continue
            if hand:   
                if play < 0 or play >= len(self.user_hand):
                    print("Not a valid card number!\n")
                else:
                    return play
            elif knowns:
                if play < 0 or play >= len(self.user_knowns):
                    print("Not a valid card number!\n")
                else:
                    return play
            else:
                if play < 0 or play >= len(self.user_mysteries):
                    print("Not a valid card number!\n")
                else:
                    return play
    
    # check if someone has won
    def checkForWin(self):
        # check if user has won
        if not self.user_hand and not self.user_mysteries:
            return 'user'
        # check if computer has won
        elif not self.computer_hand and not self.computer_mysteries:
            return 'computer'
        else:
            return 'neither'

    # check if a play is valid
    def checkPlay(self, played_card, prev_card):
        if not self.pile:
            return True
        if prev_card.value == '3':
            if len(self.pile) == 1:
                return True
            prev_card = self.pile[len(self.pile) - 2]
        if self.in_reverse:
            if played_card < prev_card:
                return True
            elif played_card == prev_card:
                return True
            elif played_card.value == '10':
                return True
            else:
                return False
        else:
            if prev_card < played_card:
                return True
            elif played_card == prev_card:
                return True
            elif played_card.value == '2':
                return True
            elif played_card.value == '3':
                return True
            elif played_card.value == '10':
                return True
            else:
                return False
    
    # play game
    def playGame(self):
        print("**********ARE YOU READY TO RUMBLEEEEEEEEEEEE?**********")
        print("Dealing cards...\n")
        self.deal()
        self.handleComputerTrades()
        while(self.handleUserTrades()):
            print("Card has been traded\n")
        print("Deciding who goes first...\n")
        first_player = random.randint(0, 1)
        if first_player:
            print("Computer goes first!\n")
            while(True):
                self.handleComputerPlay()
                winner = self.checkForWin()
                if winner != 'neither':
                    print(winner + " wins!")
                    exit(0)
                self.handleUserPlay()
                winner = self.checkForWin()
                if winner != 'neither':
                    print(winner + " wins!")
                    exit(0)
        else:
            print("User goes first!\n")
            while(True):
                self.handleUserPlay()
                winner = self.checkForWin()
                if winner != 'neither':
                    print(winner + " wins!")
                    exit(0)
                self.handleComputerPlay()
                winner = self.checkForWin()
                if winner != 'neither':
                    print(winner + " wins!")
                    exit(0)

def main():
    game = Game()
    game.playGame()

if __name__ == "__main__":
    main()