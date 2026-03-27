import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos, Card
from app.views.nuevo_editar import formulario_nuevo_editar_producto


def products_view(page: ft.Page) -> ft.Control:

    ############ Paso 3: Editar producto ###############
    def inicio_editar_producto(p: dict[str, Any]):
        async def editar_producto(data: dict):
            try:
                await update_product(p["id"], data)
                close()
                await show_snackbar(page, "Éxito", "Producto actualizado", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=editar_producto, initial=p)
        open_()

    ############ Nuevo producto ###############
    def inicio_nuevo_producto(_e):
        async def crear_nuevo_producto(data: dict):
            try:
                await create_product(data)
                await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto)
        open_()

    ############# Borrar producto #############
    async def borrar_producto(p: dict[str, Any]):
        try:
            await delete_product(p["id"])
            await show_snackbar(page, "Éxito", "Producto borrado", bgcolor=Colors.SUCCESS)
            await actualizar_data()
        except ApiError as ex:
            await show_popup(page, "Error", api_error_to_text(ex))
        except Exception as ex:
            await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

    def inicio_borrar_producto(p: dict[str, Any]):
        async def tarea():
            await borrar_producto(p)

        page.run_task(tarea)

    rows_data: list[dict[str, Any]] = []
    total_items = 0
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos_estilos.H4)

    columnas = [
        ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Acciones", style=Textos_estilos.H4)), 
    ]

    data = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("nombre1...")),
                ft.DataCell(ft.Text("cantidad1...")),
                ft.DataCell(ft.Text("ingreso1...")),
                ft.DataCell(ft.Text("min1...")),
                ft.DataCell(ft.Text("max1...")),
                ft.DataCell(ft.Text("...")), # <-- Paso 1
            ]
        )
    ]

    tabla = ft.DataTable(
        columns=columnas,
        rows=data,
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48
    )

    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            res = await list_products(limit=500, offset=0)
            total_items = int(res.get("total", 0))
            total_text.value = f"Total de productos: {total_items}"
            rows_data = res.get("items", []) or []
            actualizar_filas()
        except Exception as ex:
            await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

    def actualizar_filas():
        nuevas_filas = []
        for p in rows_data:
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.get("name", ""))),
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", "") or "")),
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                        # Paso 2: Agregar botones de acción
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT, 
                                        tooltip="Editar", 
                                        on_click=lambda e, p=p: inicio_editar_producto(p)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE, 
                                        tooltip="Borrar", 
                                        on_click=lambda e, p=p: inicio_borrar_producto(p)
                                    ), # <-- Paso 1: Botón borrar descomentado
                                ]
                            )
                        ),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()

    btn_nuevo = ft.ElevatedButton(
        "Nuevo Registro",
        icon="add",
        on_click=inicio_nuevo_producto
    )

    page.run_task(actualizar_data)

    contenido = ft.Column(
        spacing=30,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            btn_nuevo,
            total_text,
            ft.Container(content=tabla)
        ]
    )

    return contenido
