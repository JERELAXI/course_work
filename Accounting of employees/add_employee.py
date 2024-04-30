from models import Employee, DatabaseManager
from PIL import Image
from customtkinter import *
from clear_window import clear_window
from app_window import app
from tkinter import messagebox


def go_back():
    clear_window(app)
    import main
    main.create_interface(app)


def open_add_employee_window():
    clear_window(app)
    create_interface(app)


def validate_age(age):
    if not age.isdigit() or int(age) < 18 or int(age) > 65:
        return False
    return True


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

    person_img_data = Image.open("img/person_icon.png")
    person_img = CTkImage(dark_image=person_img_data,
                          light_image=person_img_data)

    CTkButton(master=sidebar_frame, image=person_img, text="Штат компанії",
              fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#207244", command=go_back, anchor="w").pack(
        anchor="center", ipady=5,
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

    CTkLabel(master=main_view, text="Додавання співробітника",
             font=("Arial Black", 25),
             text_color="#2A8C55").pack(anchor="nw", pady=(29, 0), padx=27)

    CTkLabel(master=main_view, text="ПІБ", font=("Arial Bold", 17),
             text_color="#52A476").pack(anchor="nw", pady=(25, 0), padx=27)
    name_entry = CTkEntry(master=main_view, fg_color="#F0F0F0",
                          border_width=0)
    name_entry.pack(fill="x", pady=(12, 0), padx=27, ipady=10)

    grid = CTkFrame(master=main_view, fg_color="transparent")
    grid.pack(fill="both", padx=27, pady=(31, 0))

    CTkLabel(master=grid, text="Посада", font=("Arial Bold", 17),
             text_color="#52A476", justify="left").grid(row=0, column=0,
                                                        sticky="w")
    position_entry = CTkEntry(master=grid, fg_color="#F0F0F0",
                              border_width=0, width=300)
    position_entry.grid(row=1, column=0, ipady=10, sticky="w", padx=0,
                        pady=(12, 0))

    CTkLabel(master=grid, text="Зарплата", font=("Arial Bold", 17),
             text_color="#52A476", justify="left").grid(row=0, column=1,
                                                        sticky="w",
                                                        padx=(25, 0))
    salary_entry = CTkEntry(master=grid, fg_color="#F0F0F0",
                            border_width=0, width=300)
    salary_entry.grid(row=1, column=1, ipady=10, sticky="w", padx=(25, 0),
                      pady=(12, 0))

    CTkLabel(master=grid, text="Номер телефону", font=("Arial Bold", 17),
             text_color="#52A476", justify="left").grid(row=2, column=0,
                                                        sticky="w",
                                                        pady=(38, 0))
    phone_number_entry = CTkEntry(master=grid, fg_color="#F0F0F0", width=300,
                                  corner_radius=8)
    phone_number_entry.grid(row=3, column=0, rowspan=1, sticky="w",
                            pady=(12, 0),
                            padx=(0, 0), ipady=10)

    CTkLabel(master=grid, text="Вік", font=("Arial Bold", 17),
             text_color="#52A476", justify="left").grid(row=2, column=1,
                                                        sticky="w",
                                                        pady=(42, 0),
                                                        padx=(25, 0))
    age_entry = CTkEntry(master=grid, fg_color="#F0F0F0", width=300,
                         corner_radius=8)
    age_entry.grid(row=3, column=1, rowspan=1, sticky="w", pady=(12, 0),
                   padx=(25, 0), ipady=10)

    actions = CTkFrame(master=main_view, fg_color="transparent")
    actions.pack(fill="both")

    CTkButton(master=actions, text="Назад", command=go_back, width=300,
              fg_color="transparent",
              font=("Arial Bold", 17), border_color="#2A8C55",
              hover_color="#eee",
              border_width=2, text_color="#2A8C55").pack(side="left",
                                                         anchor="sw",
                                                         pady=(30, 0),
                                                         padx=(27, 24))

    def add_employee_button_clicked():
        name = name_entry.get()
        position = position_entry.get()
        salary = salary_entry.get()
        phone_number = phone_number_entry.get()
        age = age_entry.get()

        if not name or not position or not salary or not phone_number or not age:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля")
            return

        if not phone_number.isdigit() or len(phone_number) != 10:
            messagebox.showerror("Помилка",
                                 "Номер телефону повинен складатися з 10 цифр")
            return

        if not validate_age(age):
            messagebox.showerror("Помилка",
                                 "Вік повинен бути числом від 18 до 65")
            return

        employee = Employee(name, position, salary, phone_number, age)

        db_manager = DatabaseManager('employees.db')

        db_manager.add_employee(employee)

        name_entry.delete(0, 'end')
        position_entry.delete(0, 'end')
        salary_entry.delete(0, 'end')
        phone_number_entry.delete(0, 'end')
        age_entry.delete(0, 'end')

    CTkButton(master=actions, text="Додати",
              command=add_employee_button_clicked,
              width=300, font=("Arial Bold", 17), hover_color="#207244",
              fg_color="#2A8C55", text_color="#fff").pack(side="left",
                                                          anchor="se",
                                                          pady=(30, 0),
                                                          padx=(0, 27))

    app.mainloop()
