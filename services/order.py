from beanie import Document
from beanie import PydanticObjectId
from pydantic import Field
from datetime import datetime

class Dish(Document):
    user_id: PydanticObjectId
    kitchen_id: PydanticObjectId
    dish_id: PydanticObjectId
    reservation_time: datetime
    number_of_people: int
    total_price: int
    status: int
    created_at: datetime
    
    class Settings:
        collection = "order"
        
    def to_dict(self):
        d = {}
        for k, v in self.dict().items():
            # convert ObjectId to str
            if k == 'id':
                d['id'] = str(v)
            else:
                d[k] = v
        return d