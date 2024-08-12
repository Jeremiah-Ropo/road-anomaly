from .mongo import mongo

def init_db():
    if 'users' not in mongo.db.list_collection_names():
        mongo.db.create_collection('users')

    if 'roads' not in mongo.db.list_collection_names():
        mongo.db.create_collection('roads')

# Example functions to interact with the books and users collections

def create_user(user_data):
    return mongo.db.users.insert_one(user_data)

def create_book(book_data):
    return mongo.db.books.insert_one(book_data)

def create_book(book_data):
    return mongo.db.books.insert_one(book_data)

def get_users(query={}):
    return list(mongo.db.users.find(query))

def get_books(query={}):
    return mongo.db.books.find(query)
