import os
from dotenv import load_dotenv
import pymysql
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Management(tk.Tk):
    def __init__(self, username, password):
        super().__init__()
        timeout = 10
        try:
            self.db = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=timeout,
                cursorclass=pymysql.cursors.DictCursor,
                db="money",
                host=os.environ.get('DB_HOST'),
                password=password,
                read_timeout=timeout,
                port=12727,
                user=username,
                write_timeout=timeout,
            )
            print("Connection successfully...for user", self.db.user.decode("utf-8"))
        except pymysql.Error as e:
            print("invalid credentials, you are not admin.")
            Management.destroy(self)

        self.courser = self.db.cursor()
        self.title("User Management")
        self.geometry("800x530+175+90")

        # style
        style = ttk.Style()
        style.configure("TLabel", font=('', 13), width=14)
        style.configure("TButton", font=('', 12), width=13)

        ttk.Label(self, text="User Management.").pack()
        user_entry = ttk.Entry(font=('', 12), width=13)
        user_entry.insert(0, string="userId:")
        user_entry.pack()
        ttk.Button(text="Delete", command=lambda: self.delete_user(user_entry.get())).pack()

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.config(yscrollcommand = scrollbar.set)
        self.f1 = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.f1, anchor="nw")

        ttk.Label(self.f1, text="SNo").grid(row=0, column=0)
        ttk.Label(self.f1, text="userId").grid(row=0, column=1)
        ttk.Label(self.f1, text="userName").grid(row=0, column=2)
        ttk.Label(self.f1, text="email").grid(row=0, column=3)
        self.show_users()

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_users(self):
        self.courser.execute("select userId,userName,email from pro;")
        asq = [list(row.values()) for row in self.courser.fetchall()]
        i = 1
        for t in asq:
            ttk.Label(self.f1, text=i).grid(row=i, column=0)
            ttk.Label(self.f1, text=t[0]).grid(row=i, column=1)
            ttk.Label(self.f1, text=t[1]).grid(row=i, column=2)
            ttk.Label(self.f1, text=t[2]).grid(row=i, column=3, columnspan=2)
            i += 1

    def delete_user(self, user_id):
        try:
            self.courser.execute("drop table %s;" % user_id)
            self.courser.execute("select userName from pro where userId = '%s'" % user_id)
            self.courser.execute("drop user %s@'%s'" % (self.courser.fetchone()['userName'], '%'))
            self.courser.execute("delete from pro where userId = '%s'" % user_id)
        except None:
            print("unable to delete particular user.")

        print("you are so gon.",user_id)
        self.db.commit()
        self.show_users()



def login():
    root = tk.Tk()
    root.geometry('500x450')
    username = tk.StringVar()
    password = tk.StringVar()

    background_image = Image.open("img2.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=('', 11), width=20)
    style.map("TButton", foreground=[("active", "white")], background=[("active", "#3498db")])

    canvas = tk.Canvas(root, width=500, height=450)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    login_heading = ttk.Label(root, text="Login", font=("Helvetica", 20, "bold"))
    login_heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    login_frame = ttk.Frame(root, padding="10")
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    username_label = ttk.Label(login_frame, text="Username:")
    username_entry = ttk.Entry(login_frame, font=("Arial", 12), textvariable=username)
    password_label = ttk.Label(login_frame, text="Password:")
    password_entry = ttk.Entry(login_frame, font=("Arial", 12), show="*", textvariable=password)
    login_button = ttk.Button(login_frame, text="Login", command=lambda: login_admin(root, username.get(), password.get()))

    username_label.grid(row=0, column=0, pady=10, sticky="w")
    username_entry.grid(row=0, column=1, pady=10)
    password_label.grid(row=1, column=0, pady=10, sticky="w")
    password_entry.grid(row=1, column=1, pady=10)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)
    root.mainloop()

def login_admin(root, username, password):
    root.destroy()
    global user, passw
    user = username
    passw = password
    root.quit()


if __name__ == "__main__":
    load_dotenv()
    user = passw = ""
    login()
    management = Management(username=user, password=passw)
    management.mainloop()
