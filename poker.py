import random
class Card():
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit

    def show(self):
        print("{} of {}".format(self.val, self.suit))

class Deck():
    def __init__(self):
        self.deck = []
        self.build()
        
    def build(self):
        for suits in ["Clubs","Spades","Hearts","Diamonds"]:
            for val in range(2, 15):
                if val == 14:
                    val = "Ace"
                if val == 11:
                    val = "Jack"
                if val == 12:
                    val = "Queen"
                if val == 13:
                    val = "King"
                self.deck.append(Card(val,suits))
        
    def printdeck(self):
        for c in self.deck:
            c.show()
            
    def drawcard(self):
        return self.deck.pop()
    
    def shuffle(self):
        for i in range(len(self.deck)-1, 0 ,-1):
            r = random.randint(0, i)
            self.deck[i], self.deck[r] = self.deck[r], self.deck[i]

class player():
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.moneyAMT = 100
        self.isDealer = False
        self.didFold = False
        self.botfoldState = ["[][]","folded"]
    def draw(self, deck):
        self.hand.append(deck.drawcard())
        
    def showHand(self):
        for c in self.hand:
            c.show()
            
class gamehandler():
    foldedbots = 0
    progress = False
    flops = 3
    won = False
    raiseAMT = 0
    pot = 0
    betting = False
    def __init__(self, playerlist):
        self.playerlist = playerlist
        self.amtCardsDrawn = 2
        self.flopturnriver = []
        for i in range(len(self.playerlist)):
            if self.playerlist[i].name == "Ki":
                self.userPlayer = self.playerlist[i]

    def deal(self, deck):
        for _ in range(self.amtCardsDrawn):
            for players in range(len(self.playerlist)):
                self.playerlist[players].draw(deck)
        for _ in range(5):
            self.flopturnriver.append(deck.drawcard())

    def showAll(self):#shows everyones hand
        for players in range(len(self.playerlist)):
            print("\n{} cards are:".format(self.playerlist[players].name))
            self.playerlist[players].showHand()
        print("\nFLOP:")
        for i in range(len(self.flopturnriver)):
            self.flopturnriver[i].show()
        
    def playHand(self):
        while self.flops <= 6:
            self.botBet()
            for players in self.playerlist:
                print("\n{} cards:".format(players.name))
                print("MONEY:{}".format(players.moneyAMT))
                if players.name == "Ki":
                    players.showHand()
                elif players.didFold == True:
                    print(players.botfoldState[1])
                else:
                    print(players.botfoldState[0])        
            if self.progress == True:
                print("\nFLOP:")
                for i in range(self.flops):
                    self.flopturnriver[i].show()
            print("\nPOT:"+str(self.pot))
#             self.botBet()
            self.betting = False
            userInput = input("\n(1)Check/Call\n(2)Fold\n(3)Raise\n: ")
            actions = {
                "1": self.checkCall,
                "2": self.fold,
                "3": self.Raise
                }
            if userInput not in actions.keys():
                self.playHand()
            actions[userInput]()
        
    def checkCall(self):
        print("\n" * 50)
        if self.progress == True:
            if self.flops == 5:
                self.flops +=1
                self.nextHand()
            else:
                self.flops +=1 
        self.progress = True
        
    def fold(self):
        print("\n" * 50)
        self.flops = 6
        self.showAll()
        
    def Raise(self):
        self.raiseInput = int(input("\nEnter bet: "))
        if self.raiseInput > self.userPlayer.moneyAMT:
            print("Insufficient Funds")
            self.Raise()
        else:
            self.checkCall()
            self.userPlayer.moneyAMT -= self.raiseInput
            self.pot += self.raiseInput
            self.betting = True
        
    def botBet(self):
        if self.betting:
            for player in self.playerlist:
                if player.name != "Ki":
                    if player.didFold == False:
                        r = bool(random.getrandbits(1))
                        if r:
                            if player.moneyAMT >= self.raiseInput:
                                player.moneyAMT -= self.raiseInput
                                self.pot += self.raiseInput
                            elif player.moneyAMT != 0:
                                remainder = self.raiseInput - player.moneyAMT
                                player.moneyAMT -= remainder
                                self.pot += remainder
                        else:
                            self.botFold(player)
                            self.foldedbots += 1 
            self.raiseInput = 0
            self.checkbotFold()

    def botFold(self, botthatfolded):
        botthatfolded.didFold = True
        # pass #Continue later
    def checkbotFold(self):
        if self.foldedbots == 2:
            print("Every bot folded")
            self.betting = False
            self.flops = 6
            for players in self.playerlist:
                if players.name == "Ki":
                    players.moneyAMT += self.pot
                    self.foldedbots = 0
                    self.pot = 0
                    self.nextHand()        
    
    def botRaise(self):
        pass
        #TODO
        #make abstraction to randomize bot raise frequency
    def nextHand(self):
        self.progress = False
        self.flops = 3
        self.flopturnriver = []
        for players in self.playerlist:
            if players.moneyAMT != 0:
                players.didFold = False
            players.hand = []
            if self.pot != 0:                    #DELETE THIS
                if players.name == "Ki":         #COME UP WITH CALC FOR WINNER
                    players.moneyAMT += self.pot #THIS IS JUST HERE BECAUSE ITS NOT
                    self.pot = 0                 #MADE YET
        deck = Deck()
        deck.shuffle()
        poker_player.deal(deck)
        poker_player.playHand()
        

deck = Deck()
deck.shuffle()
# maincharacter = input("Enter your name")
ply1 = player("Jack")
ply2 = player("Ben")
ply3 = player("Marhan") #User Player

players = [ply1,ply2,ply3] #player list 

poker_player = gamehandler(players)
poker_player.deal(deck)
# poker_player.showAll() // Shows everybodys hand
poker_player.playHand()
