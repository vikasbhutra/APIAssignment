import asyncio
import ormar
from fastapi import BackgroundTasks, FastAPI, HTTPException
from app.db import Number, database

app = FastAPI(title="FastAPI, Docker")


queue = []


async def queueManager(number: Number):
    await asyncio.sleep(10)
    await number.upsert(answer=number.number1 + number.number2)


@app.get("/")
def read_root():
    '''
        root endpoint
    '''
    return {"hello": "world"}


@app.on_event("startup")
async def startup():
    '''
        Starting Point
    '''
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    '''
        End Point
    '''
    if database.is_connected:
        await database.disconnect()


@app.get("/calculate/{number1}/{number2}")
async def calculate(number1: int, number2: int, background_tasks: BackgroundTasks):
    '''
        calculation end point
    '''
    number = await Number.objects.create(
        number1=number1,
        number2=number2,
        answer=2147483646
    )
    background_tasks.add_task(queueManager, number)

    return {"Identifier": number.id}


@app.get("/get_answer/{identifier}/")
async def get_answer(identifier: int):
    '''
        answer end point
    '''
    try:
        calculation: Number = await Number.objects.get(id=identifier)

        if calculation.answer == 2147483646:
            return {'message': 'Please wait ....'}
        else:
            return {'answer': calculation.answer}

    except ormar.NoMatch:
        raise HTTPException(
            status_code=404,
            detail=" Identifier entry does not exist in the database"
        )
