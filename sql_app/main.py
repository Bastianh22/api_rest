from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, SessionLocal
from . import schemas
from . import models

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
  session = SessionLocal()
  try:
      yield session
  finally:
      session.close()

@app.get("/")
def root():
    return "Hello World"

@app.post("/article", response_model=schemas.Article, status_code=status.HTTP_201_CREATED)
def create_article(article: schemas.ArticleCreate, session: Session = Depends(get_session)):

  # create an instance of the Article database model
  articledb = models.Article(**article.dict())

  # add it to the session and commit it
  session.add(articledb)
  session.commit()
  session.refresh(articledb)

  return articledb

@app.get("/article/{id}", response_model=schemas.Article)
def read_article(id: int, session: Session = Depends(get_session)):

    # get the article item with the given id
    article = session.query(models.Article).get(id)

    # close the session
    session.close()

    if not article:
        raise HTTPException(status_code=404, detail=f"Article item with id {id} not found")

    return article

@app.put("/article/{id}")
def update_article(id: int, titre: str, contenu: str, auteur: str, session: Session = Depends(get_session)):

    # get the article item with the given id
    article = session.query(models.Article).get(id)

    # update article item with the given task (if an item with the given id was found)
    if article:
        article.titre = titre
        article.contenu = contenu
        article.auteur = auteur
        session.commit()

    # check if article item with given id exists. If not, raise exception and return 404 not found response
    if not article:
        raise HTTPException(status_code=404, detail=f"Article item with id {id} not found")

    return article

@app.delete("/article/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, session: Session = Depends(get_session)):

    # get the article item with the given id
    article = session.query(models.Article).get(id)

    # if article item with given id exists, delete it from the database. Otherwise raise 404 error
    if article:
        session.delete(article)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Article item with id {id} not found")

    return None

@app.get("/article", response_model = List[schemas.Article])
def read_article_list(session: Session = Depends(get_session)):

    # get all article items
    article_list = session.query(models.Article).all()

    return article_list