from io import BytesIO

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, PlainTextResponse

from toolkit import Event


app = FastAPI()

@app.get("/ical")
async def download_ical():
    headers = {
        "Content-Disposition": "attachment; filename=comicw.ics",
    }
    return StreamingResponse(BytesIO(Event.to_ical().serialize().encode("utf-8")),
                             headers=headers,
                             media_type="text/calendar; charset=utf-8")

@app.get("/ping")
async def ping():
    return PlainTextResponse("pong!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
