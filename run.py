import uvicorn, schedule, time
from threading import Thread
from Core.url_expiration import expire_url
from fastapi import FastAPI
from Core.db import Base, engine
from Core import api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(api.router)

origins = [
    "http://127.0.0.1:8000",
]

# origins = ["*"] # not recommended for production

# "In order for our REST API endpoints to be consumed in client applications such as Vue, React, Angular or any other Web applications that are running on other domains, we should tell our FastAPI to allow requests from the external callers to the endpoints of this FastAPI application. We can enable CORS (Cross Origin Resource Sharing) either at application level or at specific endpoint level."
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# for creating database with defined models
Base.metadata.create_all(bind=engine)


def run_on_thread():
    schedule.every(120).seconds.do(expire_url)
    # schedule.every().day.at("01:00").do(expire_url) # 1.00 am
    # schedule.every().day.at("10:00").do(expire_url) # 10:00 am
    # schedule.every().day.at("17:00").do(expire_url) # 5:00 pm

    while True:
        print("Background Worker Running")
        schedule.run_pending()
        time.sleep(3)


if __name__ == "__main__":
    t = Thread(target=run_on_thread, daemon = True) # when daemon = True then this background thread(the "run_on_thread" function) will be stopped when the main thread(when the fastapi app is exited) is exited. otherwise the "run_on_thread" function will be running even after the fastapi app is stopped.
    t.start()
    uvicorn.run("run:app", host="0.0.0.0", port=8000) #, reload=True)

