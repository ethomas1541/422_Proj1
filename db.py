from pymongo import MongoClient

# MongoDB will run on port 27017 (generally reserved for Mongo; shouldn't cause conflict)
# Will need to change port number if/when I put this on ixdev
client = MongoClient(port=27017)
# Setup
db = client['database']
collection = db["collection"]

# Overwrite existing data, save whatever's in the dictionary on line 14
def save(arg: str) -> None:
    db.drop_collection(collection)
    collection.insert_one({
        "value": arg,
    })

# Return the data from the database, serialized (kinda messy, just proof of concept for now)
def load():
    print(list(collection.find()))

if __name__ == "__main__":
    print("Save")
    save("test")
    print("Load")
    load()