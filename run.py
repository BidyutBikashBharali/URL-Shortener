import uvicorn, schedule, time
from threading import Thread
from v1.url_expiration import expire_url
from fastapi import FastAPI
from v1.db import Base, engine
from v1 import api
from fastapi.middleware.cors import CORSMiddleware

description = """

**This API enables developers to convert a lengthy URL into a short one
🚀**

  
  

## **Features**

  - It accepts custom and unique short code for URL shortening
  - Automatically generates unique short code if user given custom short
    code is set to **null** or not given
  - User can set URL validity days after which the Shortened URL will be
    invalid automatically i.e all its info will be discarded  
    from the database. Shortened URL will never be expire if URL validity
    days is not set or set to **null**
  - This API returns URL information at **/{Short Code}/info** endpoint.

  
  

"""

tags_metadata = [

    {
        "name": "Shorten URL",
        "description": " Convert lengthy URL into a short one "
    },

    {
        "name": "Redirect With Short-Code",
        "description": "Get redirected to the original URL"
    },

    {
        "name": "Short-URL Info",
        "description": "This returns Shortened URL information.",
        # "summary": "Get URL info."
    },

]


app = FastAPI(

    docs_url="/",
    redoc_url=None,
    title="REST API For URL Shortening",
    description=description,
    version="0.0.1",
    # terms_of_service="http://bbbwebsite.com/terms/",
    contact={
        "name": "Developer",
        # "url": "https://bbbwebsite.com/contact/",
        "email": "imax7964@gmail.com",
    },
    license_info={
        "name": "The MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata

    )

app.include_router(api.router)

origins = [
    "http://127.0.0.1:8000",
    "https://yourl-short3n3r.herokuapp.com/",
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
    schedule.every(10).seconds.do(expire_url)
    # schedule.every().day.at("01:00").do(expire_url) # 1.00 am
    # schedule.every().day.at("10:00").do(expire_url) # 10:00 am
    # schedule.every().day.at("17:00").do(expire_url) # 5:00 pm

    while True:
        # print("Background Worker Running")
        schedule.run_pending()
        time.sleep(3)

t = Thread(target=run_on_thread, daemon = True) # when daemon = True then this background thread(the "run_on_thread" function) will be stopped when the main thread(when the fastapi app is exited) is exited. otherwise the "run_on_thread" function will be running even after the fastapi app is stopped.
t.start()


#used for development environment
# if __name__ == "__main__":
#     uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
