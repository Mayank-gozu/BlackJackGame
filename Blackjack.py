# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

DIST  = 30
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hands = [] # create Hand object

    def __str__(self):
        self.hand_str = ""
        for  hand in range(len(self.hands)):
            self.hand_str += self.hands[hand].get_suit() + self.hands[hand].get_rank() + " "
        return "Hand Contains "+self.hand_str +" "# return a string representation of a hand

    def add_card(self, card):
        self.hands.append(card) # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.hand_value = 0
        self.no_aces = True
        for hand in self.hands:
            self.hand_value += VALUES[hand.get_rank()]
            if hand.get_rank() == 'A':
                self.no_aces = False
        if (self.no_aces):        
            return self.hand_value
        else:
            if self.hand_value + 10 <=21:
                return self.hand_value + 10
            else:
                return self.hand_value
   
    def draw(self, canvas, pos):
        for count in range (1, len(self.hands)):
            self.hands[count].draw(canvas, [pos[0] + CARD_CENTER[0] + count * (DIST + CARD_SIZE[0]), pos[1] + CARD_CENTER[1]])


        
# define deck class 
class Deck:
    def __init__(self):
        self.decks = [] # create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                deck = Card(suit,rank)
                #print deck
                self.decks.append(deck)
                

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.decks)

    def deal_card(self):
        return random.choice(self.decks)    # deal a card object from the deck
    
    def __str__(self):
        ans = ""
        for deck in self.decks:
            ans += deck.get_suit()+deck.get_rank() + " "
        return ans    
            # return a string representing the deck

#define event handlers for buttons
def deal():
    global outcome, in_play,deck,dealer_hand,player_hand,score
    if in_play:
        outcome = "Dealer Wins"
        score = score -1 
        in_play = False
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "Dealer Hand"
    print dealer_hand
    print "Player Hand"
    print player_hand
    # your code goes here    
    in_play = True
    

def hit():
    # replace with your code below
    Hit = False
    global score, in_play,outcome
    if (in_play):
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            print player_hand
            Hit = True
        if Hit:
            if player_hand.get_value() > 21:
                outcome = "You Have Been Busted"
                print "You Have Been Busted"
                score = score -1
                in_play = False
    else:
        print "Cannot Hit ! You Have been Busted"
        
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    # replace with your code below
    global score,in_play,outcome
    bust = False
    if in_play:
        if dealer_hand.get_value() < 17:
            while dealer_hand.get_value() <= 17:
                dealer_hand.add_card(deck.deal_card())
                if dealer_hand.get_value() > 17:
                    bust = True
            if bust:
                outcome = "Dealer Busted"
                print "Dealer Busted"
                print dealer_hand
                score = score +1
                in_play = False
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "Dealer Wins"
                print "Dealer Wins"
                score = score -1
                in_play = False
            else :
                print dealer_hand
                outcome = "Player Wins"
                print "Player Wins"
                score = score+1
                in_play = False
    else:
        outcome = "Cannot Stand ! You have been Busted"
        print "Cannot Stand ! You have been Busted"
            
            
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    
    # test to make sure that card.draw works, replace with your code below
    global in_play, dealer_hand, player_hand,score    
    canvas.draw_text("Blackjack", [100, 100], 35, "Olive")
    canvas.draw_text("Score " + str(score), [450, 100], 25, "Black")
    canvas.draw_text("Dealer", [80, 170], 25, "Black")
    canvas.draw_text(outcome, [200, 170], 25, "Black")
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [60 + CARD_BACK_SIZE[0], 170 + CARD_BACK_SIZE[1]], CARD_SIZE)
    else:
        dealer_hand.hands[0].draw(canvas, [60 + CARD_CENTER[0], 170 + CARD_CENTER[1]])
    dealer_hand.draw(canvas, [60, 170])
    canvas.draw_text("Player", [80, 370], 25, "Black")
    if in_play:
        canvas.draw_text("Hit or stand?", [200, 370], 25, "Black")
    else:
        canvas.draw_text("New deal?", [200, 370], 25, "Black")
    
    player_hand.hands[0].draw(canvas, [60 + CARD_CENTER[0], 370 + CARD_CENTER[1]])
    player_hand.draw(canvas, [60, 370])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Silver")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric