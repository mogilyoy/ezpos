from pydantic import BaseModel
from typing import Optional


class QR(BaseModel):
    message: str
    qr: str
    show_time_sec: Optional[int] = 20
    continue_button: Optional[bool] = False

class QResponse(BaseModel):
    status: str
    info: Optional[str]
    qr: Optional[str]
    


class ScreenType(str):
    IDLE = 'idle'
    LOGO = 'logo'


class Screen(BaseModel):
    type: str
    data: str


