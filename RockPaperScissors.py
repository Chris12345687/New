import random
import time

def RockPaperScissors(PlayerChoice, BotChoice):
    if PlayerChoice == BotChoice:
        return f"Draw! You both chose {choice_map[PlayerChoice]}"
    elif (PlayerChoice == 1 and BotChoice == 2):  
        return "You won! The bot chose Scissors"
    elif (PlayerChoice == 2 and BotChoice == 3):
        return "You won! The bot chose Paper"
    elif (PlayerChoice == 3 and BotChoice == 1): 
        return "You won! The bot chose Rock"
    else:
        return f"You lost! The bot chose {choice_map[BotChoice]}"


choice_map = {
    1: "Rock",
    2: "Scissors",
    3: "Paper"
}

print("Welcome to Rock Paper Scissors!")
time.sleep(2)
print("-" * 50)
print("There will be a bot to play with you.")
time.sleep(2)


BotChoice = random.randint(1, 3)
PlayerChoice = int(input("Please Enter:\n1 for Rock\n2 for Scissors\n3 for Paper\n> "))
result = RockPaperScissors(PlayerChoice, BotChoice)
print(result)
