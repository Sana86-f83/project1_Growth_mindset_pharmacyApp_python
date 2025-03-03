import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('pharmacy.db')
c = conn.cursor()

# Get all medicine IDs and their prices
medicines = c.execute("SELECT id, price FROM medicines").fetchall()

# Clear existing sales data
c.execute("DELETE FROM sales")

# Generate sales data for the last 7 days
for day in range(7):
    sale_date = datetime.now() - timedelta(days=day)
    
    # Generate 3-8 sales per day
    for _ in range(random.randint(3, 8)):
        medicine = random.choice(medicines)
        medicine_id = medicine[0]
        price = medicine[1]
        quantity = random.randint(1, 5)
        total_price = price * quantity
        
        c.execute("""
            INSERT INTO sales (medicine_id, quantity, total_price, sale_date)
            VALUES (?, ?, ?, ?)
        """, (medicine_id, quantity, total_price, sale_date.date()))

conn.commit()
conn.close()

print("Sample sales data has been inserted successfully!") 