import random
# The player class represents the player and the dealer.
class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.wins = 0
        self.hand = []

#Placing a Bet
    def bet(self, amount):
        if amount > self.balance:
            return False #Not enough money to bet.
        self.balance -= amount
        return True
    

#Win counter and adds to your balance when you win.
    def win(self, amount):
        self.balance += amount
        self.wins += 1
        return "{name} wins ${amount}. New balance: ${balance}.".format(
            name=self.name, 
            amount=amount, 
            balance=self.balance
        )
    
#Clears hand for next round.
    def clear_hand(self):
        self.hand = []

#Takes a card from the deck.
    def hit(self, deck):
        self.hand.append(deck.pop())

# Made for calculating the total value of the hand.
    def calculate_hand(self):
        total = 0
        aces = 0
        for card in self.hand:
            if card in ["J", "Q", "K"]:
                total += 10 #Joker, Queens, Kings are set as 10.
            elif card == "A":
                total += 11 # Aces's start as 11.
                aces += 1
            else:
                total += card
        while total > 21 and aces:
            total -= 10  # Aces go from 11 to 1 if total goes over 21.
            aces -= 1
        return total
    
#This is the player's status.
    def __repr__(self):
        return "{name}: Balance: ${balance}, Hand: {hand}, Total: {total}, Wins: {wins}".format(
            name=self.name,
            balance=self.balance,
            hand=self.hand,
            total=self.calculate_hand(),
            wins=self.wins
        )

#The game
class Blackjack:
    def __init__(self, player):
        self.player = player #The player
        self.dealer = Player("Dealer", 0) #The computer dealer
        self.deck = [] #This will hold the cards

#Creates a new deck and shuffles.
    def create_deck(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
        random.shuffle(self.deck)

#Deals two cards to the player and the dealer.
    def deal_initial_cards(self):
        for i in range(2):
            self.player.hit(self.deck)
            self.dealer.hit(self.deck)

#Shows the hand.
    def show_hands(self, reveal_dealer=False):
        print("\n--- Hands ---")
        print(self.player)
        if reveal_dealer:
            print(self.dealer)
        else:
            print("Dealer: Hand: [{}, '?']".format(self.dealer.hand[0]))
        print("-------------\n")

# A round of blackjack,
    def play_round(self, bet_amount):
        #Placing bet.
        if not self.player.bet(bet_amount):
            print("Insufficient Funds!")
            return
#Resets deck for a new round.
        self.create_deck()
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.deal_initial_cards()
        self.show_hands()

        #This the player's turn.
        while self.player.calculate_hand() < 21:
            move = input("Do you want to [h]it or [s]tand? ").lower()
            #If he hits, it will give a card and show the cards as well.
            if move == 'h':
                self.player.hit(self.deck)
                self.show_hands()
                #If player's hand is more than 21, you will bust.
                if self.player.calculate_hand() > 21:
                    print("You busted! Dealer wins.")
                    return
            elif move == 's':
                break
            else:
                print("Please type 'h' or 's'.")

        # Dealer Turn
        #Like actual blackjack, the dealer hits if cards are under 17.
        while self.dealer.calculate_hand() < 17:
            self.dealer.hit(self.deck)

        self.show_hands(reveal_dealer=True)

        #Compares hands.
        player_total = self.player.calculate_hand()
        dealer_total = self.dealer.calculate_hand()

        print("Final Totals - You: {}, Dealer: {}".format(player_total, dealer_total))
        
        #Determines outcome.
        if dealer_total > 21 or player_total > dealer_total:
            print(" You win!")
            self.player.win(bet_amount * 2)
        elif player_total == dealer_total:
            print("It's a tie. You get your bet back.")
            self.player.win(bet_amount)
        else:
            print("Dealer wins.")

# Gets the name of the player and initalize player and blackjack.
players_name = input("What is your name? ")
player = Player(players_name, 100)
game = Blackjack(player)

print("Welcome to Blackjack, {name}!\n".format(name = players_name))

#To keep the game running.
while True:
    print(player)
    try:
        bet = int(input("Enter your bet (or 0 to quit): "))
        #If the game ends.
        if bet == 0:
            print("Thanks for playing! Final balance: ${}".format(player.balance))
            break
        game.play_round(bet)
    except ValueError:
        print("Please enter a valid number.")
