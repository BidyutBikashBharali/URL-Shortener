from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import ORJSONResponse
from starlette.responses import RedirectResponse
from .db import get_db
from .schema import UrlSchema 
from .model import UrlModel
from .crud import *
import os, sys, shortuuid, datetime
from decouple import config

router = APIRouter()

CODE_LENGTH = os.environ.get('CODE_LENGTH')
if CODE_LENGTH is None:
    CODE_LENGTH = config('CODE_LENGTH')

BASE_URL = os.environ.get('BASE_URL')
if BASE_URL is None:
    BASE_URL = config('BASE_URL')



# @router.get("/")
# async def read_root():
#     return {"response": "Welcome to URL shortner!"}




@router.post('/', tags=["Shorten URL"], response_class=ORJSONResponse) 
async def test(url_schema : UrlSchema, session: Session = Depends(get_db)):

    """
    'original_url' field is required, 'short_code' & 'url_expiration' fields are Optional and 0 day < 'url_expiration' field <= 90 days.
    """

    try:
        # converted pydantic schema object to python dict
        url_schema = dict(url_schema)
        
        if url_schema.get("short_code") is not None:
            short_code = url_schema.get("short_code")

            short_code_existance = get_data_by_short_code(session=session, short_code = short_code)
            if short_code_existance is not None:
                return {"status" : "Custom code already in use! Please try a different one."}

        else:
            while True:
                short_code = str(shortuuid.ShortUUID().random(length = int(config("CODE_LENGTH"))))

                short_code_existance = get_data_by_short_code(session=session, short_code = short_code)
                if short_code_existance is None:
                    # print("Custom code generated in backend")
                    break


        shortened_url = os.path.join(config("BASE_URL"), short_code)

        if url_schema.get("url_expiration") is not None:
            url_expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes = url_schema.get("url_expiration"))
        else:
            url_expiration = url_schema.get("url_expiration")
    
    
        url_model = UrlModel(
            original_url = url_schema.get("original_url"),
            shortened_url = shortened_url,
            short_code = short_code,
            url_expiration = url_expiration,
            days_for_url_expiration = url_schema.get("url_expiration")
        )

        session.add(url_model)
        session.commit()
        # session.refresh(url_model) # refresh required when returning the url_model as response, see https://fastapi.tiangolo.com/tutorial/sql-databases/


        if url_schema.get("url_expiration") is None:
            url_expiration = "Never"
        else:
            if url_schema.get('url_expiration') == 1:
                url_expiration = f"After {url_schema.get('url_expiration')} day"
            else:
                url_expiration = f"After {url_schema.get('url_expiration')} days"

        return {
            "status" : "URL shortened successfully.",
            "shortened_url" : shortened_url,
            "original_url" : url_schema.get("original_url"),
            "url_expiration" : url_expiration
        }

    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("Error Type : ", errortype)
        print("Error msg : ", emsg)





@router.get("/{short_code}", tags=["Redirect With Short-Code"], response_class=ORJSONResponse)
async def redirect_url(short_code : str, session : Session = Depends(get_db)):
    
    try:
        data_existance = session.query(UrlModel).filter(UrlModel.short_code == short_code).first()
        if data_existance is None:
            return {"status" : "Invalid URL!"}
        
        data_existance.total_visited_times += 1
        session.commit()
        # print(data_existance.total_visited_times)

        return RedirectResponse(data_existance.original_url)

    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("Error Type : ", errortype)
        print("Error msg : ", emsg)


        
        
@router.get("/{short_code}/info", tags=["Short-URL Info"], summary= "Get URL information", response_class=ORJSONResponse)
async def get_url_data(short_code : str, session : Session = Depends(get_db)):
    
    try:
        data_existance = session.query(UrlModel).filter(UrlModel.short_code == short_code).first()
        if data_existance is None:
            return {"status" : "Invalid URL!"}

        if data_existance.url_expiration is None:
            url_expiration = "Never"
        else:
            if data_existance.days_for_url_expiration == 1:
                url_expiration = f"After {data_existance.days_for_url_expiration} day"
            else:
                url_expiration = f"After {data_existance.days_for_url_expiration} days"


        return {
            "status" : "Shortened URL data.",
            "shortened_url" : data_existance.shortened_url,
            "original_url" : data_existance.original_url,
            "short_code" : data_existance.short_code,
            "created_at" : data_existance.created_at,
            "url_expiration" : url_expiration,
            "total_visited_times" : data_existance.total_visited_times
        }

    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("Error Type : ", errortype)
        print("Error msg : ", emsg)        
