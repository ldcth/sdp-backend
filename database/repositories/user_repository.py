from bson import ObjectId
from pymongo.errors import OperationFailure
from database.connect import database
from database.models.user import User
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.db = database['users']

    def save_to_db(self, user: User):
        try:
            if user._id != None:
                user.updatedAt = datetime.utcnow()
                obj_dict = user.__dict__.copy()
                obj_dict.pop('_id', None)
                result = self.db.find_one_and_update({"_id": ObjectId(user._id)},
                                                {"$set": obj_dict})
            else:
                obj_dict = user.__dict__.copy()
                obj_dict.pop('_id', None)
                result = self.db.insert_one(obj_dict)
                user._id = str(result.inserted_id)
                return result.inserted_id
        except OperationFailure as e:
            print(f"Error save to database: {e}")
            return None

    def find_by_id(self,user: User, id) -> User:
        try:
            result = self.db.find_one({"_id": ObjectId(id)})
            if result:
                result['_id'] = str(result['_id'])
                user._id = str(result['_id'])
                user.role = result['role']
                user.name = result['name']
                user.histories = result['histories']
                user.email = result['email']
                user.password = result['password']
                user.createdAt = result['createdAt']
                user.updatedAt = result['updatedAt']
            else:
                return None
        except OperationFailure as e:
            print(f"Error finding settings: {e}")
            return None

    def find_by_email(self, email) -> User:
        try:
            result = self.db.find_one({"email": email})
            if result:
                return self._map_to_user(result)
            return None
        except OperationFailure as e:
            print(f"Error finding user: {e}")
            return None

    def get_all_users(self):
        try:
            result = self.db.find({"role": 1})
            if result:
                result = list(result)
                for item in result:
                    item["_id"] = str(item['_id'])
                return result
            else:
                return []
        except OperationFailure as e:
            print(f"Error finding settings: {e}")
            return False    

    def get_total(self):
        try:
            return self.db.count_documents({"role": 1})
        except OperationFailure as e:
            print(f"Error counting users: {e}")
            return 0
    def delete_by_id(self, id):
        try:
            self.db.delete_one({"_id": ObjectId(id)})
            return True
        except OperationFailure as e:
            print(f"Error deleting user: {e}")
            return False

    def _map_to_user(self, data) -> User:
        user = User(
            role=data['role'],
            name=data['name'],
            email=data['email'],
            password=data['password'],
            histories=data['histories']
        )
        user._id = str(data['_id'])
        return user 