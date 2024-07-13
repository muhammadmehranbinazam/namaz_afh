import flet as ft 
from login import login_page
import mysql.connector
def main(page:ft.Page):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="namaz"
    )

    login_page(page, conn)
# ft.app(name="http:/127.0.0.1",target=main, view=ft.WebRenderer, port="57468")
ft.app(target=main, view=ft.WebRenderer)
