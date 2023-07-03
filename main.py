from fastapi import FastAPI, WebSocket
import json
import time
import asyncio
from random import *
from datetime import datetime

app = FastAPI()


# Define a WebSocket endpoint
@app.get("/")
async def homepage():
    data = json.dumps({'hello': 'world'})
    return data


@app.websocket("/ws_limb")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await send_limb(websocket)


@app.websocket("/ws_events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await send_events(websocket)


async def send_events(websocket: WebSocket):
    i = 0
    while True:
        i += 1


        data = {
            "events": [
                {
                    "id": "11-11",
                    "centerFrequency": i*1e5,
                    "bw": 12000.0,
                    "list": "new",

                    "activityTime": [
                        {
                          "start": i,
                          "stop": i+1,
                          "level": 12.4,
                        },
                        {
                            "start": i+2,
                            "stop": i+3,
                            "level": 2.4,
                        },
                        {
                            "start": i+4,
                            "stop": None,
                            "level": -5.4,
                        },
                    ],
                },
                {
                    "id": "11-12",
                    "centerFrequency": i*2e5,
                    "bw": 10000.0,
                    "list": "new",

                    "activityTime": [
                        {
                          "start": i+5,
                          "stop": i+6,
                          "level": 12.4,
                        },
                        {
                            "start": i+7,
                            "stop": i+8,
                            "level": -12.4,
                        },
                        {
                            "start": i+9,
                            "stop": i+10,
                            "level": 32.4,
                        },
                    ],
                },
                {
                    "id": "11-13",
                    "centerFrequency": i*3e5,
                    "bw": 12000.0,
                    "list": "new",

                    "activityTime": [
                        {
                          "start": i+11,
                          "stop": i+12,
                          "level": -33.4,
                        },
                        {
                            "start": i+13,
                            "stop": i+14,
                            "level": -31.4,
                        },
                        {
                            "start": i+15,
                            "stop": i+16,
                            "level": -51.4,
                        },
                    ],
                },
            ],
        }
        data = json.dumps(data)
        await websocket.send_text(data)
        await asyncio.sleep(1)


async def send_limb(websocket: WebSocket):
    i = 0
    while True:
        i += 0.1
        data = {
            "peleng": i % 360,
            "heading": i*2 % 360,
            "mode": i*3 % 360,
            # "mode": 0,
            "history": [
                i*4 % 360,
                i*5 % 360,
                i*6 % 360,
                i*7 % 360
            ],
            "quality": randint(1, 100),
        }
        data = json.dumps(data)
        print(data)
        await websocket.send_text(data)
        await asyncio.sleep(0.02)


async def responseMessager(websocket):
    message = await websocket.receive_text()
    response = messageChanger(message)
    # print(response)
    # Send a response back to the client
    await websocket.send_text(response)


def messageChanger(message):
    jsonMessage = json.loads(message)
    jsonRes = messageLogicChanger(jsonMessage)
    response = json.dumps(jsonRes)
    return response


def messageLogicChanger(jsonMessage):
    jsonMessage['centerFrequency'] = 1e7
    return jsonMessage
