from pymongo import MongoClient

# MongoDB will run on port 27017 (generally reserved for Mongo; shouldn't cause conflict)
# Will need to change port number if/when I put this on ixdev
client = MongoClient(port=27017)
# Setup
db = client['database']
collection = db["collection"]

# Overwrite existing data, save whatever's in the dictionary on line 14
def save(name: str, note: str) -> None:
    # Overwrite old document with same name, if it exists
    if collection.find_one({"name": name}):
        collection.delete_one({"name": name})
    collection.insert_one({
        "name": name,
        "note": note
    })

# Return the data from the database, serialized (kinda messy, just proof of concept for now)
def load(name):
    print(list(collection.find({"name": name})))

if __name__ == "__main__":
    print("Save")
    save("test")
    print("Load")
    load()

# Users can have multiple notes
# Notes have name fields - saving into a note with a pre-existing name will OVERWRITE what's in there
# Notes also have text fields for storing the actual body of the note