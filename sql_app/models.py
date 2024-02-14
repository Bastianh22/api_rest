from sqlalchemy import Column, Integer, String
from .database import Base

# Define To Do class inheriting from Base
class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    titre = Column(String, index=True)
    contenu = Column(String, index=True)
    auteur = Column(String, index=True)