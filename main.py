from fastapi import FastAPI, WebSocket
import json
import time
import asyncio
from random import *
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a WebSocket endpoint


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



fakeServerResponse = {
    "devices": [
    {
        "deviceInfo": {
            "id": "289c3aa0-ae30-423d-b3b8-03a9109d2d91",
            "model": "ESMD",
            "antenna": "ADD107",
            "serialNumber": "100100"
        },
        "isRec": True,
        "isDf": True,
        "isPscan": True,
        "devAddress": "172.17.75.1",
        "devMessagePort": 5555,
        "localDataPort": 31001,
        "dataProcAddr": "ws://192.168.1.2:30001",
        "controlPanelAddr": "ws://192.168.1.2:30002",
        "chartControlAddr": "ws://192.168.1.2:30003",
        "eventsPanelAddr": "ws://192.168.1.2:30004",
        "rawEventsAddr": "ws://192.168.1.2:30005",
        "audioMsgPort": "ws://192.168.1.2:30006",
        "audioDataPort": "ws://192.168.1.2:30016"
    },
    {
        "deviceInfo": {
            "id": "289c3aa0-ae30-423d-b3b8-03a9109d2d91",
            "model": "ESMD",
            "antenna": "ADD107",
            "serialNumber": "100100"
        },
        "isRec": True,
        "isDf": True,
        "isPscan": True,
        "devAddress": "172.17.75.1",
        "devMessagePort": 5555,
        "localDataPort": 31001,
        "dataProcAddr": "ws://192.168.1.2:30001",
        "controlPanelAddr": "ws://192.168.1.2:30002",
        "chartControlAddr": "ws://192.168.1.2:30003",
        "eventsPanelAddr": "ws://192.168.1.2:30004",
        "rawEventsAddr": "ws://192.168.1.2:30005",
        "audioMsgPort": "ws://192.168.1.2:30006",
        "audioDataPort": "ws://192.168.1.2:30016"
        }
    ],
    "serverName": "point 1",
    "description": "some user description",
    "serverCoordinate": {
        "latitude": 55.7522,
        "longitude": 37.6156,
        "altitudeKnown": True,
        "altitude": 100.2
    }
}

class DeviceInfo(BaseModel):
    id: str
    model: str
    antenna: str
    serialNumber: str


class Device(BaseModel):
    deviceInfo: DeviceInfo
    isRec: bool
    isDf: bool
    isPscan: bool
    devAddress: str
    devMessagePort: str
    localDataPort: str
    dataProcAddr: str
    controlPanelAddr: str
    chartControlAddr: str
    eventsPanelAddr: str
    rawEventsAddr: str

class ServerCoordinate(BaseModel):
    latitude: float
    longitude: float
    altitudeKnown: bool
    altitude: float


class ServerResponse(BaseModel):
    devices: List[Device]
    serverName: str
    description: str
    serverCoordinate: ServerCoordinate

class Server(BaseModel):
    devices: List[Device]
    serverUrl: str
    serverName: str
    description: str
    serverCoordinate: ServerCoordinate

class ServerList(BaseModel):
    __root__:List[Server]


@app.get("/devices", response_model=ServerResponse)
async def answerDevices():
    return fakeServerResponse

@app.post("/servers")
async def postServers(req: ServerList):
    return {"res": "ok", "req": req}

@app.get("/")
async def homepage():
    data = json.dumps({'hello': 'world'})
    return data

