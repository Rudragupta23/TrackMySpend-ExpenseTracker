from imports import tk, ttk, messagebox
from imports import Image, ImageTk
from imports import db, database

# This class is Profile page
class ProfilePage(ttk.Frame):

    def __init__(self, parent, container, table):
        super().__init__(container)
        self.table = table
        self.courser = db.cursor()
        self.parent = parent
        self.courser.execute("select fullName,email,phoneNo,note,averageM,prediction from pro where userId=%s", table)
        asq = list(self.courser.fetchone().values())
        self.prediction = tk.DoubleVar(value=0.00)

        # your --- code here
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0,weight=1)
        f1 = ttk.Frame(self)
        f2 = ttk.Frame(self)
        f1.grid(row=0, column=0, sticky="nsew")
        f2.grid(row=1, column=0, sticky="nsew")

        f2.rowconfigure(0, weight=1)
        f2.columnconfigure(0, weight=2)
        f2.columnconfigure(1, weight=1)
        f21 = ttk.Frame(f2, relief="groove", borderwidth=2)
        f22 = ttk.Frame(f2, relief="raised", borderwidth=2)
        f21.grid(row=0, column=0, sticky="nsew", columnspan=2)
        f22.grid(row=0, column=3, sticky="nse", padx=14, pady=9)

        ttk.Label(f1, text="Profile Page", font=('Times', '20')).pack()
        canvas = tk.Canvas(f1, width=200, height=200)
        canvas.pack(side='left', anchor="nw", padx=5, pady=5)
        canvas.create_image(100, 100, image=parent.photo_image)

        ttk.Label(f1, text=f"{asq[0]}\n{asq[1]}\n{asq[2]}", font=('Times', 23)).pack(side='left', anchor='nw',pady=60)
        ttk.Button(f1, text="Change Password", command=lambda:self.change_password()).pack(padx=5)
        ttk.Button(f1, text="LogOut", command=lambda:self.logout()).pack(padx=5)

        ttk.Label(f21, text="Note").pack()
        text_box = tk.Text(f21, height=11, width=55, font=("Helvetica", 15))
        text_box.pack()
        text_box.insert('1.0', str(asq[3]))
        ttk.Button(f21, text="Save", command=lambda:self.save_note(text_box.get("1.0", tk.END)), width=10).pack()

        ttk.Label(f22, text="Balance: ").grid(row=0, column=0)
        ttk.Label(f22, textvariable=parent.balance, foreground='blue').grid(row=0, column=1)
        ttk.Label(f22, text="Goal: ").grid(row=1, column=0)
        ttk.Label(f22, textvariable=parent.goal, foreground='green').grid(row=1, column=1)
        ttk.Label(f22, text="Spent: ").grid(row=2, column=0)
        ttk.Label(f22, textvariable=parent.spent, foreground='red').grid(row=2, column=1)
        ttk.Label(f22, text="Current Average: ").grid(row=3, column=0)
        ttk.Label(f22, text=asq[4], foreground='blue').grid(row=3, column=1)
        ttk.Label(f22, text="Prediction: ").grid(row=4, column=0)
        ttk.Label(f22, textvariable=self.prediction, foreground='blue').grid(row=4, column=1)
        ttk.Label(f22, text="",).grid(row=5, column=0)
        ttk.Label(f22, text="Set your new goal:").grid(row=6, column=0)
        ttk.Entry(f22, textvariable=parent.goal).grid(row=7, column=0)
        ttk.Button(f22, text="change", command=lambda:self.change_goal(), width=12).grid(row=7, column=1)

        ttk.Label(f22, text="").grid(row=8, column=0)
        ttk.Button(f22, text="Get Prediction", command=lambda:self.get_prediction(asq[5])).grid(row=9, column=0, columnspan=2)

    def logout(self):
        database().close()
        db.close()
        self.parent.destroy()
        self.parent.quit()

    def change_goal(self):
        self.courser.execute("update pro set goal=%s,spent=0 where userId='%s';" % (self.parent.goal.get(),self.table))
        db.commit()
        self.parent.get_balance()
        messagebox.showinfo("Goal changed", f"Goal changed\nYour new goal is {self.parent.goal.get()}.")

    def get_prediction(self, amount):
        messagebox.showinfo("Ai Initiated", "your predicted spending for next month is updated")
        self.prediction.set(amount)

    def save_note(self, notes):
        self.courser.execute("update pro set note='%s' where userId='%s';" % (notes, self.table))
        db.commit()
        messagebox.showinfo("Saving..", "Your notes is successfully saved.")

    def change_password(self):
        top = tk.Toplevel()
        top.title("Enter New Password")
        top.geometry("500x450")

        background_image = Image.open("img2.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        canvas = tk.Canvas(top, width=500, height=450)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=background_photo, anchor="nw")
        style = ttk.Style()
        style.configure("TButton", font=('', 11), width=20)
        style.map("TButton", foreground=[("active", "white")], background=[("active", "#3498db")])

        frame1 = ttk.Frame(top)
        frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_heading = ttk.Label(frame1, text="Enter New Password", font=("Helvetica", 18, "bold"), padding=12)
        old_pass_label = ttk.Label(frame1, text="Old Password: ", font=("Arial", 12), padding=7)
        old_pass = ttk.Entry(frame1, font=("Arial", 12), show="*", width=20)
        new_pass_label = ttk.Label(frame1, text="New Password: ", font=("Arial", 12), padding=7)
        new_pass = ttk.Entry(frame1, font=("Arial", 12), show="*", width=20)
        confirm_pass_label = ttk.Label(frame1, text="Confirm Password: ", font=("Arial", 12), padding=7)
        confirm_pass = ttk.Entry(frame1, font=("Arial", 12), show="*", width=20)

        submit_pass = ttk.Button(frame1, text="Change",command=lambda:self
                                 .new_password(top,old_pass.get(), new_pass.get(),confirm_pass.get()), padding=12)

        label_heading.grid(row=0, column=0, columnspan=2)
        old_pass_label.grid(row=1, column=0)
        old_pass.grid(row=1, column=1)
        new_pass_label.grid(row=2, column=0)
        new_pass.grid(row=2, column=1)
        confirm_pass_label.grid(row=3, column=0)
        confirm_pass.grid(row=3, column=1)
        submit_pass.grid(row=4, column=0, columnspan=2)

        top.mainloop()

    def new_password(self, top, old_pass, new_pass, confirm_pass):
        self.courser.execute("select password,userName from pro where userId='%s';" % self.table)
        asq = self.courser.fetchone()
        if asq['password'] != old_pass:
            messagebox.showerror("Error", "Old Password is incorrect")
            return
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Confirm password is not matching new Password")
            return
        self.courser.execute("update pro set password='%s' where userId='%s';" % (new_pass, self.table))
        self.courser.execute("alter user %s@%s identified by %s;", (asq['userName'],'%', new_pass))
        messagebox.showinfo("Saving..", "Password successfully saved.\nPl restart our app.")
        top.destroy()
