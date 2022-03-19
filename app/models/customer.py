import datetime
from typing import Optional

from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import HashModel, NotFoundError
from pydantic import EmailStr


class Customer(HashModel):
    first_name: str
    last_name: str
    email: EmailStr
    join_date: datetime.date
    age: int
    bio: Optional[str]

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )
