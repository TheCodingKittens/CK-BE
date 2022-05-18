from platform import node
from typing import List

# CRUD operations for the Command model
from app import crud

# Models=
from app.models.user import User

# Fastapi Dependencies
from app.services.parser import Parser
from aredis_om.model import NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()


@router.post("", response_model=User)
async def create_user(user: User):
    return await crud.user.create(user)


@router.get("/{username}", response_model=User)
async def get_user(username: str):
    return await crud.user.get_by_username(username)


@router.get("/", response_model=List[User])
async def get_users():
    return await crud.user.read_all()
