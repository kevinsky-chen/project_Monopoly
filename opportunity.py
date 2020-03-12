#Opportunity
import random
def Opportunity(rank):
    x=random.randint(1,4)
    #x=random.randint(1,10)#之後根據情況，會追加更多機會卡
    if x==1:
        print('''You get 1000 dollars!
If you have the least money of all players, get 1000 more.''')
        command='earn'
        if rank=="last":
            value=2000
        else:
            value=1000
        command_list=[command,value]
        
        return command_list     
                    
    elif x==2:
        print('''You lose 1000 dollars!
If you have the most money of all players, lose 1000 more.''')
        command='pay'
        if rank=="first":
            value=2000
        else:
            value=1000
        command_list=[command,value]
        
        return command_list  
        
    elif x==3:
        print('''The economy is very good!
You earn money from your lands!(200 $ for each)
If you have the least money of all players, you can also earn from houses.(100 $ for each level)''')
        command="earn"
        if rank=="last":
            string="land,house"
        else:
            string="land"
        command_list=[command,string]
        return command_list
        
    elif x==4:
        print('''The government asks you to pay the tax!
You pay money because of your lands!(200 $ for each)
If you have the most money of all players, you also pay money because of houses.(100 $ for each level)''')
        command="pay"
        if rank=="first":
            string="land,house"
        else:
            string="land"
        command_list=[command,string]
        return command_list
        
    #elif x==5:
        
    #elif x==6:
        
    #elif x==7:
        
    #elif x==8:
        
    #elif x==9:
        
    #else:
    
