from typing import List

from fastapi import FastAPI, Body, HTTPException, status

import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config import settings
import motor.motor_asyncio
from models.base import UserModel, CompanyModel, UpdateCompanyModel


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
    return companies


@app.get("/Users", response_description="List all users", response_model=List[UserModel])
async def list_users():
    users = await db["users"].find().to_list(1000)
    return users


@app.put("/{id}", response_description="Update a company", response_model=CompanyModel)
async def update_company(id: str, company: UpdateCompanyModel = Body(...)):
    company = {k: v for k, v in company.dict().items() if v is not None}

    if len(company) >= 1:
        update_result = await db["students"].update_one({"_id": id}, {"$set": company})

        if update_result.modified_count == 1:
            if (
                updated_company := await db["companies"].find_one({"_id": id})
            ) is not None:
                return updated_company

    if (existing_company := await db["companies"].find_one({"_id": id})) is not None:
        return existing_company

    raise HTTPException(status_code=404, detail=f"Company {id} not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
