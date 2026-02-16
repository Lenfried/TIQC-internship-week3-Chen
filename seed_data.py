"""
Script to seed sample graphics cards data into both MySQL and MongoDB databases
"""
from mysql_db import MySQLDatabase
from mongodb_db import MongoDBDatabase
from datetime import date

# Sample graphics cards data
sample_cards = [
    {
        'name': 'NVIDIA GeForce RTX 4090',
        'manufacturer': 'NVIDIA',
        'model': 'RTX 4090',
        'memory_gb': 24,
        'memory_type': 'GDDR6X',
        'core_clock_mhz': 2230,
        'boost_clock_mhz': 2520,
        'price_usd': 1599.00,
        'release_date': date(2022, 10, 12)
    },
    {
        'name': 'NVIDIA GeForce RTX 4080',
        'manufacturer': 'NVIDIA',
        'model': 'RTX 4080',
        'memory_gb': 16,
        'memory_type': 'GDDR6X',
        'core_clock_mhz': 2210,
        'boost_clock_mhz': 2505,
        'price_usd': 1199.00,
        'release_date': date(2022, 11, 16)
    },
    {
        'name': 'AMD Radeon RX 7900 XTX',
        'manufacturer': 'AMD',
        'model': 'RX 7900 XTX',
        'memory_gb': 24,
        'memory_type': 'GDDR6',
        'core_clock_mhz': 2300,
        'boost_clock_mhz': 2500,
        'price_usd': 999.00,
        'release_date': date(2022, 12, 13)
    },
    {
        'name': 'NVIDIA GeForce RTX 4070',
        'manufacturer': 'NVIDIA',
        'model': 'RTX 4070',
        'memory_gb': 12,
        'memory_type': 'GDDR6X',
        'core_clock_mhz': 1920,
        'boost_clock_mhz': 2475,
        'price_usd': 599.00,
        'release_date': date(2023, 4, 13)
    },
    {
        'name': 'AMD Radeon RX 7800 XT',
        'manufacturer': 'AMD',
        'model': 'RX 7800 XT',
        'memory_gb': 16,
        'memory_type': 'GDDR6',
        'core_clock_mhz': 2124,
        'boost_clock_mhz': 2430,
        'price_usd': 499.00,
        'release_date': date(2023, 9, 6)
    },
    {
        'name': 'NVIDIA GeForce RTX 3060',
        'manufacturer': 'NVIDIA',
        'model': 'RTX 3060',
        'memory_gb': 12,
        'memory_type': 'GDDR6',
        'core_clock_mhz': 1320,
        'boost_clock_mhz': 1777,
        'price_usd': 329.00,
        'release_date': date(2021, 2, 25)
    }
]

def seed_databases():
    """Seed both MySQL and MongoDB with sample data"""
    mysql_db = MySQLDatabase()
    mongodb_db = MongoDBDatabase()
    
    print("\n=== Seeding MySQL Database ===")
    mysql_count = 0
    for card in sample_cards:
        try:
            mysql_db.create(card)
            mysql_count += 1
            print(f"✓ Added to MySQL: {card['name']}")
        except Exception as e:
            print(f"✗ Error adding {card['name']} to MySQL: {e}")
    
    print(f"\n=== Seeding MongoDB Database ===")
    mongodb_count = 0
    for card in sample_cards:
        try:
            mongodb_db.create(card.copy())
            mongodb_count += 1
            print(f"✓ Added to MongoDB: {card['name']}")
        except Exception as e:
            print(f"✗ Error adding {card['name']} to MongoDB: {e}")
    
    print(f"\n=== Summary ===")
    print(f"MySQL: {mysql_count}/{len(sample_cards)} cards added")
    print(f"MongoDB: {mongodb_count}/{len(sample_cards)} cards added")
    
    mysql_db.close()
    mongodb_db.close()

if __name__ == '__main__':
    seed_databases()
