from typing import Optional
from pydantic import BaseModel, constr, conint, AnyHttpUrl
from decouple import config
import os


CODE_LENGTH = os.environ.get('CODE_LENGTH')
if CODE_LENGTH is None:
    CODE_LENGTH = config('CODE_LENGTH')

class UrlSchema(BaseModel):
    original_url : AnyHttpUrl
    short_code : Optional[constr(max_length = int(config("CODE_LENGTH")))] = None
    url_expiration : Optional[conint(gt =-1, le = 90)] = None
