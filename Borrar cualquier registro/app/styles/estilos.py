import flet as ft

class Colors:
    BG="#FFDBFD"
    CARD="#982598"
    BORDER="BB8ED0"
    TEXT="#000000"
    PRIMARY="#D78FEE"
    SUCCESS="#A9DFBF"
    INFO="#A1E3F9"
    DANGER="#F1948A"
    WHITE="#FFFFFF"
    BLACK="#000000"

class Textos:
    H1=ft.TextStyle(size=26,height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H2=ft.TextStyle(size=20,height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H3=ft.TextStyle(size=14,height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H4=ft.TextStyle(size=12,height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    text=ft.TextStyle(size=10,height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)

class Inputs:
    INPUT_PRIMARY={
        "border_color": Colors.BORDER,
        "focused_border_color": Colors.PRIMARY,
        "cursor_color": Colors.PRIMARY,
        "width": 500,
        "text_style":Textos.text,
        "label_style":Textos.text,
        "bgcolor": Colors.BG,    
    }

class Buttons:
    BUTTON_PRIMARY = ft.ButtonStyle(bgcolor=Colors.PRIMARY, color=Colors.WHITE,  padding=10, shape=ft.RoundedRectangleBorder(radius=5))
    BUTTON_SUCCESS = ft.ButtonStyle(bgcolor=Colors.SUCCESS, color=Colors.WHITE,  padding=10, shape=ft.RoundedRectangleBorder(radius=5))
    BUTTON_DANGER  = ft.ButtonStyle(bgcolor=Colors.DANGER,  color=Colors.WHITE,  padding=10, shape=ft.RoundedRectangleBorder(radius=5))

class Card:
    tarjeta={
        "width": 600,
        "padding": 16,
        "border_radius": 10,
        "bgcolor": Colors.BG,
        "border":ft.Border.all(2, Colors.BORDER)
    }

Textos_estilos = Textos
