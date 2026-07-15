import json
import os
from datetime import datetime
import getpass # to hide password input

DATA_FILE = "cards.json"
FARE = 15.0

# --- LOAD & SAVE DATA ---
def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Upgrade old cards to new format
            for card_id, c in data.items():
                if "lastName" not in c: c["lastName"] = ""
                if "phone" not in c: c["phone"] = "N/A"
                if "password" not in c: c["password"] = "1234" # default for old cards
                if "status" not in c: c["status"] = "ACTIVE"
                if "history" not in c: c["history"] = []
            return data
    return {}

def save_cards(cards):
    with open(DATA_FILE, "w") as f:
        json.dump(cards, f, indent=4)

cards = load_cards()

# --- LOGIN MENU ---
def login_menu():
    while True:
        print("\n=================================")
        print("   DIGITAL BUS CARD SYSTEM")
        print("=================================")
        print("1. Create New Card")
        print("2. Sign In - I already have a card")
        print("3. Top Up Card")
        print("4. Get Virtual Card")
        print("5. Display History")
        print("6. Delete/Cancel Card")
        print("7. Exit System")
        print("=================================")
        
        choice = input("Choose an option: ")

        if choice == "1":
            create_card()
        elif choice == "2":
            sign_in()
        elif choice == "3":
            top_up_main()
        elif choice == "4":
            get_virtual_card()
        elif choice == "5":
            display_history()
        elif choice == "6":
            cancel_card()
        elif choice == "7":
            save_cards(cards)
            print("Thank you for using the Digital Bus Card System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# --- HELPER: LOGIN CHECK ---
def login(card_id):
    password = getpass.getpass("Enter Password: ")
    if card_id not in cards:
        print("Error: Card ID not found.")
        return None
    if cards[card_id]["status"] == "CANCELLED":
        print("Error: This card has been cancelled.")
        return None
    if cards[card_id]["password"] != password:
        print("Error: Wrong password.")
        return None
    return cards[card_id]

# --- CREATE NEW CARD ---
def create_card():
    print("\n--- CREATE NEW CARD ---")
    name = input("Enter your Name: ")
    lastName = input("Enter your Last Name: ")
    phone = input("Enter your Phone Number: ")
    password = getpass.getpass("Create Password: ")
    card_id = input("Create your Card ID: ")
    
    if card_id in cards:
        print("Error: Card ID already exists. Please sign in instead.")
        return
    
    # check if phone already used - FIXED
    for c in cards.values():
        if "phone" in c and c["phone"] == phone and c["phone"] != "N/A":
            print("Error: Phone number already registered.")
            return

    cards[card_id] = {
        "name": name, 
        "lastName": lastName,
        "phone": phone,
        "password": password,
        "balance": 0.0,
        "status": "ACTIVE",
        "history": [f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | CREATE | R0.00"]
    }
    save_cards(cards)
    print(f"\nSuccess! Card created for {name} {lastName}")
    print(f"Your Card ID is: {card_id}  <-- Remember this to sign in")
    bus_menu(card_id)

# --- SIGN IN ---
def sign_in():
    print("\n--- SIGN IN ---")
    card_id = input("Enter your Card ID: ")
    user = login(card_id)
    if user:
        print(f"Welcome back, {user['name']}!")
        bus_menu(card_id)

# --- TOP UP FROM MAIN MENU ---
def top_up_main():
    print("\n--- TOP UP CARD ---")
    card_id = input("Enter your Card ID: ")
    user = login(card_id)
    if user:
        top_up(card_id)

# --- GET VIRTUAL CARD ---
def get_virtual_card():
    print("\n--- GET VIRTUAL CARD ---")
    card_id = input("Enter your Card ID: ")
    user = login(card_id)
    if user:
        print("\n--- VIRTUAL CARD ---")
        print(f"Card ID: {card_id}")
        print(f"Name: {user['name']} {user['lastName']}")
        print(f"Phone: {user['phone']}")
        print(f"Balance: R{user['balance']:.2f}")
        print(f"Status: {user['status']}")
        print("--------------------")

# --- DISPLAY HISTORY ---
def display_history():
    print("\n--- DISPLAY HISTORY ---")
    card_id = input("Enter your Card ID: ")
    user = login(card_id)
    if user:
        print(f"\n--- TRANSACTION HISTORY FOR {user['name']} ---")
        if len(user["history"]) == 0:
            print("No transactions yet.")
        for record in user["history"]:
            print(record)
        print("--------------------")

# --- DELETE/CANCEL CARD ---
def cancel_card():
    print("\n--- CANCEL CARD ---")
    card_id = input("Enter your Card ID: ")
    user = login(card_id)
    if user:
        confirm = input("Are you sure? Type YES to confirm: ")
        if confirm == "YES":
            cards[card_id]["status"] = "CANCELLED"
            cards[card_id]["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | CANCEL | R0.00")
            save_cards(cards)
            print("Card has been cancelled.")
        else:
            print("Cancellation aborted.")

# --- MAIN BUS MENU ---
def bus_menu(card_id):
    while True:
        user = cards[card_id]
        print(f"\n--- WELCOME {user['name'].upper()} ---")
        print(f"Card ID: {card_id} | Balance: R{user['balance']:.2f}")
        print("--------------------------")
        print("1. Top-up Card")
        print("2. Tap to Ride - R15.00")
        print("3. View Balance & Details")
        print("4. Logout")
        print("--------------------------")
        
        choice = input("Choose an option: ")

        if choice == "1":
            top_up(card_id)
        elif choice == "2":
            tap(card_id)
        elif choice == "3":
            view_balance(card_id)
        elif choice == "4":
            save_cards(cards)
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- TOP UP ---
def top_up(card_id):
    try:
        amount = float(input("Enter amount to top-up: R"))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
        if amount < 10:
            print("Minimum top-up amount is R10.00")
            return
        if cards[card_id]["status"] == "CANCELLED":
            print("Cannot top up. This card is cancelled.")
            return
        cards[card_id]["balance"] += amount
        cards[card_id]["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | TOP_UP | R{amount:.2f}")
        save_cards(cards)
        print(f"Top-up successful! New balance: R{cards[card_id]['balance']:.2f}")
    except ValueError:
        print("Invalid amount. Please enter a number.")

# --- TAP TO RIDE ---
def tap(card_id):
    if cards[card_id]["status"] == "CANCELLED":
        print("This card is cancelled.")
        return
    if cards[card_id]["balance"] >= FARE:
        cards[card_id]["balance"] -= FARE
        cards[card_id]["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | TAP | R{FARE:.2f}")
        save_cards(cards)
        print(f"Tap successful! R{FARE:.2f} deducted.")
        print(f"Remaining balance: R{cards[card_id]['balance']:.2f}")
    else:
        print(f"Insufficient balance. You need at least R{FARE:.2f} to tap.")

# --- VIEW BALANCE ---
def view_balance(card_id):
    user = cards[card_id]
    print("\n--- CARD DETAILS ---")
    print(f"Name: {user['name']} {user['lastName']}")
    print(f"Phone: {user['phone']}")
    print(f"Card ID: {card_id}")
    print(f"Status: {user['status']}")
    print(f"Current Balance: R{user['balance']:.2f}")
    print("--------------------")

# --- RUN THE PROGRAM ---
if __name__ == "__main__":
    login_menu()