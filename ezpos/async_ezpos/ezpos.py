from .engine import EzPOSEngineAsync
from ..models.sale import (
    SaleResponse, 
    SaleData,
    SaleStatusResponse,
    SaleStatus,
    Product
)
from ..models.qr import Screen, QR
from datetime import datetime
import asyncio

class ApiAsync(EzPOSEngineAsync):
    def __init__(self, ip_address: str):
        super().__init__(ip_address)
        self._name = "EzPOS API"
        self._description = "EzPOS API for managing point of sale operations."
        self._version = "1.0.0"

    async def _sale(self, data: SaleData) -> SaleResponse:
        return SaleResponse(**await self.make_request("/async/cashless/sale", method='POST', data=data.model_dump()))

    async def _sale_by_card(self, data: SaleData) -> SaleResponse:
        return SaleResponse(**await self.make_request("/async/cashless/sale/card", method='POST', data=data.model_dump()))

    async def _sale_by_qr(self, data: SaleData) -> SaleResponse:
        return SaleResponse(**await self.make_request("/async/cashless/sale/qr", method='POST', data=data.model_dump()))

    async def _cash_sale(self, data: SaleData) -> SaleResponse:
        return SaleResponse(**await self.make_request("/cash/sale", method='POST', data=data.model_dump()))

    async def _sale_fiscal(self, sale_id: str):
        return SaleResponse(**await self.make_request(f"/async/fiscal?id={sale_id}", method='POST'))

    async def _cancel_sale(self, sale_id: str):
        return SaleResponse(**await self.make_request(f"/async/cashless/sale/cancel?id={sale_id}", method='POST'))

    async def _sale_reversal(self, sale_id: str):
        return SaleResponse(**await self.make_request(f"/async/cashless/reversal?id={sale_id}", method='POST'))

    async def _sale_status(self, sale_id: str):
        return SaleStatusResponse(**await self.make_request(f"/sale?id={sale_id}", method='GET'))

    async def _status(self):
        return await self.make_request("/status", method='GET')

    async def _show_qr(self, data: QR):
        return SaleResponse(**await self.make_request("/show/qr", method='POST', data=data.model_dump()))

    async def _show_image(self, data: Screen):
        return SaleResponse(**await self.make_request("/screen", method='POST', data=data.model_dump()))
    

class SaleEngineAsync(ApiAsync):
    def __init__(self, ip_address):
        super().__init__(ip_address)

    async def sale(self, sale_id: str, amount: float, products: list[Product], timeout=30):
        sale_last_status = None
        sale_start = datetime.now()

        status = await self._sale(
            data=SaleData(
                id=sale_id,
                amount=amount,
                products=products
            )
        )

        if status.status == SaleStatus.OK:
            sale_last_status = status.status
            while sale_last_status != SaleStatus.FISCALIZED and (datetime.now() - sale_start).seconds < timeout:
                sale_status = await self._sale_status(sale_id=sale_id)

                if sale_last_status != sale_status.status:
                    sale_last_status = sale_status.status

                    match sale_last_status:
                        case SaleStatus.WAIT_FOR_CARD: print(sale_status)
                        case SaleStatus.IN_PROGRESS: print(sale_status)
                        case SaleStatus.COMPLETED:
                            await self._sale_fiscal(sale_id=sale_id)
                            print(sale_status)
                        case SaleStatus.FISCALIZATION: print(sale_status)
                        case SaleStatus.FISCALIZED:
                            print(sale_status)
                            break
                        case SaleStatus.CANCELED:
                            print(sale_status)
                            break
                        case SaleStatus.REVERTED:
                            print(sale_status)
                            break
                        case SaleStatus.FAIL:
                            print(sale_status)
                            break
                        case _:
                            print(f"Unknown sale status: {sale_last_status}")

                await asyncio.sleep(1)

    async def cancel_sale(self, sale_id: str) -> SaleResponse:
        return await self._cancel_sale(sale_id)

    async def reversal_sale(self, sale_id: str) -> SaleResponse:
        return await self._sale_reversal(sale_id)