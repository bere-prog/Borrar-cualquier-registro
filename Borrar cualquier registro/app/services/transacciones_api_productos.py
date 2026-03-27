#app/services/transacciones_api_productos.py
import httpx

BASE = "http://localhost:8000/products"
TIME_OUT = 10

#Obtiene la lista de productos de FastAPI
async def list_products(limit: int = 20, offset: int = 0) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE}/", params={"limit": limit, "offset": offset}, timeout=TIME_OUT)
            if 200 <= r.status_code < 300:
                return r.json() if r.content else {}
            raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except httpx.RequestError as e:
        raise ValueError("Error de conexión", None, str(e))

#Obtiene el producto con el id que se le pasa como parámetro
async def get_product(product_id: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE}/{product_id}", timeout=TIME_OUT)
            if 200 <= r.status_code < 300:
                return r.json() if r.content else {}
            raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except httpx.RequestError as e:
        raise ValueError("Error de conexión", None, str(e))

#Crea un producto nuevo con los datos que se le pasan como parámetro en un diccionario
async def create_product(data: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE}/", json=data, timeout=TIME_OUT)
            if 200 <= r.status_code < 300:
                return r.json() if r.content else {}
            raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except httpx.RequestError as e:
        raise ValueError("Error de conexión", None, str(e))

#Actualiza el producto que se le indica con el id y los datos nuevos en un diccionario
async def update_product(product_id: str, data: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.put(f"{BASE}/{product_id}", json=data, timeout=TIME_OUT)
            if r.status_code >= 400:
                try:
                    payload = r.json()
                    detail = payload.get("error") or payload.get("detail") or r.text
                except Exception:
                    detail = r.text
                raise ValueError(detail)
            return r.json()
    except httpx.TimeoutException:
        raise ValueError("El servidor tardó demasiado en responder")
    except httpx.ConnectError:
        raise ValueError("No se pudo conectar al servidor")
    except httpx.RequestError as e:
        raise ValueError(f"Error de red {str(e)}")

#Borra el producto que se le indica con el id
async def delete_product(product_id: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.delete(f"{BASE}/{product_id}", timeout=TIME_OUT)
            if 200 <= r.status_code < 300:
                return r.json() if r.content else {}
            raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except httpx.RequestError as e:
        raise ValueError("Error de conexión", None, str(e))