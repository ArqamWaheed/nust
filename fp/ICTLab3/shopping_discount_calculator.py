# Task 1
print("Welcome to Python Lab 3!") 
# In the output I am seeing what i have written inside the print statement as a string

# Task 2
name = "Arqam Waheed"
cart_value = 1000 
discount = 10 # this is percentage
tax = 8 # this is percentage
print(f"Name: {name} \nCartValue: {cart_value} \nDiscount: {discount}% \nTax: {tax}%")

# Task 3
discount_amount = cart_value * discount / 100
tax_amount = cart_value * tax / 100
final_value = cart_value - discount_amount + tax_amount