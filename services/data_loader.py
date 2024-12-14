import pandas as pd
from pymongo import MongoClient

def load_data_to_mongo(csv_file, db_name, collection_name):
    # MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]

    # Load CSV data
    data = pd.read_csv(csv_file)

    # Convert DataFrame to dictionary and insert into MongoDB
    records = data.to_dict(orient="records")
    collection.insert_many(records)
    print(f"Inserted {len(records)} records into the '{collection_name}' collection.")

# Run this script to load data
if __name__ == "__main__":
    load_data_to_mongo("config/data/preprocessed_data.csv", "synthetic_data", "profiles")
