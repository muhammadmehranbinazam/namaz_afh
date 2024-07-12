import flet as ft
import datetime
import mysql.connector
def get_attend_data(e, conn, emp_code):
    if conn:
        print(emp_code)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nm_emp_group WHERE emp_code=%s", (emp_code,))
        result = cursor.fetchone()
        print(result)

def attend(page, conn, username):
    emp_code = ft.TextField(label="Enter Employee Code", value=username, disabled=True)
    doc_date = datetime.date.today().strftime("%Y-%m-%d")
    date = ft.TextField(label="Today's Date", value=doc_date, disabled=True)
    
    result = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nm_emp_group WHERE emp_code=%s", (username,))
        result = cursor.fetchone()
    
    group = ft.TextField(label="Employee Group", value=result[0] if result else "", disabled=True)
    nm_number = ft.TextField(label="Enter Number of Namza")
    
    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=lambda e: get_attend_data(e, conn, emp_code.value)
    )
    page.add(emp_code, date, group, nm_number, submit_button)
    
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO nm_emp_attnd (DOC_DATE, GROUP_ID, EMP_CODE, NM_ATTND) VALUES (%s, %s, %s, %s)",
                (doc_date, group.value, emp_code.value, nm_number.value)
            )
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

def logout_func(e):
    pass

def page_view(selected_index, page, conn, username):
    page.clean()  # Clear the existing controls
    if selected_index == 0:
        attend(page, conn, username)
    elif selected_index == 1:
        page.add(ft.TextField(label="Enter name"))
    page.update()

def main_page(page, conn, username):
    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.AMBER_100,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        selected_index=0,
        on_change=lambda e: page_view(e.control.selected_index, page, conn, username),
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Bookmarks",
            ),
        ]
    )
    page_view(0, page, conn, username)  # Initialize with the first tab
    page.update()

def login_page(page: ft.Page, conn):
    def login_func(e):
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (user_name.value, password.value))
            result = cursor.fetchone()
            if result and user_name.value == result[0] and int(password.value) == result[1]:
                page.clean()
                main_page(page, conn, user_name.value)
            else:
                err_text.value = "Username or password is incorrect"
                page.update()

    heading = ft.Text(value="Login", size=100, weight=ft.FontWeight.W_900, color=ft.colors.GREEN)
    user_name = ft.TextField(label="Enter Username")
    password = ft.TextField(label="Enter Password", password=True, can_reveal_password=True)
    err_text = ft.Text(color=ft.colors.RED, weight=ft.FontWeight.W_200)
    login_button = ft.ElevatedButton(
        content=ft.Text(value="Login", size=20),
        width=300,
        height=50,
        bgcolor=ft.colors.ORANGE,
        color=ft.colors.WHITE,
        on_click=login_func
    )

    form_container = ft.Container(
        content=ft.Column(
            controls=[
                heading,
                user_name,
                password,
                err_text,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400,
        alignment=ft.alignment.center,
        padding=20,
    )

    page.add(form_container)

# Define the shared TextField variables outside the functions
c_name = ft.TextField(label="Enter Name")
reg_user_name = ft.TextField(label="Enter User Name")
reg_password = ft.TextField(label="Enter Password")
mobile_number = ft.TextField(label="Enter Mobile Number")
cnic = ft.TextField(label="Enter CNIC")
address = ft.TextField(label="Enter Address")
