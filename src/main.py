import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.codes.router import codes_router


app = FastAPI()

app.title = "Palacio Digital API"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "Fabian Espitia"}


app.include_router(codes_router)


if __name__ == "__main__":

    port = os.getenv("PORT")

    print(f"[INFO] Port: {port}")

    if not port:
        print("[INFO] Environment variable not found: Port")

        port = 8080

    uvicorn.run(app, host="0.0.0.0", port=int(port))
