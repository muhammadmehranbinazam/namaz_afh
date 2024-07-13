import flet as ft
import datetime
import mysql.connector
conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="namaz"
    )
def on_date_change(e):
    # Callback function to handle date change events
    from_date = e.control.page.controls[0].controls[0].value
    to_date = e.control.page.controls[0].controls[1].value
    print(f"From Date: {from_date}, To Date: {to_date}")


from_date_picker = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: ft.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                    on_change=on_date_change,
                    # on_dismiss=handle_dismissal,
                )
            ),
        )
to_date_picker = ft.DatePicker(on_change=on_date_change)


def get_attend_data(page,conn,username):
    if conn:
        print(username)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nm_emp_group WHERE emp_code=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        print(result)
    page.clean()
    page.add(ft.Column([
            # page.clean(),
            ft.Text("From Date"),
            from_date_picker,
            ft.Text("To Date"),
            to_date_picker
        ]))

def attend(page, conn, username):
    page.clean()
    emp_code = ft.TextField(label="Enter Employee Code", value=username, disabled=True)
    doc_date = datetime.date.today().strftime("%Y-%m-%d")
    date = ft.TextField(label="Today's Date", value=doc_date, disabled=True)
    
    result = None
    # if conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM nm_emp_group WHERE emp_code=%s", (username,))
    #     result = cursor.fetchone()
    
    group = ft.TextField(label="Employee Group", value=result[0] if result else "", disabled=True)
    nm_number = ft.TextField(label="Enter Number of Namza")
    
    def submit_handler(e):
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM nm_emp_attnd WHERE DOC_DATE=%s AND EMP_CODE=%s",
                (doc_date, emp_code.value)
            )
            existing_record = cursor.fetchone()
            if existing_record:
                print("Record already exists for this date and employee code.")
            else:
                try:
                    cursor.execute(
                        "INSERT INTO nm_emp_attnd (DOC_DATE, GROUP_ID, EMP_CODE, NM_ATTND) VALUES (%s, %s, %s, %s)",
                        (doc_date, group.value, emp_code.value, nm_number.value)
                    )
                    conn.commit()
                    print("Record inserted successfully.")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                finally:
                    cursor.close()
    
    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=submit_handler
    )
    
    page.add(emp_code, date, group, nm_number, submit_button)

def logout_func(e):
    pass



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
    page.main_page_container = ft.Container(
    )
    page_view(0, page, conn, username)  # Initialize with the first tab
    page.update()





def page_view(selected_index, page, conn, username):
      # Clear the existing controls
    if selected_index == 0:
        # page.clean()
        page.main_page_container.content=attend(page, conn, username)
        page.update()
    elif selected_index == 1:
        # page.clean()
        # page.add()
        page.main_page_container.content = get_attend_data(page,conn,username)
        # page.update()
    page.update()


def login_page(page: ft.Page, conn):
    def login_func(e):
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (user_name.value, password.value))
            result = cursor.fetchone()
            cursor.close()
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
