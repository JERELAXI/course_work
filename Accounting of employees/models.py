import sqlite3

from libs.CTkTable import CTkTable


class Employee:
    def __init__(self, name, position, salary, phone_number, age):
        self.name = name
        self.position = position
        self.salary = salary
        self.phone_number = phone_number
        self.age = age


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                position TEXT,
                salary INTEGER,
                phone_number TEXT,
                age INTEGER
            )
        """)
        self.conn.commit()

    def add_employee(self, employee):
        self.cursor.execute(
            "INSERT INTO employees (name, position, salary,"
            " phone_number, age) VALUES (?, ?, ?, ?, ?)",
            (employee.name, employee.position, employee.salary,
             employee.phone_number, employee.age)
        )
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()


class EmployeeTable:
    def __init__(self, db_manager, table_frame):
        self.db_manager = db_manager
        self.table_frame = table_frame
        self.table = None

    def create_table(self):
        rows = self.db_manager.get_employees()
        table_data = [["ID", "ПІБ", "Посада", "Зарплата", "Телефон", "Вік"]]
        for row in rows:
            formatted_row = [str(cell) for cell in row]
            table_data.append(formatted_row)
        self.table = CTkTable(master=self.table_frame, values=table_data,
                              colors=["#E6E6E6", "#EEEEEE"],
                              header_color="#2A8C55",
                              hover_color="#B4B4B4")
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.set_column_widths()
        self.table.pack(expand=True)

    def update_table(self, search_text):
        self.db_manager.cursor.execute(
            "SELECT * FROM employees WHERE name LIKE ?",
            (f"%{search_text}%",))
        rows = self.db_manager.cursor.fetchall()
        table_data = [["ID", "ПІБ", "Посада", "Зарплата", "Телефон", "Вік"]] + \
                     [[str(cell) for cell in row] for row in rows]
        self.table.update_values(table_data)
        self.set_column_widths()

    def delete_employee(self, row_number):
        self.db_manager.cursor.execute("DELETE FROM employees WHERE id=?",
                                       (row_number,))
        self.db_manager.conn.commit()
        rows = self.db_manager.get_employees()
        table_data = [["ID", "ПІБ", "Посада", "Зарплата", "Телефон", "Вік"]] + \
                     [[str(cell) for cell in row] for row in rows]
        self.table.update_values(table_data)
        self.set_column_widths()

    def set_column_widths(self):
        self.table.set_column_width(0, 10)
        self.table.set_column_width(1, 80)
        self.table.set_column_width(2, 20)
        self.table.set_column_width(3, 10)
        self.table.set_column_width(4, 5)
        self.table.set_column_width(5, 2)
