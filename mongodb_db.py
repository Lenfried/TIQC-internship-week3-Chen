from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from datetime import datetime

class MongoDBDatabase:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
        self.create_indexes()
    
    def connect(self):
        """Establish connection to MongoDB database"""
        try:
            self.client = MongoClient(
                host=MONGODB_HOST,
                port=MONGODB_PORT,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[MONGODB_DATABASE]
            self.collection = self.db['graphics_cards']
            print(f"Connected to MongoDB database: {MONGODB_DATABASE}")
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        try:
            # Create indexes on commonly queried fields
            self.collection.create_index("manufacturer")
            self.collection.create_index("memory_gb")
            self.collection.create_index("price_usd")
            self.collection.create_index("name")
            print("MongoDB indexes created successfully")
        except Exception as e:
            print(f"Error creating indexes: {e}")
    
    def create(self, data):
        """Create a new graphics card document"""
        try:
            # Add timestamps
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()
            
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating document: {e}")
            raise
    
    def read_all(self, filters=None):
        """Read graphics cards with optional search and filters.
        filters: dict with optional keys: search, manufacturer, memory_type,
                 memory_min, memory_max, price_min, price_max
        """
        try:
            query = {}
            if filters:
                if filters.get('search'):
                    from bson.regex import Regex
                    term = filters['search'].strip()
                    if term:
                        query['$or'] = [
                            {'name': Regex(term, 'i')},
                            {'manufacturer': Regex(term, 'i')},
                            {'model': Regex(term, 'i')}
                        ]
                if filters.get('manufacturer'):
                    query['manufacturer'] = filters['manufacturer']
                if filters.get('memory_type'):
                    query['memory_type'] = filters['memory_type']
                mem_min = filters.get('memory_min')
                mem_max = filters.get('memory_max')
                if mem_min is not None or mem_max is not None:
                    query['memory_gb'] = {}
                    if mem_min is not None:
                        query['memory_gb']['$gte'] = int(mem_min)
                    if mem_max is not None:
                        query['memory_gb']['$lte'] = int(mem_max)
                price_min = filters.get('price_min')
                price_max = filters.get('price_max')
                if price_min is not None or price_max is not None:
                    price_cond = {}
                    if price_min is not None:
                        price_cond['$gte'] = float(price_min)
                    if price_max is not None:
                        price_cond['$lte'] = float(price_max)
                    query.setdefault('$and', []).append(
                        {'$or': [{'price_usd': price_cond}, {'price_usd': None}]}
                    )
            cursor = self.collection.find(query).sort('_id', -1)
            cards = []
            for doc in cursor:
                doc['id'] = str(doc['_id'])
                del doc['_id']
                if 'created_at' in doc:
                    doc['created_at'] = doc['created_at'].isoformat()
                if 'updated_at' in doc:
                    doc['updated_at'] = doc['updated_at'].isoformat()
                cards.append(doc)
            return cards
        except Exception as e:
            print(f"Error reading documents: {e}")
            raise
    
    def read_one(self, card_id):
        """Read a single graphics card by ID"""
        try:
            from bson import ObjectId
            doc = self.collection.find_one({'_id': ObjectId(card_id)})
            if doc:
                doc['id'] = str(doc['_id'])
                del doc['_id']
                # Convert datetime objects to strings
                if 'created_at' in doc:
                    doc['created_at'] = doc['created_at'].isoformat()
                if 'updated_at' in doc:
                    doc['updated_at'] = doc['updated_at'].isoformat()
            return doc
        except Exception as e:
            print(f"Error reading document: {e}")
            raise
    
    def update(self, card_id, data):
        """Update a graphics card document"""
        try:
            from bson import ObjectId
            # Add updated_at timestamp
            data['updated_at'] = datetime.utcnow()
            
            result = self.collection.update_one(
                {'_id': ObjectId(card_id)},
                {'$set': data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating document: {e}")
            raise
    
    def delete(self, card_id):
        """Delete a graphics card document"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({'_id': ObjectId(card_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
