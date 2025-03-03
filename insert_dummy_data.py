import sqlite3

# Connect to database
conn = sqlite3.connect('pharmacy.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS medicines
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              manufacturer TEXT,
              price REAL,
              quantity INTEGER,
              category TEXT)''')

# Sample Pakistani medicines data
medicines = [
    ("Panadol", "GSK Pakistan", 20.50, 100, "Pain Relief"),
    ("Brufen", "Abbott Pakistan", 25.75, 150, "Pain Relief"),
    ("Risek", "Getz Pharma", 180.00, 50, "Gastric"),
    ("Flagyl", "Sanofi Pakistan", 65.00, 58, "Antibiotics"),
    ("Augmentin", "GSK Pakistan", 250.00, 80, "Antibiotics"),
    ("Disprin", "Reckitt Pakistan", 15.00, 200, "Pain Relief"),
    ("Calpol", "GSK Pakistan", 30.00, 90, "Pain Relief"),
    ("Nexum", "Getz Pharma", 170.00, 45, "Gastric"),
    ("Septran", "GSK Pakistan", 85.00, 70, "Antibiotics"),
    ("Ponstan", "Pfizer Pakistan", 40.00, 120, "Pain Relief"),
    ("Motilium", "Johnson & Johnson", 95.00, 60, "Gastric"),
    ("Zantac", "GSK Pakistan", 120.00, 40, "Gastric"),
    ("Amoxil", "GSK Pakistan", 160.00, 85, "Antibiotics"),
    ("Cifran", "Sami Pharmaceuticals", 145.00, 55, "Antibiotics"),
    ("Rigix", "Getz Pharma", 45.00, 75, "Pain Relief"),
    ("Calamox", "Bosch Pharmaceuticals", 280.00, 65, "Antibiotics"),
    ("Nospa", "Sanofi Pakistan", 55.00, 110, "Pain Relief"),
    ("Gravinate", "Abbott Pakistan", 35.00, 95, "Other"),
    ("Lexotanil", "Roche Pakistan", 190.00, 40, "Other"),
    ("Arinac", "GSK Pakistan", 75.00, 130, "Pain Relief"),
    ("Rashish", "GSK Pakistan", 75.00, 130, "Remove Rash")

]

# Insert data
c.executemany("""
    INSERT INTO medicines (name, manufacturer, price, quantity, category)
    VALUES (?, ?, ?, ?, ?)
""", medicines)

# Commit and close
conn.commit()
conn.close()

print("Sample data has been inserted successfully!")
