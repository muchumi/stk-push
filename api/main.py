from fastapi import FastAPI, status
from api.db.database import Base, engine
from api.routers.stk_routes import routes

app = FastAPI(title="STK push API", description="A FastAPI application for M-Pesa STK Push", version="1.0.0")
app.include_router(routes)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello world, welcome to STK push API"}

