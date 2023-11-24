"""database.py
    """
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS = 3000)
DATABASE = None

# Send a ping to confirm a successful connection
client.admin.command('ping')
DATABASE = client[os.getenv('MONGODB_DATABASE')]
print("Pinged your deployment. You successfully connected to MongoDB!")
