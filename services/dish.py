from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime


class Dish(Document):
    name: str
    description: str
    price: int
    image: str
    kitchen_id: PydanticObjectId
    created_at: datetime
    update_at: datetime
    
    class Settings:
        collection = "dish"
        
    def to_dict(self):
        d = {}
        for k, v in self.dict().items():
            # convert ObjectId to str
            if k == 'id':
                d['id'] = str(v)
            else:
                d[k] = v
        return d

