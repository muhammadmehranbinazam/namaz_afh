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
ft.app(target=main, view=ft.WebRenderer)
