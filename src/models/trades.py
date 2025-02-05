from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from utils.database import Base

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    pair = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Trade {self.pair} {self.amount} @ {self.price}>'
