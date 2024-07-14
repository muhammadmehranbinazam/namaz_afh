import flet as ft
import datetime
import mysql.connector

def refresh_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="namaz"
    )

def from_handle_change(e, page):
    page.session.set("from_date", e.control.value.strftime('%Y-%m-%d'))

def to_handle_change(e, page):
    page.session.set("to_date", e.control.value.strftime('%Y-%m-%d'))

def from_date_picker(page):
    return ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=10, day=1),
                last_date=datetime.datetime(year=2024, month=10, day=1),
                on_change=lambda e: from_handle_change(e, page),
            )
        ),
    )

def to_date_picker(page):
    return ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=10, day=1),
                last_date=datetime.datetime(year=2070, month=10, day=1),
                on_change=lambda e: to_handle_change(e, page),
            )
        ),
    )

def get_attend_data_value(page, username):
    conn = refresh_connection()
    from_date = page.session.get("from_date")
    to_date = page.session.get("to_date")
    
    if not from_date or not to_date:
        page.add(ft.Text("Please select both from date and to date."))
        return

    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM test_daily_attnd WHERE emp_code=%s AND timein BETWEEN %s AND %s",
            (username, from_date, to_date)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            data_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Employee Code")),
                    ft.DataColumn(ft.Text("Time In")),
                    ft.DataColumn(ft.Text("Time Out")),
                    # Add more columns as needed
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[1]))),  # Assuming date is the second column
                            ft.DataCell(ft.Text(str(row[2]))),  # Assuming attendance is the third column
                            ft.DataCell(ft.Text(str(row[3]))),
                            # Add more cells as needed
                        ]
                    ) for row in results
                ]
            )

            scroll_container = ft.Container(
                content=ft.ListView(
                    controls=[data_table],
                    width=page.width - 40,
                    height=page.height - 200,
                    padding=ft.Padding(5, 5, 5, 5),
                    auto_scroll=False,
                )
            )

            # Clear existing controls and add the updated DataTable
            page.clean()
            page.add(ft.Text("Employee Code: " + username))
            page.add(ft.Text("From Date: " + from_date))
            page.add(ft.Text("To Date: " + to_date))
            page.add(scroll_container)
        else:
            page.clean()
            page.add(ft.Text("No records found for the selected date range."))

        page.update()

def get_attend_data(page, username):
    page.clean()
    employe_code = ft.TextField(label="Employee Code", value=username, disabled=True)
    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=lambda e: get_attend_data_value(page, username)
    )
    
    page.add(ft.Column([
        employe_code,
        ft.Text("From Date"),
        from_date_picker(page),
        ft.Text("To Date"),
        to_date_picker(page),
        submit_button,
    ]))

def attend(page, conn, username):
    page.clean()
    emp_code = ft.TextField(label="Enter Employee Code", value=username, disabled=True)
    doc_date = datetime.date.today().strftime("%Y-%m-%d")
    date = ft.TextField(label="Today's Date", value=doc_date, disabled=True)

    result = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nm_emp_group WHERE emp_code=%s", (username,))
        result = cursor.fetchall()

    group = ft.TextField(label="Employee Group", value=result[0][0] if result else "", disabled=True)
    nm_number = ft.TextField(label="Enter Number of Namza")

    def submit_handler(e):
        if conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nm_emp_attnd WHERE DOC_DATE=%s AND EMP_CODE=%s",
                    (doc_date, emp_code.value)
                )
                existing_record = cursor.fetchone()
                cursor.fetchall()  # Fetch all remaining results
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

    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=submit_handler
    )

    page.add(emp_code, date, group, nm_number, submit_button)

def logout_func(e):
    pass

def main_page(page, conn, username):
    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.ORANGE,
        inactive_color=ft.colors.BLACK,
        active_color=ft.colors.WHITE,
        selected_index=0,
        on_change=lambda e: page_view(e.control.selected_index, page, conn, username),
        destinations=[
            ft.NavigationDestination(icon=ft.icons.SAFETY_CHECK, label="Namaz Attandance"),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Daily Attandance"),
            ft.NavigationDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Bookmarks",
            ),
        ]
    )
    page.main_page_container = ft.Container()
    page_view(0, page, conn, username)  # Initialize with the first tab
    page.update()

def page_view(selected_index, page, conn, username):
    if selected_index == 0:
        attend(page, conn, username)
    elif selected_index == 1:
        get_attend_data(page, username)
    page.update()

def login_page(page: ft.Page, conn):
    def login_func(e):
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (user_name.value, password.value))
                result = cursor.fetchone()
                cursor.fetchall()  # Fetch all remaining results
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
            alignment=ft.MainAxisAlignment.CENTER,  # Center align vertically
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center align horizontally
        ),
        width=400,
        alignment=ft.alignment.center,  # Center align the container itself
        padding=20,
    )

    page.add(form_container)

# Starting point of the app
# def main(page: ft.Page):
#     conn = refresh_connection()
#     login_page(page, conn)

# ft.app(target=main)
