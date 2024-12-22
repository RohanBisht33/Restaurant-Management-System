import pandas as pd
import csv
import random
import datetime
import atexit
import sys

# Define the menu items
menu = {
    "Starters": [
        {"name": "Samosa", "price": 20, "allergens": ["Gluten", "Nuts"]},
        {"name": "Soya Chaap", "price": 150, "allergens": ["Soy", "Nuts"]},
        {"name": "Paneer Tikka", "price": 200, "allergens": ["Dairy", "Nuts"]},
    ],
    "Main Course": [
        {"name": "Curry-Rice", "price": 250, "allergens": ["Soy","Gluten","Diary"]},
        {"name": "Rajma-Rice", "price": 300, "allergens": ["Diary","Gluten","Mustard"]},
        {"name": "Tandoori Roti-Shahi Paneer", "price": 400, "allergens": ["Gluten", "Dairy"]},
    ],
    "Desserts": [
        {"name": "Gulab Jamun", "price": 40, "allergens": ["Dairy","Nuts"]},
        {"name": "Ice Cream", "price": 60, "allergens": ["Dairy",]},
        {"name": "Rasmalai", "price": 100, "allergens": ["Dairy", "Nuts"]},
    ],
}
# Create a data frame of food items and prices, specifying the dtype for the allergens column
food_data = pd.read_csv("menu.csv", dtype={"allergens": str})

# Write the menu to a CSV file
with open("menu.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Food", "Price","allergens"])
    for category in menu:
        for food in menu[category]:
            allergens = ", ".join(food["allergens"])
            writer.writerow([food["name"], food["price"], allergens])
food_data = pd.read_csv("menu.csv", dtype={"allergens": str})

user_profiles = {}

# Define file paths for storing data
user_profiles_file = "user_profiles.csv"
order_history_file = "order_history.csv"

user_profile_headers = ["Username", "Name", "Contact Info"]
order_history_headers = ["Username", "Order Date", "Items Ordered", "Total Price"]

with open(user_profiles_file, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(user_profile_headers)

with open(order_history_file, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(order_history_headers)

# Initialize user_profiles and order_history from stored CSV files, if available
user_profiles = {}
order_history = []

def load_data():
    with open(user_profiles_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_profiles[row["Username"]] = {
                "Name": row["Name"],
                "Contact Info": row["Contact Info"]
            }

    with open(order_history_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_history.append(row)

# Load data at the beginning of the program
load_data()

def create_profile():
    username = input("Enter your username: ")
    if username in user_profiles:
        print("Profile already exists. Updating profile.")
    name = input("Enter your name: ")
    contact_info = input("Enter your contact information: ")
    # You can add more profile details here as needed
    user_profiles[username] = {"Name": name, "Contact Info": contact_info}

def access_profile():
    username = input("Enter your username to access your profile: ")
    if username in user_profiles:
        print("Welcome back, {}!".format(user_profiles[username]["Name"]))
        # Display other profile details here
        return username  # Return the username for later use
    else:
        print("Profile not found. Please create a new profile.")
        return None

def display_recommendation_and_allergens(order_items, food_data):
    recommendations = {
        1: "Our special Tandoori Roti-Shahi Paneer is a perfect choice to complement your order!",
        2: "Why not try our delicious Gulab Jamun for dessert? You won't regret it!",
        3: "Consider adding a refreshing Ice Cream to your order to complete your meal!",
        4: "Begin your culinary journey with the crispy and tantalizing Samosa starter.",
        5: "Indulge in Soya Chaap, grilled to perfection, a protein lover's dream.",
        6: "Delight in the creamy splendor of Rasmalai, a dessert that enchants the senses.",
        7: "Satisfy your hunger with a taste of home in our Curry-Rice main course.",
        8:  "Chill out with our Ice Cream, a refreshing dessert to sweeten your day.",
        9: "Conclude your meal on a sweet note with our heavenly Gulab Jamun dessert.",
        10: "Try our Paneer Tikka for a smoky and savory delight.",
        11: "Experience the sizzling delight of Paneer Tikka, a symphony of flavors."
    }

    # Display recommendations
    recommendation_choice = random.randint(1, 11)
    print("\nRecommendation for you:")
    print(recommendations[recommendation_choice])

    
    print("\nAllergen Information for Ordered Items:")
    for item, quantity in order_items.items():
        if item in food_data["Food"].values:
            row = food_data.loc[food_data["Food"] == item]
            allergens = ", ".join(str(x) for x in row["allergens"])
            print(f"{item} x{quantity} contains: {allergens}")
        else:
            print(f"{item} not found in the menu.")



# Get the current time
current_time = datetime.datetime.now()
current_hour = current_time.hour

# Determine the appropriate greeting based on the time of day
if 5 <= current_hour < 12:
    greeting = "Good morning"
elif 12 <= current_hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# Greet the customer
print(f"{greeting}! Welcome to Our Restaurant!")

# Initialize variables for user login
current_user = None
user_logged_in = False

# Modify your menu to include options for creating and accessing profiles
menu_with_profile = """
1. Create/Update Profile
2. Access Profile
3. Place an Order
4. Exit
Enter your choice (1-4): """

while True:
    choice = input(menu_with_profile)
    if choice == "1":
        create_profile()
    elif choice == "2":
        current_user = access_profile()
        if current_user:
            user_logged_in = True  # Set the login status to True
    elif choice == "3":
        if user_logged_in:
            break
        else:
            print("You must log in (option 2) before placing an order.")
    elif choice == "4":
        print("Thank you for visiting our restaurant. Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Please enter a valid option.")

# Create a form for the user to enter their order
order_form = """
What would you like to order?
For Starters:
1. Samosa
2. Soya Chaap
3. Paneer Tikka
Main Course(Combos):
4. Curry-Rice
5. Rajma-Rice
6. Tandoori Roti-Shahi Paneer
Desserts:
7. Gulab Jamun
8. Ice Cream
9. Rasmalai
Enter your choice (1-9): """

# Initialize the total price
total_price = 0

# Initialize a dictionary to store order items
order_items = {}

valid_choice = False
order_items_str = ""
while not valid_choice:
    try:
        choice = int(input(order_form))
        if choice not in range(1, 10):
            print("Invalid choice. Please enter a valid choice.")
            continue

        quantity = int(input("How many would you like to order? "))
        if quantity <= 0:
            print("Invalid quantity. Please enter a positive value.")
            continue

        # Get the price of the user's order
        food_price = food_data.loc[choice - 1, "Price"]
        food_name = food_data.loc[choice - 1, "Food"]
        
        # Add the items to the order dictionary
        if food_name in order_items:
            order_items[food_name] += quantity
        else:
            order_items[food_name] = quantity

        # Calculate the price for the current item
        item_price = food_price * quantity

        # Add the price of the current item to the total price
        total_price += item_price
        

        display_recommendation_and_allergens(order_items, food_data)
        
        while True:
            try:
                ch = int(input("Do you want to make another choice? (1 for yes, 0 for no): "))
                if ch == 0:
                    print("Thank you for your order!")
                    valid_choice = True
                    break
                elif ch == 1:
                    break
                else:
                    print("Invalid choice. Please enter a valid option (1 or 0).")
            except ValueError:
                print("Invalid input. Please enter a valid choice (numeric value).")
    except ValueError:
        print("Invalid input. Please enter a valid choice or quantity (numeric value).")
        continue

# Print the total price of the order
total_price_with_tax = total_price * 1.18
total_price_with_discount = total_price_with_tax * 0.8
print("The total price of your order is ₹{:.2f}".format(total_price_with_tax))
# Calculate the total price with tax
total_price_with_tax = total_price * 1.18

# Add the order details to the order history
order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
order_history.append({
    "Username": current_user,
    "Order Date": order_date,
    "Items Ordered": ", ".join([f"{item} x{quantity}" for item, quantity in order_items.items()]),
    "Total Price": total_price_with_tax
})

# Save the updated order history to the CSV file
with open(order_history_file, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        order_history[-1]["Username"],
        order_history[-1]["Order Date"],
        order_history[-1]["Items Ordered"],
        order_history[-1]["Total Price"]
    ])



print("Would you like to 1) takeout or 2) dine in?")
while True:
    try:
        t = int(input("Enter the specified number: "))
        if t in (1, 2):
            break
        else:
            print("Invalid choice. Please enter a valid option.")
    except ValueError:
        print("Invalid input. Please enter a valid choice (numeric value).")

# Generate the receipt
print("\n*****************IP ELITES RESTAURANT**************")
print("********************** Receipt ********************")
print("\n***************************************************")
print("Items Ordered:")
total_price_without_tax = 0 
for item, quantity in order_items.items():
    item_price = food_data[food_data["Food"] == item]["Price"].values[0]
    item_total_price = item_price * quantity
    total_price_without_tax += item_total_price
    print(f"{item} x{quantity}- ₹{item_price}each (Total: ₹{item_total_price:.2f})")
print("\n***************************************************")
print(f"Total Price (before tax): ₹{total_price_without_tax:.2f}")
print(f"Total Price (including tax): ₹{total_price_with_tax:.2f}")
if total_price_without_tax > 1000:
    print(f"Total Price (including tax and 20% discount): ₹{total_price_with_discount:.2f}")

print("Thanks For Visiting Us, Feel Free to Visit Again")
print("***************************************************")
if t == 1:
    print("Food is ready for takeout! Enjoy your meal! Visit Again")
else:
    print("Your food is served hot! Enjoy before it gets cold!")
    print("Thank you for ordering. Feel free to order again!")

def save_data():
    with open(user_profiles_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(user_profile_headers)
        for username, profile in user_profiles.items():
            writer.writerow([username, profile["Name"], profile["Contact Info"]])

    with open(order_history_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(order_history_headers)
        for order in order_history:
            writer.writerow([
                order["Username"],
                order["Order Date"],
                order["Items Ordered"],
                order["Total Price"]
            ])

atexit.register(save_data)
