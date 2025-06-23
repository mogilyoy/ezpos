## Пример работы

```
from ezpos import SaleEngineAsync, Product
import asyncio

eng = SaleEngineAsync(ip_address='195.101.123.124')

async def main():
    await eng.sale(
        sale_id='1234567890',
        amount=100.0,
        products=[
            Product(**{'name': 'Product 1', 'id': '124', 'cost': 50.0, 'quantity': 1}),
            Product(**{'name': 'Product 2', 'id': '1241', 'cost': 100.0, 'quantity': 1})
        ],
        timeout=30
    )

if __name__ == "__main__":
    asyncio.run(main())

```