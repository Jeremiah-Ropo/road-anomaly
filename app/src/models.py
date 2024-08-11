from .mongo import mongo

def init_db():
    # Drop the existing email index if needed
    mongo.db.users.drop_index('email_1')
    # Create indexes
    mongo.db.users.create_index('email', unique=True)

    
    mongo.db.books.create_index('title', unique=True)

# Example functions to interact with the books and users collections

def create_user(user_data):
    return mongo.db.users.insert_one(user_data)

def create_book(book_data):
    return mongo.db.books.insert_one(book_data)

def get_users(query={}):
    return list(mongo.db.users.find(query))

def get_books(query={}):
    return mongo.db.books.find(query)
