# check_db.py
from pymongo import MongoClient

def verify_data():
    """
    Connects to MongoDB and verifies the count and quality of scraped data.
    """
    # Connect to local MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["imdb_db"]
    collection = db["top_movies"] 
    
    # Count total documents
    count = collection.count_documents({})
    
    print("-" * 50)
    print(f"📂 Database:   imdb_db")
    print(f"📄 Collection: top_movies")
    print(f"🏆 TOTAL ELITE MOVIES: {count}")
    print(f"ℹ️  (Filtered by: Rating >= 8.0 & Votes >= 25,000)")
    print("-" * 50)
    
    if count > 0:
        print("✅ SAMPLE OF TOP 3 MOVIES:")
        # Sort by rating descending to show the best ones first
        cursor = collection.find().sort("rating", -1).limit(3)
        
        for doc in cursor:
            print(f" 🎬 {doc.get('title')} ({doc.get('year')})")
            print(f"    ⭐ Rating: {doc.get('rating')} | 🎬 Director: {doc.get('director')}")
            print(f"    🔗 {doc.get('url')}")
            print("-" * 20)
    else:
        print("❌ No data found. Please check your MongoDB connection.")

if __name__ == "__main__":
    verify_data()