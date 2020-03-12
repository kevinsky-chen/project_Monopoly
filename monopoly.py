#-----------------初始條件------------------------
test_mode=input("TEST MODE Y/N?")
Test_mode=False
if test_mode=='Y':
    Test_mode=True

import pygame as pg
import random
pg.init()

width, height = 600, 600

screen = pg.display.set_mode((width, height))
pg.display.set_caption('大富翁')

#insert background
background = pg.image.load('mono1 - NEW.jpg').convert()
#insert personal color
buy_r1 = pg.image.load('RED_1.png').convert_alpha()
buy_r2 = pg.image.load('RED_2.png').convert_alpha()
buy_b1 = pg.image.load('BLUE_1.png').convert_alpha()
buy_b2 = pg.image.load('BLUE_2.png').convert_alpha()
buy_g1 = pg.image.load('GREEN_1.png').convert_alpha()
buy_g2 = pg.image.load('GREEN_2.png').convert_alpha()
buy_y1 = pg.image.load('YELLOW_1.png').convert_alpha()
buy_y2 = pg.image.load('YELLOW_2.png').convert_alpha()
yellow = pg.image.load('yellow.png').convert_alpha()
blue = pg.image.load('blue.png').convert_alpha()
red = pg.image.load('red.png').convert_alpha()
green = pg.image.load('green.png').convert_alpha()

#insert house
house_1 = pg.image.load("house_1.png").convert_alpha()
house_2 = pg.image.load("house_2.png").convert_alpha()
house_3 = pg.image.load("house_3.png").convert_alpha()
house_4 = pg.image.load("house_4.png").convert_alpha()
hotel = pg.image.load("hotel.png").convert_alpha()


monopoly_map=["START","A","B","Opportunity","C","D","E","Destiny","Park","F",
              "G","Opportunity","H","I","J","Destiny","Park","K","L",
              "Opportunity","M","N","O","Destiny","Park","P","Q",
              "Opportunity","R","S","T","Destiny"]
land_cost=[0,1200,2600,0,1000,2800,3200,0,0,1000,1800,0,2000,2500,3500,0,0,800,2400,3000,2200,2800,0,0,600,2200,0,4000,1400,3000,0]
land_owner=[]
land_level=[]
player_list=[]
Player_list=[]
kill_list=[]
Turn=0
player_turn=0

import random

for x in range(0,32):
    land_owner.insert(x,None)
for x in range(0,32):
    land_level.insert(x,0)

def Opportunity(rank):
    x=random.randint(1,2)
    #x=random.randint(1,10)#之後根據情況，會追加更多機會卡
    if x==1:
        print('''You get 1000 dollars!
        If you have the least money of all players, get 1000 more.''')
        command='earn'
        if rank==4:
            value=2000
        else:
            value=1000
        command_list=[command,value]
        
        return command_list     
                    
    elif x==2:
        print('''You lose 1000 dollars!
If you have the most money of all players, lose 1000 more.''')
        command='pay'
        if rank==1:
            value=2000
        else:
            value=1000
        command_list=[command,value]
        
        return command_list  
import opportunity
import destiny

#-----------------角色設定------------------------
class setPlayer:
    def __init__(self,player_name):
        self.name = player_name
        self.lands = dict()
        self.money = 30000
        #self.image = image
        self.position = 0
        #self.dice_value = 0
        self.effect=dict()
        self.bankrupt=False
        
    def buy(self,land_name,cost):
        self.lands[land_name]=0
        self.money-=cost
        return self.money
    
    def build(self,land_name,cost):
        self.lands[land_name]=self.lands[land_name]+1
        self.money-=cost
        return self.money
    
    def move(self,move):
        self.position=int((self.position+move)%32)
        return self.position
    
    def pay(self,money):
        '''Tolls and the cost due to destiny are counted'''
        self.money-=money
        return self.money
        if self.money<0:
            self.bankrupt=True

    def earn(self,money):
        '''Tolls and the earning due to destiny are counted'''
        self.money+=money
        return self.money
    def effect_earn(self,string,value):
        self.effect[string]=value
        

#-----------------函數------------------------
#賦予玩家屬性
def init(n_of_player):
    while n_of_player!="2" and n_of_player!="3" and n_of_player!="4":
        n_of_player=input("How many players will play the game?(enter 2 or 3 or 4)") 
    if int(n_of_player)>=2:
        player1_name = input("player1's name?")
        player1=setPlayer(player1_name)
        player_list.insert(0,player1)
        Player_list.insert(0, player1_name)
        player2_name = input("player2's name?")
        while player2_name== player1_name:
            player2_name = input("player2's name?")    
        player2=setPlayer(player2_name)
        player2.position=8
        player_list.insert(1,player2)
        Player_list.insert(1, player2_name)
        
        print("%s is in this game!"%(player1.name)) #玩家進場的提示句
        print("%s is in this game!"%(player2.name)) #玩家進場的提示句
    if int(n_of_player)>=3:
        player3_name = input("player3's name?")
        while player3_name== player1_name or player3_name== player2_name:
            player3_name = input("player3's name?")
        player3=setPlayer(player3_name)
        player_list.insert(2,player3)
        Player_list.insert(2,player3_name)
        player3.position=16
        
        print("%s is in this game!"%(player3.name)) #玩家進場的提示句
    if int(n_of_player)==4:
        player4_name = input("player4's name?")
        while player4_name== player1_name or player4_name==player2_name or player4_name==player3_name:
            player4_name = input("player4's name?")
        player4=setPlayer(player4_name)
        player_list.insert(3,player4)
        Player_list.insert(3,player4_name)
        player4.position=24
        print("%s is in this game!"%(player4.name)) #玩家進場的提示句
    
def action(string):
    """
    This fucntion decide what process to run by string the player enter.
    Input:str(1,2,sell)/Output:a process
    """

    if string==str(1):
        move=roll_dices(1)
    elif string==str(2):
        move=roll_dices(2)
    else:
        move=0
    print(move)
    
    return move
      
    
def roll_dices(n):
    '''
    This fucntion can roll n dices, and sum them up.
    Input:an integer/Output:the sum of dices dots.
    '''
    import random
    dice=0
    index=1
    while index<=n:
        Dice=random.randint(1,6)
        dice += Dice
        index += 1
    
    return dice


def land_type(x):
    '''
    This function can guide what action will the program due by giving
    the type of land.
    Input:position/Output:str(type)
    '''
    if x%8==1 or x%8==2 or x%8==4 or x%8==5 or x%8==6:
        type_of_land="buyable"
    elif monopoly_map[x]=="Opportunity":
        type_of_land="Opportunity"
    elif monopoly_map[x]=="Destiny":
        type_of_land="Destiny"
    else:
        type_of_land="None"
    return type_of_land

def build_cost(n):
    '''Input:land_of_cost/Output:build cost'''
    if n<=1200:
        cost=500
    elif n<=2000:
        cost=1000
    elif n<=2800:
        cost=1500
    else:
        cost=2000
    return cost

def toll(cost,level):
    '''Input: land_cost and land level(both are intergers)
Output:toll(also interger)'''
    if level==0:
        toll=cost*0.1
    elif level==1:
        toll=cost*0.4
    elif level==2:
        toll=cost*1
    elif level==3:
        toll=cost*1.5
    elif level==4:
        toll=cost*3
    else:
        toll=cost*5
    return toll

#玩家狀況對話框
def text(input_text1, input_text2, input_text3, input_text4, input_round, player_number, position1 = (110,110) , position2 = (300,110), position3 = (110,130), position4 = (300,130), position5 = (450,110)):
    '''
    This function can show the attribute of players in the middle of the map, including their name and money.
    '''
    font = pg.font.SysFont("msgothicmsuigothicmspgothic", 18, bold= True, italic= False)
    font_for_turn = pg.font.SysFont("SHOWG", 50, bold= True, italic= False)
    output_text1 = font.render(input_text1, True, (30,144,255))
    output_text2 = font.render(input_text2, True, (30,144,255))
    output_text5 = font_for_turn.render(input_round, True, (220,20,60))

    screen.blit(background, (0, 0))

    if(player_number == 4):
        output_text3 = font.render(input_text3, True, (30,144,255))
        output_text4 = font.render(input_text4, True, (30,144,255))

        screen.blit(output_text1, position1)  
        screen.blit(output_text2, position2)  
        screen.blit(output_text3, position3)
        screen.blit(output_text4, position4)
        screen.blit(output_text5, position5)  
    elif(player_number == 3):
        output_text3 = font.render(input_text3, True, (30,144,255))

        screen.blit(output_text1, position1)  
        screen.blit(output_text2, position2)  
        screen.blit(output_text3, position3)
        screen.blit(output_text5, position5)
    else:
        screen.blit(output_text1, position1)  
        screen.blit(output_text2, position2)  
        screen.blit(output_text5, position5)
      
    pg.display.flip()  


def rank(x,list_of_playermoney):
    '''This fucntion can show the rank of one assigned player.
Input:The money the assigned player owns.(Integer)/Output: the rank1,2,3,4 '''
    money_list=sorted(list_of_playermoney)
    if x==money_list[0]:
        rank="last"
    elif x==money_list[-1]:
        rank="first"

    else:
        rank="middle"
    return rank

#-----------------主程式------------------------

running=True
screen.blit(background, (0, 0))

#輸入玩家的提示字串   
n_of_player=input("How many players will play the game?(enter 2 or 3 or 4):")
init(n_of_player)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    status_quo = ""     #第一人
    status_quo1 = ""    #第二人 
    status_quo2 = ""    #第三人
    status_quo3 = ""    #第四人
    
        
    for i in range(len(player_list)):
        screen.blit(background, (0, 0))
        status_quo = "%s   %d" %(player_list[0].name, player_list[0].money)
        status_quo1 = "%s   %d" %(player_list[1].name, player_list[1].money)
        if len(player_list) >= 3:
            status_quo2 = "%s   %d" %(player_list[2].name, player_list[2].money)
        if len(player_list) == 4:
            status_quo3 = "%s   %d" %(player_list[3].name, player_list[3].money)
        text(status_quo, status_quo1, status_quo2, status_quo3, str(Turn), len(player_list))

    player_turn=int(player_turn%len(Player_list))
    pg.display.update()
    
    semi_class_name = ""
    if player_turn==0:
        #Player=Player_list[0]
        
        semi_class_name = Player_list[0]
        Turn=Turn+1
    if player_turn==1:
        #Player=Player_list[1]
        
        semi_class_name = Player_list[1]
    if player_turn==2:
        #Player=Player_list[2]
        
        semi_class_name = Player_list[2]
    if player_turn==3:
        #Player=Player_list[3]
                               #叫出物件
        semi_class_name = Player_list[3]
    for pl in player_list:
        if pl.name==semi_class_name:
            player=pl
    
    
        
        
    position=player.position
    step = position%8
    
    if semi_class_name == player_list[0].name:
        if position/8 < 1:
            screen.blit(blue, (66.67*step+5,15))                    
        elif position/8 < 2:
            screen.blit(blue, (540, 66.67*step+5))
        elif position/8 < 3:
            screen.blit(blue, (610-66.67*(1+step), 555))
        else:
            screen.blit(blue, (20, 66.67*(8-step)+5))


    if semi_class_name == player_list[1].name:
        if position/8 < 1:
            screen.blit(yellow, (66.67*step+20,15))
        elif position/8 < 2:
            screen.blit(yellow, (555, 66.67*step+5))
        elif position/8 < 3:
            screen.blit(yellow, (625-66.67*(1+step), 555))
        else:
            screen.blit(yellow, (35, 66.67*(8-step)+5))
            
    if int(n_of_player)>= 3:
        if semi_class_name == player_list[2].name:
            if position/8 < 1:
                screen.blit(red, (66.67*step+5,35))
            elif position/8 < 2:
                screen.blit(red, (540, 66.67*step+20))
            elif position/8 < 3:
                screen.blit(red, (610-66.67*(1+step), 570))
            else:
                screen.blit(red, (20, 66.67*(8-step)+20))
                
    if int(n_of_player) == 4:
        if semi_class_name == player_list[3].name:
            if position/8 < 1:
                screen.blit(green, (66.67*step+20,35))
            elif position/8 < 2:
                screen.blit(green, (555, 66.67*step+20))
            elif position/8 < 3:
                screen.blit(green, (625-66.67*(1+step),570))
            else:
                screen.blit(green, (35, 66.67*(8-step)+20))

    pg.display.update()
    money=player.money
    name=str(player.name)    
        
    print("""It's turn %d of %s.

He/She has %d dollars."""%(Turn,name,money))    
    
    

    
    lst = []
    lst_ = []
    lst__ = []
    lst___ = []
    for land in range(8):
        if land_owner[land] != None:
            lst.append(land)
            for site in lst:
                if land_owner[site] == player_list[0].name:
                    screen.blit(buy_b1, (66.67*(site%8),0))
                elif land_owner[site] == player_list[1].name:
                    screen.blit(buy_y1, (66.67*(site%8),0))
                elif land_owner[site] == player_list[2].name:
                    screen.blit(buy_r1, (66.67*(site%8),0))
                else:
                    screen.blit(buy_g1, (66.67*(site%8),0))
                
    for land_ in range(8,16):
        if land_owner[land_] != None:
            lst_.append(land_)
            for site_ in lst_:
                if land_owner[site_] == player_list[0].name:
                    screen.blit(buy_b2, (590, 66.67*(site_%8)))
                elif land_owner[site_] == player_list[1].name:
                    screen.blit(buy_y2, (590, 66.67*(site_%8)))
                elif land_owner[site_] == player_list[2].name:
                    screen.blit(buy_r2, (590, 66.67*(site_%8)))
                else:
                    screen.blit(buy_g2, (590, 66.67*(site_%8)))

    for land__ in range(16,24):
        if land_owner[land__] != None:
            lst__.append(land__)
            for site__ in lst__:
                if land_owner[site__] == player_list[0].name:
                    screen.blit(buy_b1, (600-66.67*(1+site__%8), 590))
                elif land_owner[site__] == player_list[1].name:
                    screen.blit(buy_y1, (600-66.67*(1+site__%8), 590))
                elif land_owner[site__] == player_list[2].name:
                    screen.blit(buy_r1, (600-66.67*(1+site__%8), 590))
                else:
                    screen.blit(buy_g1, (600-66.67*(1+site__%8), 590))

    for land___ in range(24,32):
        if land_owner[land___] != None:
            lst___.append(land___)
            for site___ in lst___:
                if land_owner[site___] == player_list[0].name:
                    screen.blit(buy_b2, (0, -66.67*(1+site___%8)+600))
                elif land_owner[site___] == player_list[1].name:
                    screen.blit(buy_y2, (0, -66.67*(1+site___%8)+600))
                elif land_owner[site___] == player_list[2].name:
                    screen.blit(buy_r2, (0, -66.67*(1+site___%8)+600))
                else:
                    screen.blit(buy_g2, (0, -66.67*(1+site___%8)+600))
    bst = []
    bst_ = []
    bst__ = []
    bst___ = []
    for land in range(8):
        if land_level[land] != 0:
            bst.append(land)
            for site in bst:
                if land_level[site] == 1:
                    screen.blit(house_1, (66.67*(site%8),20))
                elif land_level[site] == 2:
                    screen.blit(house_2, (66.67*(site%8),20))
                elif land_level[site] == 3:
                    screen.blit(house_3, (66.67*(site%8),20))
                elif land_level[site] == 4:
                    screen.blit(house_4, (66.67*(site%8),20))
                else:
                    screen.blit(hotel, (66.67*(site%8),20))
    for land_ in range(8,16):
        if land_level[land_] != 0:
            bst_.append(land_)
            for site_ in bst_:
                if land_level[site_] == 1:
                    screen.blit(house_1, (550, 66.67*(site_%8)))
                elif land_level[site_] == 2:
                    screen.blit(house_2, (550, 66.67*(site_%8)))
                elif land_level[site_] == 3:
                    screen.blit(house_3, (550, 66.67*(site_%8)))
                elif land_level[site_] == 4:
                    screen.blit(house_4, (550, 66.67*(site_%8)))
                else:
                    screen.blit(hotel, (550, 66.67*(site_%8)))
                
    for land__ in range(16,24):
        if land_level[land__] != 0:
            bst__.append(land__)
            for site__ in bst__:
                if land_level[site__] == 1:
                    screen.blit(house_1, (600-66.67*(1+site__%8), 550))
                elif land_level[site__] == 2:
                    screen.blit(house_2, (600-66.67*(1+site__%8), 550))
                elif land_level[site__] == 3:
                    screen.blit(house_3, (600-66.67*(1+site__%8), 550))
                elif land_level[site__] == 4:
                    screen.blit(house_4, (600-66.67*(1+site__%8), 550))
                else:
                    screen.blit(hotel, (600-66.67*(1+site__%8), 550))
    
    for land___ in range(24,32):
        if land_level[land___] != 0:
            bst___.append(land___)
            for site___ in bst___:
                if land_level[site___] == 1:
                    screen.blit(house_1, (20, -66.67*(1+site___%8)+600))
                elif land_level[site___] == 2:
                    screen.blit(house_2, (20, -66.67*(1+site___%8)+600))
                elif land_level[site___] == 3:
                    screen.blit(house_3, (20, -66.67*(1+site___%8)+600))
                elif land_level[site___] == 4:
                    screen.blit(house_4, (20, -66.67*(1+site___%8)+600))
                else:
                    screen.blit(hotel, (20, -66.67*(1+site___%8)+600))
    
    pg.display.update()
    

    move_control=False
    #print(land_level)
    print("You are in position:","land",position,",whose name is",monopoly_map[position])
    print('''Enter one of these:1:roll a dice,2:roll 2 dices,sell:sell your land.''')
    if len(player.effect)!=0:
        
        for k in (player.effect).keys():
            if k=='move':
                move=player.effect[k]
                move_control=True
                print("Destiny effect: You will move "+str(move)+" steps.")
        del player.effect[k]
    if move_control==False:           
        if Test_mode==True:
            string="2"
            move=action(string)
        
        else:
            string=input("Choose one:1,2:")
            while string!="1" and string!="2":
                string=input("Choose one:1,2:")
            move=action(string)
        
    
    position=player.move(move)
    position=player.position
    step = position%8
    
    if semi_class_name == player_list[0].name:
        if position/8 < 1:
            screen.blit(blue, (66.67*step+5,15))                    
        elif position/8 < 2:
            screen.blit(blue, (540, 66.67*step+5))
        elif position/8 < 3:
            screen.blit(blue, (610-66.67*(1+step), 555))
        else:
            screen.blit(blue, (20, 66.67*(8-step)+5))


    if semi_class_name == player_list[1].name:
        if position/8 < 1:
            screen.blit(yellow, (66.67*step+20,15))
        elif position/8 < 2:
            screen.blit(yellow, (555, 66.67*step+5))
        elif position/8 < 3:
            screen.blit(yellow, (625-66.67*(1+step), 555))
        else:
            screen.blit(yellow, (35, 66.67*(8-step)+5))
            
    if int(n_of_player)>= 3:
        if semi_class_name == player_list[2].name:
            if position/8 < 1:
                screen.blit(red, (66.67*step+5,35))
            elif position/8 < 2:
                screen.blit(red, (540, 66.67*step+20))
            elif position/8 < 3:
                screen.blit(red, (610-66.67*(1+step), 570))
            else:
                screen.blit(red, (20, 66.67*(8-step)+20))
                
    if int(n_of_player) == 4:
        if semi_class_name == player_list[3].name:
            if position/8 < 1:
                screen.blit(green, (66.67*step+20,35))
            elif position/8 < 2:
                screen.blit(green, (555, 66.67*step+20))
            elif position/8 < 3:
                screen.blit(green, (625-66.67*(1+step),570))
            else:
                screen.blit(green, (35, 66.67*(8-step)+20))

    pg.display.update()

    print("You are in position:","land",position,",whose name is",monopoly_map[position])
    
    if position-int(move)<0 and position!=0:
        print("You go through START! Give you 2000.")
    if land_type(position)=="buyable":
        if land_owner[position]==None:
            if (player.money-int(land_cost[position]))>=0:
                if Test_mode==True:
                    buy="Y"
                else:
                    buy=str(input("Do you want to buy %s, which costs %d ? Enter Y for yes, N for no:"
                          %(str(monopoly_map[position]),land_cost[position])))
                    
                while (buy!="Y" and buy!="N"):
                    buy=str(input("Do you want to buy %s, which costs %d ? Enter Y for yes, N for no:"
                          %(str(monopoly_map[position]),land_cost[position])))
                
                if buy=="Y":
                    land_owner.pop(position)
                    land_owner.insert(position,player.name)
                    player.buy(monopoly_map[position],land_cost[position])
                    money=player.money
                
                    #print(land_owner)
                    #print(player.lands)
                print("%s has bought %s, %s has %d left."%(player.name,monopoly_map[position],player.name,money))
            else:
                print("Sorry, you don't have enough money to buy it.")

                
        elif land_owner[position]==player.name:
            if (money-build_cost(land_cost[position]))>=0 and land_level[position]<=4:
                if Test_mode==True:
                    build="Y"
                else:
                    build=str(input("Do you want to build %s from level %d to level %d, which costs %d ? Enter Y for yes, N for no:"
                          %(str(monopoly_map[position]),land_level[position],land_level[position]+1,build_cost(land_cost[position]))))
                while (build!="Y" and build!="N"):
                    build=str(input("Do you want to build %s from level %d to level %d, which costs %d ? Enter Y for yes, N for no:"
                          %(str(monopoly_map[position]),land_level[position],land_level[position]+1,build_cost(land_cost[position]))))
                if build=="Y":
                    
                    player.build(monopoly_map[position],build_cost(land_cost[position]))
                    land_level[position]=land_level[position]+1
                    print("You have built %s from level %d to level %d, you have %d left."%(monopoly_map[position],land_level[position],land_level[position]+1,money))
                    
            elif land_level[position]==5:
                print("You have owned a hotel here! Good Job!")
            else:
                print("Sorry, you don't have enough money to build it.")
        else:
            if land_owner[position]==player_list[0].name:
                owner=player_list[0]
            elif land_owner[position]==player_list[1].name:
                owner=player_list[1]
            elif land_owner[position]==player_list[2].name:
                owner=player_list[2]
            elif land_owner[position]== player_list[3].name:
                owner=player_list[3]
            else:
                print("There is a bug")
            cost=land_cost[position]
            level=land_level[position]
            pay=toll(cost,level)
            print("The toll of %s, which is owned by %s, is %d dollars."
                  %(monopoly_map[position],owner.name,pay))
            owner.earn(pay)
            player.pay(pay)
            print("%s pays %d dollars. %s earns %d dollars."
                  %(player.name,pay,owner.name,pay))
                
    player_turn+=1
    if land_type(position)=="Opportunity":
        x=player.money
        list_of_playermoney=[]
        for c in player_list:
            list_of_playermoney.insert(-1,c.money)
        #print(x,list_of_playermoney)
        Rank=rank(x,list_of_playermoney)
        #print(Rank)
        command_list=opportunity.Opportunity(Rank)
        if command_list[0]=='earn':
            if type(command_list[1])=="int":
                player.earn(command_list[1])
                print("You have %d dollars now."%player.money)
            elif command_list[1]=="land":
                prize=200*len(player.lands)
                player.earn(prize)
                print("You have %d lands. You earn %d money. You have %d dollars now."%(len(player.lands),prize,player.money))
            elif command_list[1]=="land,house":
                prize=200*len(player.lands)
                count=0
                print(player.lands)
                house=player.lands
                print(type(house))
                for c in house.values():
                    prize+=100*c
                    count+=c
                player.earn(prize)
                print("You have %d lands and %d levels. You earn %d money. You have %d dollars now."%(len(player.lands),count,prize,player.money))

                
                    
        if command_list[0]=='pay':
            if type(command_list[1])=="int":
                player.pay(command_list[1])
                print("You have %d dollars now."%player.money)
            elif command_list[1]=="land":
                tax=200*len(player.lands)
                player.pay(tax)
                print("You have %d lands. You pay %d money. You have %d dollars now."%(len(player.lands),tax,player.money))
            elif command_list[1]=="land,house":
                tax=200*len(player.lands)
                count=0
                print(player.lands)
                house=player.lands
                print(type(house))
                for c in house.values():
                    tax+=100*c
                    count+=c
                player.pay(tax)
                print("You have %d lands and %d levels. You pay %d money. You have %d dollars now."%(len(player.lands),count,tax,player.money))
    if land_type(position)=="Destiny":
        import destiny
        a=random.randint(1,2)
        x=random.randint(1,4)
        y=random.randint(1,4)
        while x==y:
            y=random.randint(1,4)
        z=random.randint(1,4)
        while z==y or z==x:
            z=random.randint(1,4)
        number_list=[a,x,y,z]
        
        command_list=destiny.Destiny(number_list)

        print("Your destiny:","1:",command_list[0],"2:",command_list[3],"3:",command_list[6])
        if Test_mode==True:
            choice=1
        else:
            choice=input("Choose 1: 1 or 2 or 3:")
            while choice!="1" and choice!="2" and choice!="3":
                choice=input("Choose 1: 1 or 2 or 3:")
        choice=int(choice)
        if choice==1:
            if command_list[1]=='earn':
                player.earn(command_list[2])
                print("You have %d dollars now."%player.money)
            if command_list[1]=='pay':
                player.pay(command_list[2])
                print("You have %d dollars now."%player.money)
            if command_list[1]=='move':
                player.effect_earn("move",command_list[2])
                print("During next turn, you will move %d steps."%command_list[2])
        if choice==2:
            if command_list[4]=='earn':
                player.earn(command_list[5])
                print("You have %d dollars now."%player.money)
            if command_list[4]=='pay':
                player.pay(command_list[5])
                print("You have %d dollars now."%player.money)
            if command_list[4]=='move':
                player.effect_earn("move",command_list[5])
                print("During next turn, you will move %d steps."%command_list[5])
        if choice==3:
            if command_list[7]=='earn':
                player.earn(command_list[8])
                print("You have %d dollars now."%player.money)
            if command_list[7]=='pay':
                player.pay(command_list[8])
                print("You have %d dollars now."%player.money)
            if command_list[7]=='move':
                player.effect_earn("move",command_list[8])
                print("During next turn, you will move %d steps."%command_list[8])
            

    #破產判定
    
    for c in player_list:
        if c.money<0:
            print("%s is out!"%c.name)
            for x in range(0,len(land_owner)):
                if land_owner[x]==c.name:
                    land_owner.pop(x)
                    land_owner.insert(x,None)
                    land_level.pop(x)
                    land_level.insert(x,0)
                    print(land_owner)
                    print(land_level)
            for x in range(0,len(Player_list)):
                if Player_list[x]==c.name:
                    kill=True
                    kill_list.insert(0,Player_list[x])
            if kill==True:
                    
                for c in Player_list:
                    if c in kill_list:
                       Player_list.remove(c)     
                    
                kill=False
       
    if len(Player_list)==1:
        
        running=False
print("%s wins the game!"%(Player_list[0]))
pg.quit()

    
