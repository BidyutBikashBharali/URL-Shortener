from .db import SessionLocal
from .crud import *
import os, sys, datetime

def expire_url():
    try:
        session = SessionLocal()
        all_data = get_all_data(session=session)
        # print(type(all_data))
        
        for data in all_data:
            if data.url_expiration is not None and data.url_expiration <= datetime.datetime.utcnow():
                print("short code: ", data.short_code, "url expiration: ", data.url_expiration)
                session.delete(data)
                session.commit()

        session.close()
        
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("Error Type : ", errortype)
        print("Error msg : ", emsg)