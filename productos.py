from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["products"])

class Productos1(BaseModel):
    id_prodcto: int
    nombre_prodcto: str

productos_lista = [
    Productos1(id_prodcto=1, nombre_prodcto="telefono"),
    Productos1(id_prodcto=2, nombre_prodcto="televisor"),
    Productos1(id_prodcto=3, nombre_prodcto="ipad"),
    Productos1(id_prodcto=4, nombre_prodcto="ps5"),
    Productos1(id_prodcto=5, nombre_prodcto="monitor"),
    Productos1(id_prodcto=6, nombre_prodcto="laptop")
]

# Obtener todos los productos
@router.get("/productos")
async def productos():
    return productos_lista

# Obtener un producto por ID
@router.get("/producto/{id_prodcto}")
async def get_product(id_prodcto: int):
    producto = search_products(id_prodcto)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Crear un nuevo producto
@router.post("/producto/")
async def create_product(product: Productos1):
    # Verificar si el producto ya existe
    if search_products(product.id_prodcto) is not None:
        raise HTTPException(status_code=400, detail="El producto ya existe")
    
    # Si no existe, agregar a la lista
    productos_lista.append(product)
    return {"mensaje": "Producto creado con éxito", "producto": product}

# Actualizar un producto existente
@router.put("/producto/")
async def update_product(product: Productos1):
    for index, saved_product in enumerate(productos_lista):
        if saved_product.id_prodcto == product.id_prodcto:
            productos_lista[index] = product
            return {"mensaje": "Producto actualizado con éxito", "producto": product}
    
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar un producto por ID
@router.delete("/producto/{id_prodcto}")
async def product_delete(id_prodcto: int):
    for index, saved_product in enumerate(productos_lista):
        if saved_product.id_prodcto == id_prodcto:
            del productos_lista[index]
            return {"mensaje": "Producto borrado con éxito"}

    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Función auxiliar para buscar un producto por ID
def search_products(id_prodcto: int):
    for product in productos_lista:
        if product.id_prodcto == id_prodcto:
            return product
    return None
