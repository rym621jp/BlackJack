# -*- coding: utf-8 -*-

import random

class Deck():   #ジョーカーの枚数
    class Card():
    
        suits = ["♤","♧","♡","♢"]
        marks=["J","Q","K"]
    
        #num: カードの数字（１〜１３）,0でジョーカー
        #suit: カードのスート（0スペード、1クラブ、2ハート、3ダイヤ）
        def __init__(self, num, suit=0):
            self.num = num
            self.suit = suit
            if(num==0):
                self.joker=True
            else:
                self.joker=False
            
            if(self.joker):
                self.name="Joker"
            else:
                if(self.num>10):
                    num_ = self.marks[num%10-1]
                    self.count = 10
                elif(self.num==1):
                    num_ = "A"
                    self.count = 11
                else:
                    num_ = str(num)
                    self.count = num
                
                self.name = self.suits[self.suit]+num_
        
        def disp(self):
            print(self.name)
            
    #joker: ジョーカーの枚数
    def __init__(self, joker=0):
        
        self.deck = []
        
        for suit in range(4):
            for num in range(1,14):
                self.deck.append(self.Card(num,suit))
        
        for cnt in range(joker):
            self.deck.append(self.Card(0))
            
        random.shuffle(self.deck)
        
    def draw(self,num=1):
        result = []
        for cnt in range(num):
            result.append(self.deck.pop(cnt))
        return result
    

class Players():   #人数, 初期所持チップ
    class Player():
        def __init__(self, name , chips, isDealer=False):
            self.chips = chips
            self.name = name
            self.hand = []
            self.count = 0
            self.betting = 0
            self.originalBet = 0
            self.finish = False
            self.bust = False
            self.BJ = False
            self.NBJ = False
            self.isDealer = isDealer

        def nextGame(self):
            self.hand = []
            self.count = 0
            self.betting = 0
            self.originalBet = 0
            self.finish = False
            self.bust = False
            self.BJ = False
            self.NBJ = False

        def firstBet(self, amount):
            amount_ = 0
            try:
                amount_ = int(amount)
            except:
                print ("無効な入力です")
                return False
            if(self.chips<amount_):
                print("チップが足りません")
                return False
            self.chips-=amount_
            self.betting += amount_
            self.originalBet = amount_
            return True
        
        def bet(self, amount):
            if(self.chips<amount):
                print("チップが足りません")
                return False
            self.chips-=amount
            self.betting += amount
            return True
    
        def won(self, amount):
            self.chips += amount
            self.betting = 0
            self.finish = True
            
        def lose(self):
            self.betting = 0
            
        def showChips(self):
            print("{}: {}".format(self.name, self.chips))
            
        def addCard(self, card):
            if(type(card)==list):
                for fuc in card:
                    self.hand.append(fuc)
            else:
                self.hand.append(card)
            self.counter(returnValue=False)
            if(self.count==21 and len(self.hand)==2):
                self.finish = True
                self.BJ = True
                self.NBJ = True
            elif(self.count==21):
                self.finish = True
                self.BJ = True
            if(self.count>21):
                self.bust = True
                self.finish = True
        
        def showCard(self, hide=0):
            result = ""
            numOfCards = len(self.hand)
            for i in range(numOfCards):
                if(i < numOfCards - hide):
                    result += self.hand[i].name+" "
                else:
                    result += "■■ "
            print("{}の手札: {}（カウント: {}）".format(self.name,result,self.counter(hide=hide)))
            if(hide==0):
                if(self.bust):
                    print("{}->バーストしました。".format(self.name))
                elif(self.BJ and (not self.NBJ)):
                    print("{}->BlackJack".format(self.name))
        
        def DD(self):
            if(self.chips<self.originalBet):
                print("チップが足りません")
                return False
            self.finish = True
            self.bet(self.originalBet)
            return True

        def ST(self):
            self.finish = True

        def SR(self):
            self.finish = True
            self.won(self.betting//2)

        def counter(self, returnValue=True, hide=0):
            result = 0
            numOfAce = 0
            """if(not hide==0):
                hand = self.hand[:hide*-1]
            else:
                hand = self.hand"""
            for card in self.hand:
                result += card.count
                if(card.num==1):
                    numOfAce += 1
            if(result>21):
                for cnt in range(numOfAce):
                    result -= 10
                    if(result<21):
                        break
            if(result>21):
                self.bust = True
                self.finish = True
            self.count = result

            if(not hide==0):   #ハイドしたときreturnの値をアップカードのみのカウントにする
                result = 0
                hand = self.hand[:hide*-1]
                for card in hand:
                    result += card.count
                    if(card.num==1):
                        numOfAce += 1
                if(result>21):
                    for cnt in range(numOfAce):
                        result -= 10
                        if(result<21):
                            break
                if(result>21):
                    self.bust = True
                    self.finish = True
            if(self.count==21):
                self.BJ = True
                self.finish = True
            if(returnValue):
                return result
        
        """def do(self,action):
            if(action == "DD"):
                success = self.DD()
                if(not success):
                    return False
            elif(action == "ST"):
                self.ST()
            elif(action == "SR"):
                self.SR()
            else:
                print("無効な入力です")
                return False
            return True"""


    #ここからPlayers()の処理
    players = []
    def __init__(self, num, initialChips):
        for i in range(num):
            name = input("プレイヤーの名前を入力してください")
            if(name == ""):
                name = "player"+str(i+1)
            self.players.append(self.Player(name, initialChips))

    def canFinish(self):
        result = True
        for player in self.players:
            result = result and player.finish
        return result

    def allBust(self):
        result = True
        for player in self.players:
            result = result and player.bust
        return result

            
class BlackJack(Players,Deck):   #参加人数, 初期所持チップ, ジョーカーの枚数
    
    def __init__(self, numOfPlayers=1, initialChips=1000):
        Players.__init__(self, numOfPlayers, initialChips)
        Deck.__init__(self, 0)
        self.dealer = Players.Player("dealer",0,True)

    def andCalc(self, boolList):
        result = True
        for value in boolList:
            result = result and value
        return result

    def do(self, player, action):
        if(action.upper() in ["H","HIT"]):
            player.addCard(self.draw())
        elif(action.upper() in ["ST","STAND"]):
            player.ST()
        elif(action.upper() in ["DD","DOUBLE","DOUBLING"]):
            if(player.DD()):
                player.addCard(self.draw())
            else:
                return False
        elif(action.upper() in ["SR","SURRENDER"]):
            player.SR()
        else:
            print("無効な入力です")
            return False 
        return True

    def ordinalNo(self,num):
        if(num%10 == 1):
            return str(num)+"st"
        elif(num%10 == 2):
            return str(num)+"nd"
        elif(num%10 == 3):
            return str(num)+"rd"
        else:
            return str(num)+"th"

    def playGame(self):
        leaveTable = False
        while not leaveTable:

            turnCnt = 1
            finishGame = False

            #ベット額を決定
            for player in self.players:
                success = False
                while not success:
                    success = player.firstBet(input("{}さんのターン-> ベットする金額を入力（所持金：{}チップ）".format(player.name,player.chips)))
            
            #カードを配る
            self.dealer.addCard(self.draw(2))
            for player in self.players:
                player.addCard(self.draw(2))

            print("-----{} turn--------------------------".format(self.ordinalNo(turnCnt)))
                
            #カードを表示
            self.dealer.showCard(1)
            for player in self.players:
                player.showCard()
                if(player.NBJ and not self.dealer.NBJ):
                    print("{}さん-> BlackJack! あなたの勝利です。".format(player.name))
                    player.won(int(player.betting * 2.5))
                elif(player.NBJ and self.dealer.NBJ):
                    print("{}さん-> プッシュです。".format(player.name))
                    player.won(player.betting)
                    finishGame = True
                elif(self.dealer.NBJ):
                    print("{}さん-> ナチュラル21でディーラーの勝利です。".format(player.name))
                    player.lose()
                    finishGame = True
                
            while not finishGame:
                """currentPlayer = []
                for player in self.players:
                    if(not player.finish):
                        currentPlayer.append(player)"""

                #プレイヤーのアクション
                for player in self.players:
                    if(not player.finish):
                        success = False
                        while not success:
                            action = input("{}さんアクションを選択してください（H:ヒット, ST:スタンド, DD:ダブルダウン, SR:サレンダー）".format(player.name))
                            success = self.do(player,action)
                            if(player.bust or player.BJ):
                                player.showCard()

                if(self.allBust()):
                    break
                    
                #ディーラーのアクション
                if(not self.dealer.finish):
                    if(self.dealer.count<=16):
                        self.dealer.addCard(self.draw())
                    if(self.dealer.count>16):
                        self.dealer.finish = True

                turnCnt += 1

                if((not self.dealer.finish) or (not self.canFinish())):
                    print("-----{} turn--------------------------".format(self.ordinalNo(turnCnt)))

                    self.dealer.showCard(1)
                    for player in self.players:
                        if(not player.finish):
                            player.showCard()

                if(self.dealer.finish and self.canFinish()):
                    finishGame = True

            #勝敗の判定
            if(not self.allBust()):   #allBust()で終了した場合勝敗表示済みのため除外
                print("-----RESULT--------------------------")
                self.dealer.showCard()
                if(self.dealer.bust):   #ディーラーがバストしている場合の勝敗
                    for player in self.players:
                        if(player.NBJ or player.bust):   #勝敗表示済み除外

                            continue
                        else:
                            player.showCard()
                            print("{}さん->あなたの勝利です。".format(player.name))
                            player.won(player.betting*2)
                else:   #ディーラーがバストしていない場合の勝敗
                    for player in self.players:
                        if(player.NBJ or player.bust):   #勝敗表示済み除外
                            continue
                        player.showCard()
                        if(self.dealer.count > player.count):   #ディーラー勝利
                            print("{}さん->あなたの敗北です。".format(player.name))
                            player.lose()
                        elif(self.dealer.count < player.count):   #プレイヤー勝利
                            print("{}さん->あなたの勝利です。".format(player.name))
                            player.won(player.betting*2)
                        elif(self.dealer.count == player.count):   #引き分け
                            print("{}さん->プッシュです。".format(player.name))
                            player.won(player.betting)

            #所持チップで継続可能か判定
            print("-----ゲーム終了--------------------------")
            cnt = 0
            nextPlayers = []
            for player in self.players:
                if(player.chips>0):
                    print("{}さんのチップ数：".format(player.name), player.chips)
                    success = False
                    while not success:
                        tmp = input("ゲームを続けますか？（Y/N）")
                        if(tmp.upper() in ["Y","YES"]):
                            player.nextGame()
                            nextPlayers.append(player)
                            success = True
                            continue
                        elif (tmp.upper() in ["N","NO"]):
                            success = True
                        else:
                            print("無効な入力です")
                cnt += 1
            self.players = nextPlayers
            if(len(self.players)==0):
                leaveTable = True
            else:
                self.dealer.nextGame()
                
#=====以下実行部=======================================================

player = 1   #プレイ人数を入力してください
initialChips = 1000   #初期所持チップ数を入力してください

game1 = BlackJack(player,initialChips)
game1.playGame()

