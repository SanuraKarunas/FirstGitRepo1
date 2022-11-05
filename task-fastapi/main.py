from typing import Union, Sequence
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class DogType(str, Enum):
    terrier = 'terrier'
    bulldog = 'bulldog'
    dalmatian = 'dalmatian'


class Timestamp(BaseModel):
    id: Union[int, None] = None
    timestamp: Union[int, None] = None


class Dog(BaseModel):
    name: str
    pk: Union[int, None] = None
    kind: DogType


dogs = []


@app.get('/', response_model=str)
async def root_get():
    return


@app.post('/post', response_model=Timestamp)
async def get_post(whatever: Timestamp):
    return {whatever.id: whatever.timestamp}


@app.get('/dog', response_model=Sequence[Dog])
async def get_dogs(x: DogType = None):
    y = []
    for i in dogs:
        if i.kind == x:
            y.append(i)
    if not y:
        return dogs
    return y


@app.post('/dog', response_model=Dog)
async def create_dog(x: Dog):
    if x.pk:
        x = x
    elif len(dogs) == 0:
        x.pk = 0
    else:
        x.pk = len(dogs)
    dogs.append(x)
    return x


@app.get('/dog/{pk]', response_model=Dog)
async def get_dog_by_pk(pk: int):
    for i in dogs:
        if i.pk == pk:
            return i
    raise HTTPException(404)


@app.patch('/dog/{pk}', response_model=Dog)
async def update_dog(pk: int, x: Dog):
    for i in dogs:
        if i.pk == pk:
            i.pk = pk
            buffer = i
            modified_dict = x.dict(exclude_unset=True)
            modified_item = buffer.copy(update=modified_dict)
            dogs[dogs.index(i)] = modified_item
            return modified_item
    raise HTTPException(404)
