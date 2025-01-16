import json
from sqlalchemy import Column, Integer, String, ARRAY
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    interests = Column("interests", String)  # Storing interests as a JSON string instead of ARRAY as ARRAY not supported by SQLite
    
    def set_interests(self, interests_list):
        self.interests = json.dumps(interests_list)  

    def get_interest(self):
        return json.loads(self.interests) if self.interests else []  # Retrieve the list from the JSON string
    
    def get_user(self):
        
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender":self.gender,
            "email": self.email,
            "city": self.city,
            "interests": self.get_interest()
        }
