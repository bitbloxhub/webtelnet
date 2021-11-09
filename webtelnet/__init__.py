import asyncio
from sanic import Sanic

__version__ = "1.0.0"

app = Sanic("webtelnet")

app.config["THOST"] = "telehack.com"
app.config["TPORT"] = 23

app.static("/", "webtelnet/index.html")


async def websocket_fwd2client(ws, rsreader):
    while True:
        tosend = await rsreader.read(1024)
        await ws.send(tosend)


async def websocket_fwd2serv(ws, rswriter):
    while True:
        recvd = await ws.recv()
        rswriter.write(recvd.encode())
        await rswriter.drain()


@app.websocket("/ws")
async def websocket(req, ws):
    rsreader, rswriter = await asyncio.open_connection(
        app.config["THOST"], app.config["TPORT"]
    )
    asyncio.create_task(websocket_fwd2client(ws, rsreader))
    asyncio.create_task(websocket_fwd2serv(ws, rswriter))
    await asyncio.Future()
