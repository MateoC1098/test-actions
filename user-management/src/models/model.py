from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID



class Model():
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    def __init__(self):
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()