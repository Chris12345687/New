def sentence_transforming():
    # Get original sentence
    original = input("Enter the original sentence that you're required to rewrite:\n")
    
    if not isinstance(original, str) or original.strip() == "":
        print("Please enter a valid sentence (text only)!")
        return
    
    # Ask if there's a hint
    try:
        hint_choice = int(input("Did you get any hint?\nEnter 1 for YES, 2 for NO:\n"))
    except ValueError:
        print("Invalid input! Please enter 1 or 2.")
        return

    # Based on the user's choice, generate the prompt
    print("-" * 50)
    if hint_choice == 1:
        hint = input("Please enter the hint you got:\n")
        print(f"Hey, I need your help with rewriting sentences to keep them with the same meaning.")
        print(f"Please rewrite this sentence: \"{original}\" with the help of the following hint:\n\"{hint}\"")
    elif hint_choice == 2:
        print(f"Hey, I need your help with rewriting sentences to keep them with the same meaning.")
        print(f"Please rewrite this sentence: \"{original}\" to another one with the same meaning. There is no hint from the question, so try your best!")
    else:
        print("Invalid choice. Please enter 1 or 2.")

        return
    
    print("-" * 50)
    print("This is the sentence you should copy-paste to the AI now. Have fun!")

def word_form():
    print("You chose Word Form – this part is under construction!")

# Main Menu
print("Welcome to Make AI Understand You App!\n")
print("We are here to give you 2 options:")
print("1. Sentence Transforming")
print("2. Word Form")

choice = input("Please choose 1 or 2:\n")

if choice == "1":
    sentence_transforming()
elif choice == "2":
    word_form()
else:
    print("Invalid choice. Please enter 1 or 2.")
