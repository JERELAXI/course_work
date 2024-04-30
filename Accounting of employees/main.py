from tkinter import messagebox
from models import DatabaseManager, EmployeeTable
from customtkinter import *
from PIL import Image
from app_window import app
from clear_window import clear_window


def open_add_employee_window():
    clear_window(app)
    import add_employee
    add_employee.create_interface(app)


def create_interface(app):
    sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55", width=176,
                             height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("img/logo.png")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data,
                        size=(77.68, 85.42))

    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0),
                                                                 anchor="center")

    analytics_img_data = Image.open("img/person_icon.png")
    analytics_img = CTkImage(dark_image=analytics_img_data,
                             light_image=analytics_img_data)

    CTkButton(master=sidebar_frame, image=analytics_img, text="Штат компанії",
              fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#207244", anchor="w").pack(anchor="center", ipady=5,
                                                      pady=(60, 0))

    list_img_data = Image.open("img/add.png")
    list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)

    CTkButton(master=sidebar_frame, image=list_img, text="Додати",
              fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#207244", anchor="w",
              command=open_add_employee_window).pack(anchor="center", ipady=5,
                                                     pady=(16, 0))

    main_view = CTkFrame(master=app, fg_color="#fff", width=1280, height=900,
                         corner_radius=0)
    main_view.pack_propagate(0)
    main_view.pack(side="left")

    title_frame = CTkFrame(master=main_view, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

    CTkLabel(master=title_frame, text="Штат компанії",
             font=("Arial Black", 25),
             text_color="#2A8C55").pack(anchor="nw", side="left")

    search_container = CTkFrame(master=main_view, height=50,
                                fg_color="#F0F0F0")
    search_container.pack(fill="x", pady=(45, 0), padx=27)

    search_entry = CTkEntry(master=search_container, width=305,
                            placeholder_text="Пошук співробітника",
                            border_color="#2A8C55",
                            border_width=2)
    search_entry.pack(side="left", padx=(13, 0), pady=15)

    table_frame = CTkScrollableFrame(master=main_view, fg_color="transparent")
    table_frame.pack(expand=True, fill="both", padx=27, pady=21)

    employee_table = EmployeeTable(DatabaseManager('employees.db'),
                                   table_frame)
    employee_table.create_table()

    def update_table():
        search_text = search_entry.get()
        employee_table.update_table(search_text)

    search_entry.bind("<KeyRelease>", lambda event: update_table())

    table = employee_table.table
    table.pack(expand=True)

    actions = CTkFrame(master=main_view, fg_color="transparent")
    actions.pack(fill="both")

    CTkLabel(master=actions, text="ID для видалення:", font=("Arial Bold", 14),
             text_color="#2A8C55").pack(side="left", padx=(27, 10))

    delete_row_entry = CTkEntry(master=actions, fg_color="#F0F0F0", width=300,
                                corner_radius=8)
    delete_row_entry.pack(side="left", padx=(0, 10))

    def delete_employee_button_clicked():
        row_number = delete_row_entry.get()

        if not row_number:
            messagebox.showerror("Помилка", "Будь ласка, введіть номер рядка")
            return

        if not row_number.isdigit():
            messagebox.showerror("Помилка", "Номер рядка повинен бути числом")
            return

        row_number = int(row_number)

        employee_exists = any(row[0] == row_number for row in
                              employee_table.db_manager.get_employees())
        if not employee_exists:
            messagebox.showerror("Помилка",
                                 "Співробітника з таким id не існує")
            return

        employee_table.delete_employee(row_number)

        messagebox.showinfo("Інформація",
                            f"Співробітник з id {row_number} був успішно видалений")

        employee_table.update_table(search_entry.get())

    CTkButton(master=actions, text="Видалити",
              command=delete_employee_button_clicked,
              width=150, font=("Arial Bold", 17), hover_color="#207244",
              fg_color="#2A8C55", text_color="#fff").pack(side="right",
                                                          anchor="center",
                                                          pady=(30, 30),
                                                          padx=(0, 50))

    app.mainloop()
