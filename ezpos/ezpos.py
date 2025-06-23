from .engine import EzPOSEngine
from .models.sale import (
        SaleData,
        SaleResponse,
        SaleStatusResponse,
        Product,
        SaleStatus
    )
from .models.qr import QR, Screen
from datetime import datetime
from threading import Thread
import time


class Api(EzPOSEngine):
    def __init__(self, ip_address: str):
        super().__init__(ip_address)
        self._name = "EzPOS API"
        self._description = "EzPOS API for managing point of sale operations."
        self._version = "1.0.0"

    def _sale(self, data: SaleData) -> SaleResponse:
        """
        Process a sale transaction with the provided data.
        
        :param data: Dictionary containing sale details.
        :return: Response from the sale operation.
        """
        
        return SaleResponse(**self.make_request("/async/cashless/sale", method='POST', data=data.model_dump()))
    
    def _sale_by_card(self, data: SaleData) -> SaleResponse:
        """
        Process a sale transaction using card data.
        
        :param card_data: Dictionary containing card details.
        :return: Response from the sale operation.
        """
        return SaleResponse(**self.make_request("/async/cashless/sale/card", method='POST', data=data.model_dump()))
    
    def _sale_by_qr(self, data: SaleData) -> SaleResponse:
        """
        Process a sale transaction using card data.
        
        :param card_data: Dictionary containing card details.
        :return: Response from the sale operation.
        """
        return SaleResponse(**self.make_request("/async/cashless/sale/qr", method='POST', data=data.model_dump()))
    
    def _cash_sale(self, data: SaleData) -> SaleResponse:
        """
        Process a cash sale transaction with the provided data.
        
        :param data: Dictionary containing cash sale details.
        :return: Response from the cash sale operation.
        """
        return SaleResponse(**self.make_request("/cash/sale", method='POST', data=data.model_dump()))
    
    def _sale_fiscal(self, sale_id: str):
        """
        Process a fiscal sale transaction with the provided data.
        
        :param data: Dictionary containing fiscal sale details.
        :return: Response from the fiscal sale operation.
        """
        return SaleResponse(**self.make_request(f"/async/fiscal?id={sale_id}", method='POST'))
    
    def _cancel_sale(self, sale_id: str):
        """
        Cancel a sale transaction with the provided data.
        
        :param data: Dictionary containing cancellation details.
        :return: Response from the cancellation operation.
        """
        return SaleResponse(**self.make_request(f"/async/cashless/sale/cancel?id={sale_id}", method='POST'))
    
    def _sale_reversal(self, sale_id: str):
        """
        Process a sale reversal transaction with the provided data.
        
        :param data: Dictionary containing reversal details.
        :return: Response from the reversal operation.
        """
        return SaleResponse(**self.make_request(f"/async/cashless/reversal?id={sale_id}", method='POST'))
    
    def _sale_status(self, sale_id: str):
        """
        Check the status of a sale transaction with the provided data.
        
        :param data: Dictionary containing sale status details.
        :return: Response from the sale status operation.
        """
        return SaleStatusResponse(**self.make_request(f"/sale?id={sale_id}", method='GET'))
    
    def _status(self):
        """
        Get the status of the EzPOS server.
        
        :return: Response containing the server status.
        """
        return self.make_request("/status", method='GET')
    
    def _show_qr(self, data: QR):
        """
        Show a QR code for the provided data.
        
        :param data: Dictionary containing QR code details.
        :return: Response from the QR code operation.
        """
        return SaleResponse(**self.make_request("/show/qr", method='POST', data=data.model_dump()))
    
    def _show_image(self, data: Screen):
        """
        Show an image for the provided data.
        
        :param data: Dictionary containing image details.
        :return: Response from the image operation.
        """
        return SaleResponse(**self.make_request("/screen", method='POST', data=data.model_dump()))
    

class SaleEngine(Api):
    def __init__(self, ip_address):
        super().__init__(ip_address)
    
    def sale(self, sale_id: str, amount: float, products: list[Product], timeout = 30):
        sale_last_status = None
        sale_status = None
        sale_start = datetime.now()
        status = self._sale(
            data=SaleData(
                id=sale_id,
                amount=amount,
                products=products
            )
        )
        if status.status == SaleStatus.OK:
            sale_last_status = status.status
            while sale_last_status != SaleStatus.FISCALIZED or (datetime.now() - sale_start).seconds < timeout:
                sale_status = self._sale_status(sale_id=sale_id)

                if sale_last_status != sale_status.status:
                    sale_last_status = sale_status.status

                    match sale_last_status:
                        case SaleStatus.WAIT_FOR_CARD: print(sale_status) 
                        case SaleStatus.IN_PROGRESS: print(sale_status) 
                        case SaleStatus.COMPLETED: self._sale_fiscal(sale_id=sale_id); print(sale_status)
                        case SaleStatus.FISCALIZATION: print(sale_status)
                        case SaleStatus.FISCALIZED: print(sale_status); # self._show_qr(data=QR())
                        case SaleStatus.CANCELED: print(sale_status); break
                        case SaleStatus.REVERTED: print(sale_status); break
                        case SaleStatus.FAIL: print(sale_status); break
                        case _:
                            print(f"Unknown sale status: {sale_last_status}")
                time.sleep(1)

    def cancel_sale(self, sale_id: str) -> SaleResponse:
        return self._cancel_sale(sale_id)
    
    def reversal_sale(self, sale_id: str) -> SaleResponse:
        return self._sale_reversal(sale_id)

        

        