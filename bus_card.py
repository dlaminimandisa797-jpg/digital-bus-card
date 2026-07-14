import json
from datetime import datetime

# Weekly/Monthly ticket prices
TICKET_PRICES = {
    "weekly": 100.00,
    "monthly": 350.00,
    "single_trip": 15.00
}

class BusCard:
    def __init__(self, card_id, balance=0.0):
        self.card_id = card_id
        self.balance = balance
        self.ticket_type = "pay_as_you_go"  # or "weekly", "monthly"
        self.ticket_expiry = None
        self.transaction_history = []
    
    # CRUD: READ
    def display_info(self):
        print(f"\n--- Card {self.card_id} ---")
        print(f"Balance: R{self.balance:.2f}")
        print(f"Ticket: {self.ticket_type}")
        if self.ticket_expiry:
            print(f"Ticket expires: {self.ticket_expiry}")
    
    # Top-up/Fare Deduction
    def top_up(self, amount):
        self.balance += amount
        self.add_transaction("Top Up", amount)
        print(f"Top up successful! New balance: R{self.balance:.2f}")
    
    def tap(self):
        fare = TICKET_PRICES["single_trip"]
        # Check if they have active weekly/monthly ticket
        if self.ticket_type in ["weekly", "monthly"]:
            if self.ticket_expiry and datetime.now() < self.ticket_expiry:
                self.add_transaction("Tap - Ticket Active", 0)
                print("Tap successful! Ticket active. No charge.")
                return
        
        # Otherwise deduct single fare
        if self.balance >= fare:
            self.balance -= fare
            self.add_transaction("Bus Fare", -fare)
            print(f"Tap successful! Fare: R{fare}. New balance: R{self.balance:.2f}")
        else:
            print("Not enough money. Please top up.")
    
    # Link/Manage Bus Ticket
    def buy_ticket(self, ticket_type):
        if ticket_type not in ["weekly", "monthly"]:
            print("Invalid ticket type")
            return
        
        price = TICKET_PRICES[ticket_type]
        if self.balance >= price:
            self.balance -= price
            self.ticket_type = ticket_type
            
            # Set expiry date
            if ticket_type == "weekly":
                days = 7
            else:
                days = 30
            self.ticket_expiry = datetime.now().replace(hour=23, minute=59) # simplified
            
            self.add_transaction(f"{ticket_type.title()} Ticket", -price)
            print(f"{ticket_type.title()} ticket bought for R{price}!")
            print(f"Digital Receipt: Card {self.card_id} | {ticket_type} | R{price} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"Not enough balance. Need R{price}")
    
    # Transaction history
    def add_transaction(self, description, amount):
        self.transaction_history.append({
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "description": description,
            "amount": amount,
            "balance": self.balance
        })
    
    def show_history(self):
        print(f"\n--- Transaction History for {self.card_id} ---")
        if not self.transaction_history:
            print("No transactions yet")
        for t in self.transaction_history:
            print(f"{t['date']} | {t['description']} | R{t['amount']:.2f} | Balance: R{t['balance']:.2f}")


# CRUD Manager - manages multiple cards
class CardSystem:
    def __init__(self):
        self.cards = {}
    
    # CRUD: CREATE
    def create_card(self, card_id):
        if card_id in self.cards:
            print("Card already exists")
        else:
            self.cards[card_id] = BusCard(card_id)
            print(f"Card {card_id} created!")
    
    # CRUD: READ
    def get_card(self, card_id):
        return self.cards.get(card_id)
    
    # CRUD: UPDATE - handled by methods inside BusCard
    
    # CRUD: DELETE
    def delete_card(self, card_id):
        if card_id in self.cards:
            del self.cards[card_id]
            print(f"Card {card_id} deleted")
        else:
            print("Card not found")
    
    # Display prices
    def display_prices(self):
        print("\n--- Ticket Prices ---")
        print(f"Single Trip: R{TICKET_PRICES['single_trip']}")
        print(f"Weekly Pass: R{TICKET_PRICES['weekly']}")
        print(f"Monthly Pass: R{TICKET_PRICES['monthly']}")


# ===== INTERACTIVE MENU FOR USER =====
system = CardSystem()

while True:
    print("\n========== DIGITAL BUS CARD ==========")
    print("1. Create new card")
    print("2. Top Up")
    print("3. Tap Bus")
    print("4. Buy Weekly/Monthly Ticket")
    print("5. View Card Info")
    print("6. View Transaction History")
    print("7. View Prices")
    print("8. Delete Card")
    print("9. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        card_id = input("Enter new Card ID: ")
        system.create_card(card_id)
    
    elif choice == "2":
        card_id = input("Enter Card ID to top up: ")
        card = system.get_card(card_id)
        if card:
            amount = float(input("Enter amount to top up: R"))
            card.top_up(amount)
        else:
            print("Card not found")
    
    elif choice == "3":
        card_id = input("Enter Card ID to tap: ")
        card = system.get_card(card_id)
        if card:
            card.tap()
        else:
            print("Card not found")
    
    elif choice == "4":
        card_id = input("Enter Card ID: ")
        card = system.get_card(card_id)
        if card:
            system.display_prices()
            ticket = input("Enter ticket type: weekly / monthly: ").lower()
            card.buy_ticket(ticket)
        else:
            print("Card not found")
    
    elif choice == "5":
        card_id = input("Enter Card ID: ")
        card = system.get_card(card_id)
        if card:
            card.display_info()
        else:
            print("Card not found")
    
    elif choice == "6":
        card_id = input("Enter Card ID: ")
        card = system.get_card(card_id)
        if card:
            card.show_history()
        else:
            print("Card not found")
    
    elif choice == "7":
        system.display_prices()
    
    elif choice == "8":
        card_id = input("Enter Card ID to delete: ")
        system.delete_card(card_id)
    
    elif choice == "9":
        print("Goodbye!")
        break
    
    else:
        print("Invalid choice. Try again.")