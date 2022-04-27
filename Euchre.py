import random
import time
from termcolor import colored


# This is the card game Euchre. Rules: https://bicyclecards.com/how-to-play/euchre/
# Cards used are 9 up to Ace. 'Going alone' for a round is not a feature of this script
# Human player is player 1. Player 3 is your teammate

# Define our classes: Card, Deck, Player & Team


class Card:
    def __init__(self, suit, rank, point, left_bower, left_bower_suit, owner, display, card_string, clincher=False):
        self.suit = suit
        self.rank = rank
        self.point = point
        self.left_bower = left_bower
        self.left_bower_suit = left_bower_suit
        self.owner = owner
        self.display = display
        self.card_string = card_string
        self.clincher = clincher

    def show(self):
        if self.suit == 'Clubs':
            self.display = colored(f'{self.rank} ♣ Clubs', 'grey', 'on_white')
        elif self.suit == 'Spades':
            self.display = colored(f'{self.rank} ♠ Spades', 'grey', 'on_white')
        elif self.suit == 'Hearts':
            self.display = colored(f'{self.rank} ♥ Hearts', 'red', 'on_grey')
        elif self.suit == 'Diamonds':
            self.display = colored(f'{self.rank} ♦ Diamonds', 'red', 'on_grey')

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_point(self):
        # This is used to determine the best card played each trick
        return self.point

    def get_clincher(self):
        # Boolean so computer players know which cards are clincher
        return self.clincher

    def is_left_bower(self):
        # Boolean that is true for the jack that 'switches suit' each round and becomes a clincher
        return self.left_bower

    def suit_left_bower(self):
        # The effective suit of each card. The only change from the original suit is the odd jack card aka left bower
        # This counts as the other suit of the same color (diamonds and hearts are red, spades and clubs are black)
        return self.left_bower_suit


class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.build()

    def __len__(self):
        return len(self)  # Shows how many cards are in deck. This should be 24 for 9 -> Ace

    def show(self):
        for c in self.cards:
            c.show()

    def build(self):
        # This creates the deck of 24 cards
        for suit in self.suits:  # for every suit and rank, creates a card that is added to cards list
            for rank in self.ranks:
                card = Card(suit, rank, point=0, clincher=False, left_bower=False, left_bower_suit=suit, owner=None,
                            display='', card_string=f'{rank} of {suit}')
                self.cards.append(card)

    def destroy(self):
        # This empties out the cards in the deck. Used at the end of each round to help simulate reshuffling
        self.cards = []

    def deal_cards(self, player_name):
        # Deals 5 random cards to each player
        for i in range(5):
            random_card = random.choice(self.cards)
            self.cards.remove(random_card)
            player_name.hand.append(random_card)
        return player_name.hand

    def flip_card(self):
        # Flips one card on the table. Players have option to tell dealer to pick up this card to make its suit clincher
        # This is called after all players have 5 cards
        flipped = random.choice(self.cards)
        return flipped


class Player:
    def __init__(self, number):
        self.number = number
        self.name = 'Player' + str(number)
        self.hand = []
        self.card_values = [0, 0, 0, 0]
        self.tricks_won = 0

    def evaluate_cards(self):
        # This function is run before clincher suit is called
        # It assigns points based on the cards in the players hand
        # It gives points to each suit based on how strong the players hand would be if that suit were clincher
        # This exists so the computer players can use strategy to decide whether to call clincher and which suit to call

        self.card_values = [0, 0, 0, 0]  # [Clubs, Diamonds, Hearts, Spades]
        point_dict_clubs = {'Jack of Clubs': 15, 'Jack of Spades': 13, 'Ace of Clubs': 11, 'King of Clubs': 10,
                            'Queen of Clubs': 9, '10 of Clubs': 8, '9 of Clubs': 7,
                            'Ace of Diamonds': 4, 'Ace of Hearts': 4, 'Ace of Spades': 4}
        point_dict_diamonds = {'Jack of Diamonds': 15, 'Jack of Hearts': 13, 'Ace of Diamonds': 11,
                               'King of Diamonds': 10, 'Queen of Diamonds': 9, '10 of Diamonds': 8, '9 of Diamonds': 7,
                               'Ace of Clubs': 4, 'Ace of Hearts': 4, 'Ace of Spades': 4}
        point_dict_hearts = {'Jack of Hearts': 15, 'Jack of Diamonds': 13, 'Ace of Hearts': 11, 'King of Hearts': 10,
                             'Queen of Hearts': 9, '10 of Hearts': 8, '9 of Hearts': 7,
                             'Ace of Clubs': 4, 'Ace of Diamonds': 4, 'Ace of Spades': 4}
        point_dict_spades = {'Jack of Spades': 15, 'Jack of Clubs': 13, 'Ace of Spades': 11, 'King of Spades': 10,
                             'Queen of Spades': 9, '10 of Spades': 8, '9 of Spades': 7,
                             'Ace of Clubs': 4, 'Ace of Diamonds': 4, 'Ace of Hearts': 4}
        for c in self.hand:
            if c.card_string in point_dict_clubs:
                self.card_values[0] += point_dict_clubs.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_diamonds:
                self.card_values[1] += point_dict_diamonds.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_hearts:
                self.card_values[2] += point_dict_hearts.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_spades:
                self.card_values[3] += point_dict_spades.get(c.card_string)
        return self.card_values


class Team:
    # Teams are made up of 2 players. In real Euchre, teammates sit across the table from each other. So odd players
    # make up team1, and even numbered players make up team2
    # The human user is on team1 with Player3
    def __init__(self, player_a, player_b, points, tricks):
        self.player_a = player_a
        self.player_b = player_b
        self.points = points
        self.tricks = tricks


# This variable determines how aggressive a computer player will be when calling suit.
# If their hand has 30+ points in a given suit, they will call it clincher
points_to_call_suit = 30

# Create the 4 players and the deck out of the 24 possible cards.
# Randomly assign 5 cards to each player (no repeats)
# Flip one remaining card

d = Deck()
d.show()

player_1 = Player(1)
player_2 = Player(2)
player_3 = Player(3)
player_4 = Player(4)

team_1 = Team(player_1, player_3, 0, 0)
team_2 = Team(player_2, player_4, 0, 0)


def user_order_up_card(p, flipped_c, suit, dealer_):
    # This allows the user to tell a computer player whether to pick up the flipped card and call that suit clincher

    options = ['y', 'n']
    print('Your hand is: \n')
    for c in p.hand:
        print(c.display)
        time.sleep(0.3)
    time.sleep(0.5)
    while True:
        try:
            does_user_order_card = input(
                f'\n{dealer_.name} is the dealer. Would you like them to pick up the flipped card? (y/n)')
            if does_user_order_card.lower() not in options:
                raise TypeError
            if does_user_order_card.lower() == 'y':
                suit = flipped_c.suit
                discard = None
                ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
                dealer_.hand.append(flipped_c)
                for rank in ranks:
                    for each_card in dealer_.hand:
                        if each_card.get_rank() == rank and each_card.get_suit() != suit:
                            discard = each_card
                            break
                    else:
                        continue
                    break
                try:
                    dealer_.hand.pop(dealer_.hand.index(discard))
                except ValueError:
                    len_hand = len(dealer_.hand)
                    dealer_.hand.pop(random.randint(0, len_hand))
                was_suit_picked = True
                caller = p

            elif does_user_order_card.lower() == 'n':
                was_suit_picked = False
                caller = None
            else:
                print('Invalid Input. Please enter y or n next time')
            return p, suit, was_suit_picked, dealer_, caller
        except TypeError:
            print('Invalid input. Please enter y or n to determine whether the dealer should pick up the card')


def user_pick_up_card(p, flipped_c, suit):
    # This allows the user to pick up the flipped card and call that suit clincher.
    # This is only run when the user is the dealer for that round (only dealer may pick up card)

    print('\n')
    options = ['y', 'n']
    while True:
        try:
            for c in p.hand:
                print(c.display)
                time.sleep(0.3)
            time.sleep(0.7)
            does_user_take_card = input(
                '\nYou are the dealer. Would you like to pick up the flipped card? Please enter y or n: ')
            if does_user_take_card.lower() not in options:
                raise TypeError
            num_cards_in_hand = len(p.hand)
            if does_user_take_card.lower() == 'y':
                card_to_remove = int(input(
                                        f'\nPlease enter the position (1-{num_cards_in_hand}) of the card you want to '
                                        f'remove from your hand: ')) - 1
                p.hand.remove(p.hand[card_to_remove])
                p.hand.append(flipped_c)
                suit = suit.join(flipped_c.get_suit())
                was_card_picked_up = True
                caller = p
                return p, suit, was_card_picked_up, caller

            elif does_user_take_card.lower() == 'n':
                was_card_picked_up = False
                caller = None
                return p, suit, was_card_picked_up, caller
        except TypeError:
            print('Please enter y or n to indicate whether you want to pick up the card!')
        else:
            break


def user_choose_call_suit(p, flipped_c, suit):
    # This allows the user to determine clincher for that round after everyone has passed on the flipped card

    was_suit_declared = False
    user_call_options = ['y', 'n']
    suit_options = ['c', 'd', 'h', 's']
    suit_options.pop(suit_options.index(flipped_c.suit[0].lower()))
    # This removes the suit of the flipped card. cant be clincher
    print('\n')
    for c in p.hand:
        print(c.display)
    while True:
        try:
            does_user_call = input('\nYour hand is above. Would you like to call clincher suit? (y/n):')
            if does_user_call[0].lower() not in user_call_options:
                raise ValueError
            elif does_user_call[0].lower() == 'y':
                was_suit_declared = True
                caller = p
                called_suit = input(f'\nPlease enter the first letter of the suit you\'d like to call '
                                    f'({suit_options[0]}/{suit_options[1]}/{suit_options[2]}): ')
                suit_letter = called_suit[0].lower()
                if suit_letter not in suit_options:
                    if suit_letter == flipped_c.suit[0].lower():
                        print(f'\nYou may not call {flipped_c.suit} because it was turned down as the flipped card.')
                    else:
                        pass
                    raise ValueError
                else:
                    pass
                if suit_letter == 'c':
                    suit = suit.join('Clubs')
                elif suit_letter == 'd':
                    suit = suit.join('Diamonds')
                elif suit_letter == 'h':
                    suit = suit.join('Hearts')
                elif suit_letter == 's':
                    suit = suit.join('Spades')
                else:
                    print('Please enter a valid letter next time. Options are c for clubs, d for diamonds, '
                          'h for hearts and s for spades')
            elif does_user_call[0].lower() == 'n':
                was_suit_declared = False
                caller = None
                pass
            else:
                print('PLease enter a valid option. y or n')
            return suit, was_suit_declared, caller
        except ValueError:
            print('Please enter a valid option')


def user_must_call_suit(p, suit, flipped_c):
    # This forces the user to call clincher for that round. This function only runs when all players refuse to order up
    # the flipped card, and all computer player refuse to call clincher suit on the next round.
    # This only happens when the user is dealer. Rule is called 'Stick to Dealer' & forces dealer to call clincher

    was_suit_declared = False
    print('\n')
    for c in p.hand:
        print(c.display)
    while True:
        try:
            called_suit = input(
                f'''\nYour hand is above and you can call any suit except {flipped_c.get_suit()}.\nYou must call suit. 
                Please enter the first letter of the suit to call (c/d/h/s): ''')
            if called_suit[0].lower() == flipped_c.get_suit()[0].lower():
                print('You entered the suit that was turned down...Please enter a different suit')
                raise ValueError
            else:
                if called_suit.lower() == 'c':
                    suit = suit.join('Clubs')
                    was_suit_declared = True
                elif called_suit.lower() == 'd':
                    suit = suit.join('Diamonds')
                    was_suit_declared = True
                elif called_suit.lower() == 'h':
                    suit = suit.join('Hearts')
                    was_suit_declared = True
                elif called_suit.lower() == 's':
                    suit = suit.join('Spades')
                    was_suit_declared = True
                else:
                    raise ValueError
            caller = p
            return suit, was_suit_declared, caller
        except ValueError:
            print('Please enter a valid suit')


def user_drop_card(dealer_, flipped_c, caller_):
    # This is run when the computer orders the user to pick up the flipped card. Only happens when user is dealer
    # User adds the card to their hand, then chooses one to discard
    # This is called by the computer_order_up_card function, but only when user is dealer

    dealer_.hand.append(flipped_c)
    num_cards = len(dealer_.hand)

    while True:
        try:
            print('\nYour hand is:\n')
            for c in dealer_.hand:
                print(c.display)
            card_index_to_drop = int(input(
                f'\n{caller_.name} has ordered you to pick up the {flipped_c.display}.\n\n'
                f'Please enter the position 1-{num_cards} of the card to discard: ')) - 1

            if card_index_to_drop in list(range(num_cards)):
                dealer_.hand.pop(card_index_to_drop)
                return dealer_
            else:
                raise ValueError
        except ValueError:
            print(f'\nInvalid Input. Please enter a number between 1-{num_cards}\n')


def computer_order_up_card(p, flipped_c, suit, dealer_, pts_to_call_suit):
    # This function gives the computer the option to tell the dealer to pick up the card.
    # If the user is the dealer, it calls the user_drop_card function. Otherwise, it will discard a non-clincher
    # Card of low rank from the dealers had
    # Aggressiveness of computer ordering up card depends on points_to_call_suit integer
    discard = None
    ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']

    suit_dict = {'Clubs': 0, 'Diamonds': 1, 'Hearts': 2, 'Spades': 3}
    suit_idx = suit_dict.get(flipped_c.suit)
    if p.card_values[suit_idx] >= pts_to_call_suit:
        suit = flipped_c.suit
        was_card_picked_up = True
        caller = p
        if dealer_.name == 'Player1':  # If player1 is the dealer, then the user has option of which card to drop
            dealer_ = user_drop_card(dealer_, flipped_c, p)
        else:  # If players 2-4 are dealer, make dealer choose lowest off-suit card to drop
            dealer_.hand.append(flipped_c)
            for rank in ranks:
                for each_card in dealer_.hand:
                    if each_card.get_rank() == rank and each_card.left_bower_suit != suit:
                        discard = each_card
                        break
                else:
                    continue
                break
            try:
                dealer_.hand.pop(p.hand.index(discard))
            except ValueError:  # This happens if dealer has no non-clincher cards
                len_hand = len(dealer_.hand)
                dealer_.hand.pop(random.randint(0, len_hand - 1))

    else:
        was_card_picked_up = False
        caller = None
        print(f'{p.name}: Pass')
    return p, suit, was_card_picked_up, dealer_, caller


def computer_pick_up_card(p, flipped_c, suit, pts_to_call_suit):
    # This adds the point value of the flipped card to the appropriate suit points for the cards in the dealers hand
    # Ex. if the 9 of Diamonds is flipped, the dealers hand gains 7 points for diamonds card_values
    # Dealer will pick up the card if that suit has >= points in card_values[] than the points_to_call_suit variable
    discard = None
    was_card_picked_up = False
    caller = None

    ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
    card_value_flipped_clincher = {'Jack': 15, 'Ace': 11, 'King': 10, 'Queen': 9, '10': 8, '9': 7}

    suit_dict = {'Clubs': 0, 'Diamonds': 1, 'Hearts': 2, 'Spades': 3}
    suit_idx = suit_dict.get(flipped_c.suit)
    p.card_values[suit_idx] += card_value_flipped_clincher.get(flipped_c.rank)
    if p.card_values[suit_idx] >= pts_to_call_suit:
        suit = flipped_c.suit
        p.hand.append(flipped_c)
        was_card_picked_up = True
        caller = p
        for rank in ranks:
            for each_card in p.hand:
                if each_card.get_rank() == rank and each_card.get_suit() != suit:
                    discard = each_card
                    break
            else:
                continue
            break
        try:
            p.hand.pop(p.hand.index(discard))
        except ValueError:  # If the dealer has no non-clincher cards to discard, discard a random one
            len_hand = len(p.hand)
            p.hand.pop(random.randint(0, len_hand))
    else:
        print(f'{p.name}: Pass')

    return p, suit, was_card_picked_up, caller


def computer_choose_call_suit(p, flipped_c, suit, pts_to_call_suit):
    # This will give the computer the option to call suit after everyone has refused to call the suit of flipped card
    # It will only call suit if the player has more pts in that suit than the variable points_to_call_suit

    was_suit_declared = False
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    best_suit_idx = p.card_values.index(max(p.card_values))
    if p.card_values[best_suit_idx] < pts_to_call_suit:
        caller = None
        print(f'{p.name}: Pass')
        pass
    elif suits[best_suit_idx] == flipped_c.suit:  # Comp may not call suit that was turned down earlier
        p.card_values[best_suit_idx] = 0
        second_best_suit_idx = p.card_values.index(max(p.card_values))
        if p.card_values[second_best_suit_idx] < pts_to_call_suit:
            caller = None
            print(f'{p.name}: Pass')
            pass
        else:
            was_suit_declared = True
            caller = p
            suit = suits[second_best_suit_idx]
    else:
        was_suit_declared = True
        caller = p
        suit = suits[best_suit_idx]
    return suit, was_suit_declared, caller


def computer_must_call_suit(p, flipped_c, suit):
    # This forces the computer to call a suit after everyone has turned down the flipped card and then refused
    # to call suit. Only happens when comp is dealer. If the best suit for comp matched that of the flipped card,
    # comp card_values for that suit is set to 0.

    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    best_suit_idx = p.card_values.index(max(p.card_values))
    was_suit_declared = True
    caller = p
    if suits[best_suit_idx] == flipped_c.get_suit():
        p.card_values[best_suit_idx] = 0
        second_best_suit_idx = p.card_values.index(max(p.card_values))
        suit = suits[second_best_suit_idx]
    else:
        suit = suits[best_suit_idx]

    return suit, was_suit_declared, caller


def user_lead_card(hand):
    # This allows the user to play any card as the first card of the trick

    num_cards_in_hand = len(hand)
    print('\nYour hand is: ')
    for c in hand:
        print(c.display)
    while True:
        try:
            card_index_to_play = int(
                input(f'\nPlease enter the position (1-{num_cards_in_hand}) of the card you would like to lead: ')) - 1
            lead = hand[card_index_to_play]
        except (ValueError, IndexError):
            print(f'\nSorry, that is not a valid number. Please enter a number: 1-{num_cards_in_hand} to choose.')
        else:
            break

    hand.pop(card_index_to_play)
    return lead, hand


def computer_lead_card(hand):
    # This allows the computer player to play any card as the first card of the trick
    # Comp will always play a card of the highest rank - even if it is a clincher (legal play, but not always strategic)

    lead = None
    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9']

    if len(hand) == 1:
        lead = hand[0]
        hand.pop(hand.index(lead))
    else:
        for rank in ranks:
            for each_card in hand:
                if each_card.get_rank() == rank and not each_card.clincher:
                    lead = each_card
                    hand.pop(hand.index(lead))
                    break
            else:
                continue
            break

        if not lead:  # If we didn't pick a card to lead earlier (this happens when comp. only has clinchers)
            clincher_ranks = ['Jack', 'Ace', 'King', 'Queen', '10', '9']
            for c_rank in clincher_ranks:
                for clincher in hand:
                    if clincher.get_rank() == c_rank:
                        lead = clincher
                        hand.pop(hand.index(lead))
                        break
                else:
                    continue
                break

    return lead, hand


def assign_left_bower(best, hand):
    # This will assign the 'Correct' suit to the odd jack. it always acts as the other suit of the same color
    # Other names for odd jack: left bower

    for c in hand:
        if best == 'Clubs' and c.card_string == 'Jack of Spades':
            c.left_bower = True
            c.left_bower_suit = 'Clubs'

        elif best == 'Diamonds' and c.card_string == 'Jack of Hearts':
            c.left_bower = True
            c.left_bower_suit = 'Diamonds'

        elif best == 'Hearts' and c.card_string == 'Jack of Diamonds':
            c.left_bower = True
            c.left_bower_suit = 'Hearts'

        elif best == 'Spades' and c.card_string == 'Jack of Clubs':
            c.left_bower = True
            c.left_bower_suit = 'Spades'
        else:
            pass
    return hand


def assign_points(hand, best, lead):
    # This is called at the start of every round after the 1st card is played
    # This gives point values to every card that could potentially win the round (clincher > suit of 1st card)
    # This will act as a ranking system to determine which was the best card played that round

    c_clincher = {'Jack of Clubs': 13, 'Jack of Spades': 12, 'Ace of Clubs': 11, 'King of Clubs': 10,
                  'Queen of Clubs': 9, '10 of Clubs': 8, '9 of Clubs': 7}
    d_clincher = {'Jack of Diamonds': 13, 'Jack of Hearts': 12, 'Ace of Diamonds': 11, 'King of Diamonds': 10,
                  'Queen of Diamonds': 9, '10 of Diamonds': 8, '9 of Diamonds': 7}
    h_clincher = {'Jack of Hearts': 13, 'Jack of Diamonds': 12, 'Ace of Hearts': 11, 'King of Hearts': 10,
                  'Queen of Hearts': 9, '10 of Hearts': 8, '9 of Hearts': 7}
    s_clincher = {'Jack of Spades': 13, 'Jack of Clubs': 12, 'Ace of Spades': 11, 'King of Spades': 10,
                  'Queen of Spades': 9, '10 of Spades': 8, '9 of Spades': 7}
    c_lead = {'Ace of Clubs': 6, 'King of Clubs': 5, 'Queen of Clubs': 4, 'Jack of Clubs': 3,
              '10 of Clubs': 2, '9 of Clubs': 1}
    d_lead = {'Ace of Diamonds': 6, 'King of Diamonds': 5, 'Queen of Diamonds': 4, 'Jack of Diamonds': 3,
              '10 of Diamonds': 2, '9 of Diamonds': 1}
    h_lead = {'Ace of Hearts': 6, 'King of Hearts': 5, 'Queen of Hearts': 4, 'Jack of Hearts': 3,
              '10 of Hearts': 2, '9 of Hearts': 1}
    s_lead = {'Ace of Spades': 6, 'King of Spades': 5, 'Queen of Spades': 4, 'Jack of Spades': 3,
              '10 of Spades': 2, '9 of Spades': 1}

    if best == 'Clubs':
        if lead.left_bower_suit == 'Spades':
            s_lead.pop('Jack of Spades')
            c_clincher.update(s_lead)
        elif lead.left_bower_suit == 'Hearts':
            c_clincher.update(h_lead)
        elif lead.left_bower_suit == 'Diamonds':
            c_clincher.update(d_lead)
        elif lead.left_bower_suit == 'Clubs':
            pass
        lead.point = c_clincher.get(lead.card_string, 0)
        for crd in hand:
            crd.point = c_clincher.get(crd.card_string, 0)

    elif best == 'Diamonds':
        if lead.left_bower_suit == 'Clubs':
            d_clincher.update(c_lead)
        elif lead.left_bower_suit == 'Diamonds':
            pass
        elif lead.left_bower_suit == 'Hearts':
            h_lead.pop('Jack of Hearts')
            d_clincher.update(h_lead)
        elif lead.left_bower_suit == 'Spades':
            d_clincher.update(s_lead)
        lead.point = d_clincher.get(lead.card_string, 0)
        for crd in hand:
            crd.point = d_clincher.get(crd.card_string, 0)

    elif best == 'Hearts':
        if lead.left_bower_suit == 'Clubs':
            h_clincher.update(c_lead)
        elif lead.left_bower_suit == 'Diamonds':
            d_lead.pop('Jack of Diamonds')
            h_clincher.update(d_lead)
        elif lead.left_bower_suit == 'Hearts':
            pass
        elif lead.left_bower_suit == 'Spades':
            h_clincher.update(s_lead)
        lead.point = h_clincher.get(lead.card_string, 0)
        for crd in hand:
            crd.point = h_clincher.get(crd.card_string, 0)

    elif best == 'Spades':
        if lead.left_bower_suit == 'Clubs':
            c_lead.pop('Jack of Clubs')
            s_clincher.update(c_lead)
        elif lead.left_bower_suit == 'Diamonds':
            s_clincher.update(d_lead)
        elif lead.left_bower_suit == 'Hearts':
            s_clincher.update(h_lead)
        elif lead.left_bower_suit == 'Spades':
            pass
        lead.point = s_clincher.get(lead.card_string, 0)
        for crd in hand:
            crd.point = s_clincher.get(crd.card_string, 0)
    return hand


def assign_clincher(best, hand):
    for c in hand:
        if c.get_suit() == best or c.is_left_bower():
            c.clincher = True
        else:
            pass
    return hand


def computer_follow_suit(lead_c, hand, played):
    if len(hand) == 1:
        card_to_play = hand[0]
    else:
        currently_winning_card = played[0]
        cards_to_follow_suit = {}
        for c in hand:
            if c.left_bower_suit == lead_c.left_bower_suit:  # If the card in hand has the same suit as card lead then..
                cards_to_follow_suit[c] = c.point  # Add that card to dict of cards that follow suit
            else:
                pass

        for played_card in played:  # This looks at all cards played already and determines which is winning so far
            if played_card.point > currently_winning_card.point:
                currently_winning_card = played_card

        best_card = max(cards_to_follow_suit, key=cards_to_follow_suit.get)
        worst_card = min(cards_to_follow_suit, key=cards_to_follow_suit.get)

        if best_card.point > currently_winning_card.point:
            if len(played) == 3 and played.index(currently_winning_card) == 1:
                card_to_play = worst_card
            else:
                card_to_play = best_card
        else:
            card_to_play = worst_card
    hand.pop(hand.index(card_to_play))

    return card_to_play, hand


def computer_play_clincher(hand, played, winner, calling_player):
    clinchers = {}
    currently_winning_card = played[0]
    players_yet_to_play = ['1', '2', '3', '4']

    for played_card in played:
        if played_card.point > currently_winning_card.point:
            currently_winning_card = played_card
        players_yet_to_play.pop(players_yet_to_play.index(str(played_card.owner)))

    for card in hand:  # this makes a dictionary of the clinchers in the computers hand. This is used to
        if card.get_clincher:  # decide which card to play later
            clinchers[card] = card.point

    card_to_play = max(clinchers, key=clinchers.get)

    for card in played:
        winning_card = played[0]
        if card.point > winning_card.point:
            winning_card = card

    if card_to_play.point < winning_card.point:  # If the computer's clincher cannot win the round,
        raise ValueError  # then raise an error and discard a bad card instead

    elif len(played) == 3 and played.index(winning_card) == 1:  # If the computer is last to play and teammate is
        raise ValueError  # winning, raise ValueError to discard bad card

    elif len(clinchers) > 1 and calling_player.number not in players_yet_to_play:  # If comp has >1 clincher and
        lowest_winning_card = card_to_play  # the player who called suit has yet to play, play lowest clincher
        for c in clinchers:  # that will still take the lead in the trick
            if winning_card.point < c.point < lowest_winning_card.point:
                lowest_winning_card = c
        card_to_play = lowest_winning_card
        hand.pop(hand.index(card_to_play))
    else:
        hand.pop(hand.index(card_to_play))
    return card_to_play, hand


def computer_discard_bad_card(hand, suit):
    # This makes the computer discard their lowest rank, non-clincher card
    # If all cards are clincher, the lowest clincher will be played
    bad_card = None
    ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
    clincher_ranks = ['9', '10', 'Queen', 'King', 'Ace', 'Jack']

    all_cards_are_clincher = True
    for each_card in hand:
        if not each_card.clincher:
            all_cards_are_clincher = False
    if all_cards_are_clincher:
        for rank in clincher_ranks:
            for each_card in hand:
                if each_card.get_rank() == rank:
                    bad_card = each_card
                    break
            else:
                continue
            break
    else:
        for rank in ranks:
            for each_card in hand:
                if each_card.get_rank() == rank and each_card.left_bower_suit != suit:
                    bad_card = each_card
                    break
            else:
                continue
            break
    hand.pop(hand.index(bad_card))
    return bad_card, hand


def user_follow_suit(lead_c, hand, played):
    # This allows the user to follow suit of the first card played
    # User must follow suit, per rules of Euchre
    # If user cannot follow suit, ValueError is raised, and user is allowed to choose any card
    legal_cards = []
    if lead_c.left_bower_suit == 'Clubs':
        for c in hand:
            if c.left_bower_suit == 'Clubs':
                legal_cards.append(c)
            else:
                pass
    if lead_c.left_bower_suit == 'Diamonds':
        for c in hand:
            if c.left_bower_suit == 'Diamonds':
                legal_cards.append(c)
            else:
                pass
    if lead_c.left_bower_suit == 'Hearts':
        for c in hand:
            if c.left_bower_suit == 'Hearts':
                legal_cards.append(c)
            else:
                pass
    if lead_c.left_bower_suit == 'Spades':
        for c in hand:
            if c.left_bower_suit == 'Spades':
                legal_cards.append(c)
            else:
                pass

    if len(legal_cards) == 0:
        raise ValueError

    print('\nThe card(s) you can play to follow suit are: \n')
    for l in legal_cards:
        print(l.display)
    while True:
        try:
            legal_card_play_index = int(input('\nPlease enter the position of the card you\'d like to play: ')) - 1
            card_to_play = legal_cards[legal_card_play_index]
        except (ValueError, IndexError):
            print(f'Please enter a valid number between 1-{len(legal_cards)} to follow suit with that card')
        else:
            break
    hand.pop(hand.index(card_to_play))
    return card_to_play, hand


def user_choose_card(hand):
    # This allows user to play any card in their hand
    while True:
        try:
            card_play_index = int(input('\nPlease enter the position of the card to play: ')) - 1
            card_to_play = hand[card_play_index]
            hand.pop(hand.index(card_to_play))
            return card_to_play, hand
        except (ValueError, IndexError):
            print('Invalid input. Please enter the card position: ')
        else:
            break


def determine_winning_trick_so_far(played):
    # This function determines which played is currently winning the trick, as in who has played the best card so far
    # Used to help the computer make strategic decisions about which card to play

    points_scored = {}
    for pc in played:
        points_scored[pc.owner] = pc.point
    player_in_lead = max(points_scored, key=points_scored.get)
    return player_in_lead


def assign_point_trick_winner(winning_play, play1, play2, play3, play4):
    #  Keeps track of the numbers of tricks each player has won
    if winning_play == 1:
        play1.tricks_won += 1
    elif winning_play == 2:
        play2.tricks_won += 1
    elif winning_play == 3:
        play3.tricks_won += 1
    elif winning_play == 4:
        play4.tricks_won += 1
    return play1, play2, play3, play4


def determine_trick_winner(played):
    # After all 4 cards are played, this function finds the one with the highest point value. that card wins the trick
    # and the winning player (owner of that card) is returned
    cards_points = {}
    for c in played:
        cards_points[c] = c.point
    print('\n')
    for crd in cards_points:
        print(f'{crd.display} (P{crd.owner})')
        time.sleep(.4)
    time.sleep(1)
    winning_card = max(cards_points, key=cards_points.get)
    winner = winning_card.owner
    print(f'\nPlayer{winner} won with the {winning_card.display}')
    return winner


def play_trick(p1, p2, p3, p4, round_leader, best_suit, caller):
    # The user can now play a card by choosing the index (1-5) of the card to play. That suit is lead
    # and must be followed by other players
    print(colored(f'\nClincher: {best_suit} ({caller.name})', 'green'))

    p1.hand = assign_clincher(best_suit, p1.hand)
    p2.hand = assign_clincher(best_suit, p2.hand)
    p3.hand = assign_clincher(best_suit, p3.hand)
    p4.hand = assign_clincher(best_suit, p4.hand)

    if round_leader == 1:
        lead_card, p1.hand = user_lead_card(p1.hand)
    elif round_leader == 2:
        lead_card, p2.hand = computer_lead_card(p2.hand)
    elif round_leader == 3:
        lead_card, p3.hand = computer_lead_card(p3.hand)
    elif round_leader == 4:
        lead_card, p4.hand = computer_lead_card(p4.hand)

    played_cards = [lead_card]
    lead_suit = lead_card.left_bower_suit

    p1.hand = assign_points(p1.hand, best_suit, lead_card)
    p2.hand = assign_points(p2.hand, best_suit, lead_card)
    p3.hand = assign_points(p3.hand, best_suit, lead_card)
    p4.hand = assign_points(p4.hand, best_suit, lead_card)

    time.sleep(1.75)
    if round_leader == 1:
        player_in_lead = 1
        try:
            p2_card, p2.hand = computer_follow_suit(lead_card, p2.hand, played_cards)
        except ValueError:
            try:
                p2_card, p2.hand = computer_play_clincher(p2.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p2_card, p2.hand = computer_discard_bad_card(p2.hand, best_suit)

        played_cards.append(p2_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

        try:
            p3_card, p3.hand = computer_follow_suit(lead_card, p3.hand, played_cards)
        except ValueError:
            try:
                if player_in_lead == 1:
                    raise ValueError
                else:
                    p3_card, p3.hand = computer_play_clincher(p3.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p3_card, p3.hand = computer_discard_bad_card(p3.hand, best_suit)

        played_cards.append(p3_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

        try:
            p4_card, p4.hand = computer_follow_suit(lead_card, p4.hand, played_cards)
        except ValueError:
            try:
                if player_in_lead == 2:
                    raise ValueError
                else:
                    p4_card, p4.hand = computer_play_clincher(p4.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p4_card, p4.hand = computer_discard_bad_card(p4.hand, best_suit)

        played_cards.append(p4_card)

    elif round_leader == 2:
        player_in_lead = 2
        try:
            p3_card, p3.hand = computer_follow_suit(lead_card, p3.hand, played_cards)
        except ValueError:
            try:
                p3_card, p3.hand = computer_play_clincher(p3.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p3_card, p3.hand = computer_discard_bad_card(p3.hand, best_suit)

        played_cards.append(p3_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

        try:
            p4_card, p4.hand = computer_follow_suit(lead_card, p4.hand, played_cards)
        except ValueError:
            try:
                if player_in_lead == 2:
                    raise ValueError
                else:
                    p4_card, p4.hand = computer_play_clincher(p4.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p4_card, p4.hand = computer_discard_bad_card(p4.hand, best_suit)

        played_cards.append(p4_card)

        try:
            print('\nThe cards played so far are: ')
            for pc in played_cards:
                time.sleep(.4)
                print(f'{pc.display} (P{pc.owner})')
            time.sleep(1)
            print('\nYour hand is: \n')
            for c in p1.hand:
                print(c.display)
            p1_card, p1.hand = user_follow_suit(lead_card, p1.hand, played_cards)
        except ValueError:
            p1_card, p1.hand = user_choose_card(p1.hand)

        played_cards.append(p1_card)

    elif round_leader == 3:
        player_in_lead = 3
        try:
            p4_card, p4.hand = computer_follow_suit(lead_card, p4.hand, played_cards)
        except ValueError:
            try:
                p4_card, p4.hand = computer_play_clincher(p4.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p4_card, p4.hand = computer_discard_bad_card(p4.hand, best_suit)

        played_cards.append(p4_card)

        try:
            print('\nThe cards played so far are: ')
            for pc in played_cards:
                time.sleep(.4)
                print(f'{pc.display} (P{pc.owner})')
            time.sleep(1)
            print('\nYour hand is: \n')
            for c in p1.hand:
                print(c.display)
            p1_card, p1.hand = user_follow_suit(lead_card, p1.hand, played_cards)
        except ValueError:
            p1_card, p1.hand = user_choose_card(p1.hand)

        played_cards.append(p1_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

        try:
            p2_card, p2.hand = computer_follow_suit(lead_card, p2.hand, played_cards)
        except ValueError:
            try:
                if player_in_lead == 4:
                    raise ValueError
                else:
                    p2_card, p2.hand = computer_play_clincher(p2.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p2_card, p2.hand = computer_discard_bad_card(p2.hand, best_suit)

        played_cards.append(p2_card)

    elif round_leader == 4:
        player_in_lead = 4
        try:
            print('\nThe cards played so far are: ')
            for pc in played_cards:
                time.sleep(.4)
                print(f'{pc.display} (P{pc.owner})')
            time.sleep(1)
            print('\nYour hand is: \n')
            for c in p1.hand:
                print(c.display)

            p1_card, p1.hand = user_follow_suit(lead_card, p1.hand, played_cards)
        except ValueError:
            p1_card, p1.hand = user_choose_card(p1.hand)

        played_cards.append(p1_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

        try:
            p2_card, p2.hand = computer_follow_suit(lead_card, p2.hand, played_cards)
        except ValueError:
            try:
                if player_in_lead == 4:
                    raise ValueError
                else:
                    p2_card, p2.hand = computer_play_clincher(p2.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p2_card, p2.hand = computer_discard_bad_card(p2.hand, best_suit)

        played_cards.append(p2_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

        try:
            p3_card, p3.hand = computer_follow_suit(lead_card, p3.hand, played_cards)
        except ValueError:
            try:
                if player_in_lead == 1:
                    raise ValueError
                else:
                    p3_card, p3.hand = computer_play_clincher(p3.hand, played_cards, player_in_lead, caller)
            except ValueError:
                p3_card, p3.hand = computer_discard_bad_card(p3.hand, best_suit)

        played_cards.append(p3_card)

    winning_player = determine_trick_winner(played_cards)

    p1, p2, p3, p4 = assign_point_trick_winner(winning_player, p1, p2, p3, p4)

    print(colored(f'\nRound Score: {p1.tricks_won + p3.tricks_won}-{p2.tricks_won + p4.tricks_won}', 'green'))

    return p1, p2, p3, p4, winning_player


def play_round(team1, team2, player1, player2, player3, player4, deck, dlr_index, dlr, ldr_index):
    #  This function runs each round of Euchre and will be looped over until enough points are scored (11 by 1 team)
    deck.show()
    deck.deal_cards(player1)
    deck.deal_cards(player2)
    deck.deal_cards(player3)
    deck.deal_cards(player4)

    player1.tricks_won = 0
    player2.tricks_won = 0
    player3.tricks_won = 0
    player4.tricks_won = 0

    flipped_card = deck.flip_card()

    print(f'\nDealer: {dlr.name}\nFlipped: {flipped_card.display}\n')
    time.sleep(1.5)

    best_suit = ''

    player1.evaluate_cards()
    player2.evaluate_cards()
    player3.evaluate_cards()
    player4.evaluate_cards()

    # The person to the left of the dealer always has the first option whether to
    # Pick up the flipped card
    was_suit_picked = False

    if dlr_index == 4:
        while True:
            player1, best_suit, was_suit_picked, player4, calling_player = \
                user_order_up_card(player1, flipped_card, best_suit, player4)
            if was_suit_picked:
                break
            player2, best_suit, was_suit_picked, player4, calling_player = \
                computer_order_up_card(player2, flipped_card, best_suit, player4, points_to_call_suit)
            if was_suit_picked:
                break
            player3, best_suit, was_suit_picked, player4, calling_player = \
                computer_order_up_card(player3, flipped_card, best_suit, player4, points_to_call_suit)
            if was_suit_picked:
                break
            player4, best_suit, was_suit_picked, calling_player = \
                computer_pick_up_card(player4, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = user_choose_call_suit(player1, flipped_card, best_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player2, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player3, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = computer_must_call_suit(player4, flipped_card, best_suit)
            if was_suit_picked:
                break

    elif dlr_index == 1:
        while True:
            player2, best_suit, was_suit_picked, player1, calling_player = \
                computer_order_up_card(player2, flipped_card, best_suit, player1, points_to_call_suit)
            if was_suit_picked:
                break
            player3, best_suit, was_suit_picked, player1, calling_player = \
                computer_order_up_card(player3, flipped_card, best_suit, player1, points_to_call_suit)
            if was_suit_picked:
                break
            player4, best_suit, was_suit_picked, player1, calling_player = \
                computer_order_up_card(player4, flipped_card, best_suit, player1, points_to_call_suit)
            if was_suit_picked:
                break
            player1, best_suit, was_suit_picked, calling_player = user_pick_up_card(player1, flipped_card, best_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player2, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player3, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player4, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = user_must_call_suit(player1, best_suit, flipped_card)
            if was_suit_picked:
                break

    elif dlr_index == 2:
        while True:
            player3, best_suit, was_suit_picked, player2, calling_player = \
                computer_order_up_card(player3, flipped_card, best_suit, player2, points_to_call_suit)
            if was_suit_picked:
                break
            player4, best_suit, was_suit_picked, player2, calling_player = \
                computer_order_up_card(player4, flipped_card, best_suit, player2, points_to_call_suit)
            if was_suit_picked:
                break
            player1, best_suit, was_suit_picked, player2, calling_player = \
                user_order_up_card(player1, flipped_card, best_suit, player2)
            if was_suit_picked:
                break
            player2, best_suit, was_suit_picked, calling_player = \
                computer_pick_up_card(player2, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player3, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player4, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = user_choose_call_suit(player1, flipped_card, best_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = computer_must_call_suit(player2, flipped_card, best_suit)
            if was_suit_picked:
                break

    elif dlr_index == 3:
        while True:
            player4, best_suit, was_suit_picked, player3, calling_player = \
                computer_order_up_card(player4, flipped_card, best_suit, player3, points_to_call_suit)
            if was_suit_picked:
                break
            player1, best_suit, was_suit_picked, player3, calling_player = \
                user_order_up_card(player1, flipped_card, best_suit, player3)
            if was_suit_picked:
                break
            player2, best_suit, was_suit_picked, player3, calling_player = \
                computer_order_up_card(player2, flipped_card, best_suit, player3, points_to_call_suit)
            if was_suit_picked:
                break
            player3, best_suit, was_suit_picked, calling_player = \
                computer_pick_up_card(player3, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player4, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = user_choose_call_suit(player1, flipped_card, best_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = \
                computer_choose_call_suit(player2, flipped_card, best_suit, points_to_call_suit)
            if was_suit_picked:
                break
            best_suit, was_suit_picked, calling_player = computer_must_call_suit(player3, flipped_card, best_suit)
            if was_suit_picked:
                break

    for c in player1.hand:
        c.owner = 1
    for c in player2.hand:
        c.owner = 2
    for c in player3.hand:
        c.owner = 3
    for c in player4.hand:
        c.owner = 4

    print(colored(f'{calling_player.name}: {best_suit} is clincher suit.', 'green'))
    time.sleep(1.3)

    player1.hand = assign_left_bower(best_suit, player1.hand)
    player2.hand = assign_left_bower(best_suit, player2.hand)
    player3.hand = assign_left_bower(best_suit, player3.hand)
    player4.hand = assign_left_bower(best_suit, player4.hand)

    player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player)
    player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player)
    player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player)
    player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player)
    player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player)

    team1.tricks = player1.tricks_won + player3.tricks_won
    team2.tricks = player2.tricks_won + player4.tricks_won

    if team1.tricks > team2.tricks:
        if calling_player.name == 'Player2' or calling_player.name == 'Player4' or team1.tricks == 5:
            team1.points += 2
            print(f'\nYou win! Team 1 won, taking {team1.tricks} tricks. Your team scored 2 points!')
        else:
            team1.points += 1
            print(f'\nYou win! Team 1 won, taking {team1.tricks} tricks. Your team scored 1 point!')
    elif team2.tricks > team1.tricks:
        if calling_player.name == 'Player1' or calling_player.name == 'Player3' or team2.tricks == 5:
            team2.points += 2
            print(f'\nYou lost this round! Team 2 won, taking {team2.tricks} tricks. They scored 2 points!')
        else:
            team2.points += 1
            print(f'\nYou lost this round! Team 2 won, taking {team2.tricks} tricks. They scored 1 point!')

    time.sleep(2.5)
    print(f'\nThe game score is {team1.points}-{team2.points}')
    time.sleep(2.5)

    return team1, team2, player1, player2, player3, player4


players = {player_1: 1, player_2: 2, player_3: 3, player_4: 4}
dealer, dealer_index = random.choice(list(players.items()))
leader_index = (dealer_index % 4) + 1

while team_1.points < 11 and team_2.points < 11:
    team_1, team_2, player_1, player_2, player_3, player_4 = play_round(team_1, team_2, player_1, player_2, player_3,
                                                                        player_4, d, dealer_index, dealer, leader_index)
    dealer_index = dealer_index % 4 + 1
    leader_index = leader_index % 4 + 1
    dealer = list(players.keys())[list(players.values()).index(dealer_index)]
    d.destroy()
    d.build()
    if team_1.points >= 11:
        print(f'You win the game! Final Score: {team_1.points}-{team_2.points}')
        break
    elif team_2.points >= 11:
        print(f'You lose the game! Final Score: {team_1.points}-{team_2.points}')
        break
