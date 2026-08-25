from fastapi import FastAPI

app = FastAPI(title="LedgerCore")

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}