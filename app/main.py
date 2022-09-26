from typing import List

import motor.motor_asyncio
import uvicorn
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config import settings
from models.base import CompanyModel, UserModel

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
db = client["test_db"]


@app.post("/User", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@app.post("/Company", response_description="Add new company", response_model=CompanyModel)
async def create_company(company: CompanyModel = Body(...)):
    company = jsonable_encoder(company)
    new_company = await db["companies"].insert_one(company)
    created_company = await db["companies"].find_one({"_id": new_company.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_company)


@app.get("/Companies", response_description="List all companies", response_model=List[CompanyModel])
async def list_companies():
    companies = await db["companies"].find().to_list(1000)
    if companies is not None:
        return companies
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Companies not found")


@app.get("/Users", response_description="List all users", response_model=List[UserModel])
async def list_users():
    users = await db["users"].find().to_list(1000)
    if users is not None:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Users not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
