from customtkinter import *

app = CTk()
app.geometry("856x645")
app.resizable(0, 0)

set_appearance_mode("light")


def start_app():
    import main
    main.create_interface(app)
    app.mainloop()


start_app()
