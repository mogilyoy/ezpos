## Пример работы

```
from ezpos import SaleEngine
from ezpos.models.sale import Product

eng = SaleEngine(ip_adress='198.162.0.107')

eng.sale(
    sale_id='123',
    amount=100.0,
    products=Product(
        name='Сникерс',
        id=124412,
        cost=10.0,
        quantity=10
    )
)

```