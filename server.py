from pymongo import MongoClient

client = MongoClient("mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("quiz_db")
records = db.quiz_records

print(records.count_documents({}))

