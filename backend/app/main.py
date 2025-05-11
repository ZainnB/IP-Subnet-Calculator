from fastapi import FastAPI
from app.routers import ip_calculator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="IP Calculator for Subnet Design",
    description="Calculate subnetting details, split networks, and export results.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the IP Calculator router
print("Router imported:", ip_calculator)
app.include_router(ip_calculator.router, prefix="/api/v1/ip", tags=["IP Calculator"])

@app.get("/")
def root():
    return {"message": "Welcome to the IP Calculator API!"}
