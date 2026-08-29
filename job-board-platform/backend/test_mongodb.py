from pymongo import MongoClient
import ssl

# Your connection string
uri = "mongodb://kamranAK:hggqOSoptchg1VYk@ac-zm1w0v6-shard-00-00.nnk56el.mongodb.net:27017,ac-zm1w0v6-shard-00-01.nnk56el.mongodb.net:27017,ac-zm1w0v6-shard-00-02.nnk56el.mongodb.net:27017/onjob?ssl=true&authSource=admin"

print("Testing direct connection...")

try:
    # Disable DNS resolution by using direct IPs
    client = MongoClient(uri, serverSelectionTimeoutMS=10000, directConnection=False)
    client.admin.command('ping')
    print("✅ Connected successfully!")
    
    db = client['onjob']
    collections = db.list_collection_names()
    print(f"Collections: {collections}")
    
    if 'jobs' in collections:
        count = db.jobs.count_documents({})
        print(f"Total jobs: {count}")
        
except Exception as e:
    print(f"Error: {e}")
    
    # Try alternative: Use directConnection=True
    print("\nTrying with directConnection=True...")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=10000, directConnection=True)
        client.admin.command('ping')
        print("✅ Connected with directConnection!")
    except Exception as e2:
        print(f"Still failing: {e2}")