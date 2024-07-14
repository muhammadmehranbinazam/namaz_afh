import flet as ft 
from login import login_page
import mysql.connector
def main(page:ft.Page):
    page.horizontal_alignment=ft.MainAxisAlignment.CENTER,
    page.vertical_alignment= ft.CrossAxisAlignment.CENTER,
    page.scroll = ft.ScrollMode.ALWAYS,
    # page.splash = ft.Image("assets/favicon.png")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="namaz"
    )

    login_page(page, conn)
# ft.app(name="http:/127.0.0.1",target=main, view=ft.WebRenderer, port="57468")
ft.app(target=main,assets_dir="assets", view=ft.WEB_BROWSER)
