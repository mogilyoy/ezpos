from pydantic import BaseModel, Field
from typing import Optional


class VatEnum(str):
    VATOff = "VATOff"
    VAT0 = "VAT0"
    VAT10 = "VAT10"
    VAT20 = "VAT20"
    VAT110 = "VAT10_110"
    VAT20_120 = "VAT20_120"

class SaleStatusEnum(str):
    OK = "ok"
    BUSY = "busy"
    FAIL = "fail"


class Product(BaseModel):
    name: str
    id: int
    cost: float
    quantity: Optional[float] = 1
    mark_code: Optional[str] = ""
    tag1212: Optional[int] = 1
    vat: Optional[str] = VatEnum.VATOff

class SaleData(BaseModel):
    id: str
    amount: float
    products: Optional[list[Product]] = None

class SaleResponse(BaseModel):
    status: str
    info: Optional[str] = None


class SaleStatus(str):
    OK = 'ok'
    CREATED = 'created'
    WAIT_FOR_CARD = 'wait_for_card'
    CANCELED = 'canceled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FISCALIZATION = 'fiscalization'
    FISCALIZED = 'fiscalized'
    REVERTED = 'reverted'
    FAIL = 'fail'

class SaleType(str):
    CARD = 'card'
    QR = 'qr'


class Slip(BaseModel):
    date: str
    approval_code: str
    rrn: str
    pan: str
    amount: float
    response_code: int
    response_desc: str
    aid: str
    pos_entry_mode: str
    app_label: str
    tvr: str
    invoice: str


class SaleStatusResponse(BaseModel):
    status: str
    info: Optional[str]
    fiscal_qr: Optional[str]
    type: Optional[str] = SaleType.CARD
    slip: Optional[Slip] = None


class Status(BaseModel):
    status: str
    info: Optional[str]
    s_n: str = Field(alias='S/N')
    last_op_id: Optional[str]
    



