from fastapi import FastAPI, status
from api.db.database import Base, engine

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello world"}