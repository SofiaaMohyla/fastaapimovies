from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import String, Integer, Float, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from sqlalchemy import create_engine, select

# ---------- SQLAlchemy setup ----------
DATABASE_URL = "sqlite:///./movies.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    year: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float, default=0.0)  # 0–10
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


Base.metadata.create_all(engine)

# ---------- Pydantic schemas ----------
class MovieBase(BaseModel):
    title: str = Field(..., max_length=200)
    year: int = Field(..., ge=1888, le=2100)
    rating: float = Field(0, ge=0, le=10)
    description: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    year: Optional[int] = Field(None, ge=1888, le=2100)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None


class MovieOut(MovieBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy -> Pydantic


# ---------- FastAPI app ----------
app = FastAPI(title="Movies CRUD (FastAPI + SQLite)")


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create
@app.post("/movies", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


# Read (list with simple filters + pagination)
@app.get("/movies", response_model=List[MovieOut])
def list_movies(
    q: Optional[str] = None,
    year: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    stmt = select(Movie)
    if q:
        # very simple title filter
        stmt = stmt.filter(Movie.title.contains(q))
    if year:
        stmt = stmt.filter(Movie.year == year)
    movies = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return movies


# Read (one)
@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# Update (partial)
@app.patch("/movies/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(movie, field, value)

    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


# Delete
@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return None


uvicorn.run(app)