import random

from faker import Faker
from pymongo import MongoClient

fake = Faker()
client = MongoClient('mongodb://localhost:27017/')
db = client['admin']

users_collection = db['users']
products_collection = db['products']
browsing_history_collection = db['browsing_history']
purchase_history_collection = db['purchase_history']

# Delete all records in each collection
for collection_name in ["users", "products", "browsing_history", "purchase_history"]:
    collection = db[collection_name]
    result = collection.delete_many({})
    print(result.deleted_count, " records deleted in collection: ", collection_name)

products_name = [

    'Laptop', 'Phone', 'Shoes', 'Watch', 'Camera', 'Backpack', 'Headphones',
    'Tablet', 'Gaming Console', 'Smart Speaker', 'Electric Scooter',
    'Wireless Charger', 'Drone', 'Fitness Tracker', 'Smart Light', 'Air Purifier',
    'Smart Thermostat', 'Smart Lock', 'Bluetooth Speaker', 'E-Reader',
    'Portable Projector', 'Mechanical Keyboard', '3D Printer', 'Coffee Maker',
    'Blender', 'Juicer', 'Smart TV', 'Streaming Device', 'Action Camera',
    'VR Headset', 'Robot Vacuum', 'Electric Bike', 'Microwave', 'Smart Refrigerator',
    'Dishwasher', 'Smart Oven', 'Water Purifier', 'Electric Shaver', 'Hair Dryer',
    'Pressure Cooker', 'Toaster', 'Gaming Chair', 'Electric Toothbrush', 'Air Fryer',
    'Smart Mirror', 'Smart Scale', 'Home Security Camera', 'Smart Doorbell', 'Smart Plug',
    'Soundbar', 'Electric Kettle', 'Laptop Stand', 'Phone Case', 'Monitor',
    'Desk Lamp', 'Standing Desk', 'Office Chair', 'Electric Grill', 'Wireless Mouse',
    'Wireless Keyboard', 'Graphic Tablet', 'Video Doorbell', 'Portable Power Bank',
    'Action Camera Mount', 'Smart Bulb', 'Robot Dog', 'Streaming Microphone',
    'Smart Bed', 'Gaming Mouse', 'Smart Glasses', 'VR Gloves', 'Electric Skateboard',
    'Smart Air Conditioner', 'Standing Fan', 'Foot Massager', 'Electric Blanket',
    'Smart Mattress', 'Gaming Headset', 'Cordless Vacuum', 'Digital Camera', 'Smart Watch',
    'Automatic Pet Feeder', 'Noise-Cancelling Headphones', 'Tablet Case', 'Projector Screen',
    'Phone Charger', 'Wireless Earbuds', 'Smart Notebook', 'Smart Pen', 'Smart Mug',
    'Smart Wallet', 'Electric Massager', 'Ergonomic Pillow', 'Home Theater System',
    'Solar Power Bank', 'Portable Solar Panel', 'Smart Desk', 'Smart Bicycle Helmet',
    'Electric Guitar', 'Keyboard', 'Webcam', 'Portable SSD'
]

users = {}
for i in range(600):
    user_id = f"user_id_{i + 1}"
    users[user_id] = {
        "name": fake.first_name(),
        "age": random.randint(18, 70),
        "location": fake.city()
    }

users_collection.insert_many([{"_id": k, **v} for k, v in users.items()])

categories = ["Electronics", "Books", "Clothing", "Home", "Toys", "Sports"]
products = {}
for i in range(1400):
    product_id = f"product_id_{i + 1}"
    products[product_id] = {
        "name": random.choice(products_name),
        "category": random.choice(categories),
        "price": round(random.uniform(5, 2000), 2)
    }

products_collection.insert_many([{"_id": k, **v} for k, v in products.items()])

browsing_history = {}
for i in range(200000):
    user_id = random.choice(list(users.keys()))
    product_ids = random.sample(list(products.keys()), random.randint(1, 12))
    browsing_history[f"history_id_{i + 1}"] = {
        "user_id": user_id,
        "product_ids": product_ids
    }

browsing_history_collection.insert_many([{"_id": k, **v} for k, v in browsing_history.items()])

purchase_history = {}
for i in range(180000):
    user_id = random.choice(list(users.keys()))
    product_ids = random.sample(list(products.keys()), random.randint(1, 15))
    purchase_history[f"purchase_id_{i + 1}"] = {
        "user_id": user_id,
        "product_ids": product_ids
    }

purchase_history_collection.insert_many([{"_id": k, **v} for k, v in purchase_history.items()])

print("Data generation complete!")
