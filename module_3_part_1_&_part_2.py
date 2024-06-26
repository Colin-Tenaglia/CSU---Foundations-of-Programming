# -*- coding: utf-8 -*-
"""Module 3: Part 1 & Part 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gQmtErtlUDZMwrFBoj8F8xo4zqYmTLzg

##**Part 1 - Pseudocode**

###START

  - PROMPT user to "Please enter the charge for the food" and store their input in food_charge
  - CALCULATE tip_amount as food_charge (user input) multiplied by 0.18
  - CALCULATE sales_tax as food_charge (user input) multiplied by 0.07
  - CALCULATE total_price as the sum of food_charge, tip_amount, and sales_tax
  - DISPLAY "Food Charge: ", food_charge
  - DISPLAY "Tip (18%): ", tip_amount
  - DISPLAY "Sales Tax (7%): ", sales_tax
  - DISPLAY "Total Price: ", total_price

###END

##**Part 1 - Code**
"""

# Part 1: Meal Purchase Calculation Code

# Ask the user to enter the charge for the food
food_charge = float(input("Please enter the charge for the food: $"))

# Calculate the tip and tax
tip_amount = food_charge * 0.18
sales_tax = food_charge * 0.07

# Calculate the total price
total_price = food_charge + tip_amount + sales_tax
20
# Display the amounts
print(f"\nFood Charge: ${food_charge:.2f}")
print(f"Tip (18%): ${tip_amount:.2f}")
print(f"Sales Tax (7%): ${sales_tax:.2f}")
print(f"Total Price: ${total_price:.2f}")

"""##**Part 2 - Pseudocode**

###START
  - PROMPT user for current time "What is the current time (in hours, 24-hour format)?" and store in current_time
  - PROMPT user for hours to wait "How many hours should the alarm wait?" and store in hours_to_wait
  - CALCULATE alarm_time as (current_time + hours_to_wait) - future time alarm will go off in 24 hr
  - DISPLAY "The alarm will go off at ", alarm_time, ":00."

###END

##**Part 2 - Code**
"""

# Part 2: 24-Hour Clock Alarm

# Ask the user for the current time and hours to wait for the alarm
current_time = int(input("What is the current time (in hours, 24-hour format)? "))
hours_to_wait = int(input("How many hours should the alarm wait? "))

# Calculate the alarm time
alarm_time = (current_time + hours_to_wait) % 24

# Display the result
print(f"The alarm will go off at {alarm_time}:00.")