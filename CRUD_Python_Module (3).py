# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'SNHU123'  # Change this to your actual password
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def get_next_record_number(self):
        """
        Finds the current highest record number in the collection and returns the next number.
        Returns: integer - next available record number
        """
        try:
            # Sort by 'record_number' descending and get the first document
            last_record = self.collection.find().sort("record_number", -1).limit(1)
            last_record_list = list(last_record)
            if last_record_list:
                return last_record_list[0]["record_number"] + 1
            else:
                return 1  # if collection is empty, start at 1
        except Exception as e:
            print("Error getting next record number:", e)
            return 1  # default to 1 if something goes wrong

    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """
        Inserts a document into the animals collection.
        Input: data - dictionary containing key/value pairs for the document
        Returns: True if insert successful, False if failed
        """
        if data is not None: 
            try:
                # Optionally assign a record_number to document
                data["record_number"] = self.get_next_record_number()
                self.collection.insert_one(data)  # data should be dictionary
                return True
            except Exception as e:
                print("Error inserting document:", e)
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, query):
        """
        Queries documents from the animals collection.
        Input: query - dictionary specifying key/value pairs to search for
        Returns: list of documents if successful, empty list if none found or error
        """
        if query is not None:
            try:
                cursor = self.collection.find(query)  # returns a cursor
                results = list(cursor)  # convert cursor to list of documents
                return results
            except Exception as e:
                print("Error reading documents:", e)
                return []
        else:
            print("Query parameter is empty")
            return []

    # Create method to implement the U in CRUD
    def update(self, query, update_data):
        """
        Updates document(s) in the animals collection.
        Input: 
            query - dictionary specifying which documents to update
            update_data - dictionary of fields to update
        Returns: number of documents modified
        """
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_many(query, {"$set": update_data})
                return result.modified_count
            except Exception as e:
                print("Error updating documents:", e)
                return 0
        else:
            print("Query or update_data is empty")
            return 0

    # Create method to implement the D in CRUD
    def delete(self, query):
        """
        Deletes document(s) from the animals collection.
        Input: query - dictionary specifying which documents to delete
        Returns: number of documents deleted
        """
        if query is not None:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print("Error deleting documents:", e)
                return 0
        else:
            print("Query parameter is empty")
            return 0
