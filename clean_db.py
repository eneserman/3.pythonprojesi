import pymongo

# --- CONFIGURATION ---
# Ensure these match the settings in your pipelines.py
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "imdb_project"       # Your database name
COLLECTION_NAME = "top_movies" # Your collection name

def clean_database():
    try:
        # 1. Establish Connection
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # 2. Check Current Status
        count_before = collection.count_documents({})
        print(f"📡 Connected to: {DB_NAME} -> {COLLECTION_NAME}")
        print(f"📊 Current movie count: {count_before}")

        if count_before == 0:
            print("✅ Database is already empty. No action needed.")
            return

        # 3. Ask for Confirmation
        confirm = input("⚠️ WARNING: All data will be deleted! Are you sure? (y/n): ")
        
        if confirm.lower() == 'y':
            # 4. Perform Deletion
            result = collection.delete_many({})
            print(f"🗑️ Successfully deleted: {result.deleted_count} records.")
            print("✨ Database is now clean.")
        else:
            print("❌ Operation cancelled.")

    except Exception as e:
        print(f"🚨 An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    clean_database()