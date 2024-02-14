from pydantic import BaseModel

class ArticleBase(BaseModel):
    titre: str
    contenu: str | None = None
    auteur: str

class ArticleCreate(ArticleBase):
    pass

# Complete Article Schema (Pydantic Model)
class Article(ArticleBase):
    id: int

    class Config:
        orm_mode = True