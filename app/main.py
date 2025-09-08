from imports import *

from App import App
from Personalize import PersonalizePage

# Authorization
class Author(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user_id = "entry"
        self.title("Authorize yourself")
        self.geometry("500x450+175+90")
        self.resizable(False, False)
        self.iconbitmap("logo.ico")

        background_image = Image.open("img2.jpg")
        self.background_photo = ImageTk.PhotoImage(background_image)
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=('', 11), width=20)
        style.map("TButton", foreground=[("active", "white")], background=[("active", "#3498db")])

        container = ttk.Frame(self)
        container.pack(side="top", expand=True, fill="both")

        # first time creating frame and storing in frames list
        self.frames = {}
        for F in {Login, Signup, Forgotpass, Verify}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.rase_frame(Login)

    def rase_frame(self, curr_frame):
        self.frames[curr_frame].tkraise()

class Login(ttk.Frame, Author):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.login_user_value = tk.StringVar()
        self.login_pass_value = tk.StringVar()

        # login --- your code
        canvas = tk.Canvas(self, width=500, height=450)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=parent.background_photo, anchor="nw")

        login_heading = ttk.Label(self, text="Login", font=("Helvetica", 20, "bold"))
        login_heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        login_frame = ttk.Frame(self, padding="10")
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        username_label = ttk.Label(login_frame, text="Username:")
        username_entry = ttk.Entry(login_frame, font=("Arial", 12), textvariable=self.login_user_value)
        password_label = ttk.Label(login_frame, text="Password:")
        password_entry = ttk.Entry(login_frame, font=("Arial", 12), show="*", textvariable=self.login_pass_value)
        login_button = ttk.Button(login_frame, text="Login", command=lambda: self.click_log())
        forgot_password_label = ttk.Button(login_frame, text="Forgot Password?",
                                           command=lambda: Author.rase_frame(parent, Forgotpass))
        sign_up_label = ttk.Button(login_frame, text="Don't have an account?",
                                   command=lambda: Author.rase_frame(parent, Signup))

        username_label.grid(row=0, column=0, pady=10, sticky="w")
        username_entry.grid(row=0, column=1, pady=10)
        password_label.grid(row=1, column=0, pady=10, sticky="w")
        password_entry.grid(row=1, column=1, pady=10)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        forgot_password_label.grid(row=3, column=0, columnspan=2, pady=5)
        sign_up_label.grid(row=4, column=0, columnspan=2)

        parent.bind('<Return>', lambda event: self.click_log())

    def click_log(self):
        # username and password
        username = self.login_user_value.get()
        password = self.login_pass_value.get()
        f = switch_user(username, password)
        if f == 0:
            courser.execute("select userId from pro where userName='%s'" % username)
            global table_name
            table_name = courser.fetchone()['userId']
            row = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), table_name)
            courser.execute("update pro set lastLogin='%s' where userId='%s';" % row)
            db.commit()
            Author.destroy(self.parent)
        else:
            messagebox.showerror("Login", "Invalid Username or Password")


class Signup(ttk.Frame, Author):
    def __init__(self, parent, container):
        self.db = None
        self.courser = None
        self.parent = parent
        super().__init__(container)
        self.sign_user_value = tk.StringVar()
        self.sign_email_value = tk.StringVar()
        self.sign_pass_value = tk.StringVar()

        # Sign up --- your code
        canvas = tk.Canvas(self, width=500, height=450)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=parent.background_photo, anchor="nw")

        label_heading = ttk.Label(self, text="Sign Up", font=("Helvetica", 20, "bold"))
        signup_frame = ttk.Frame(self, padding="10")
        label_username = ttk.Label(signup_frame, text="Username: ")
        entry_username = ttk.Entry(signup_frame, font=("Arial", 12), textvariable=self.sign_user_value)
        label_email = ttk.Label(signup_frame, text="Email: ")
        entry_email = ttk.Entry(signup_frame, font=("Arial", 12), textvariable=self.sign_email_value)
        label_password = ttk.Label(signup_frame, text="Password: ")
        entry_password = ttk.Entry(signup_frame, font=("Arial", 12), show="*", textvariable=self.sign_pass_value)
        sign_up_button = ttk.Button(signup_frame, text="Sign Up", command=lambda: self.click_sign())
        back_to_login_label = ttk.Button(signup_frame, text="Already have an account? Log in!", cursor="hand2",
                                         command=lambda: Author.rase_frame(parent, Login))

        label_heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        signup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        label_username.grid(row=0, column=0, pady=10, sticky="w")
        entry_username.grid(row=0, column=1, pady=10)
        label_email.grid(row=1, column=0, pady=10, sticky="w")
        entry_email.grid(row=1, column=1, pady=10)
        label_password.grid(row=2, column=0, pady=10, sticky="w")
        entry_password.grid(row=2, column=1, pady=10)
        sign_up_button.grid(row=3, column=0, columnspan=2, pady=10)
        back_to_login_label.grid(row=5, column=0, columnspan=2)

    def click_sign(self):
        new_username = self.sign_user_value.get()
        new_email = self.sign_email_value.get()
        new_password = self.sign_pass_value.get()
        try:
            self.db = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=timeout,
                cursorclass=pymysql.cursors.DictCursor,
                db="money",
                host=os.environ.get('DB_HOST'),
                password=os.environ.get('DB_PASSWORD_ROOT'),
                read_timeout=timeout,
                port=12727,
                user=os.environ.get('DB_USER_ROOT'),
                write_timeout=timeout,
            )
            print("Connection successfully...")

        except pymysql.Error as e:
            print(f"Connection failed: {e}")

        no = random.randint(100,999)
        user_id = random.choice(["asd","fsd","hdf","bre"," nmu","oiu","asg"]) + str(no)
        self.courser = self.db.cursor()
        self.courser.execute("""CREATE TABLE %s ("SNo" integer NOT NULL,
          "Date" date,"Note" varchar(250) NOT NULL,
          "Type" varchar(125),
          "Mode" tinyint(1),
          "Amount" decimal(7,2) NOT NULL,
          PRIMARY KEY ("SNo"));""" % user_id)

        self.courser.execute("select max(SNo) from pro;")
        sno = self.courser.fetchone()['max(SNo)']+1
        new_user_row = (sno, user_id, new_username, new_password, new_email)
        self.courser.execute("insert into pro(SNo, userId, userName, password, email) "
                             "values(%s,%s,%s,%s,%s);",new_user_row)
        self.courser.execute("create user %s@%s identified by %s;", (new_username,'%', new_password))
        self.courser.execute("GRANT SELECT, INSERT ON money.%s TO %s@'%s';" % (user_id, new_username,'%'))

        # *messagebox
        print("new user is created.")
        Author.destroy(self.parent)
        personalize = PersonalizePage(user_id)
        personalize.mainloop()
        send_mail(new_email, "New Account", "Thank you for creating new account in our application.")
        Author().mainloop()

class Forgotpass(ttk.Frame, Author):
    code = random.randint(1000, 9999)

    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        ttk.Label(self, text="forgot password", font=('Times', '20')).pack()
        self.verify_user_value = tk.StringVar()
        self.verify_email_value = tk.StringVar()

        # forgot --- you code
        bg_label = tk.Label(self, image=parent.background_photo)
        bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        bg_label.image = parent.background_photo  # Keep a reference to avoid garbage collection

        # Frame with transparent background for input fields
        forgot_frame = tk.Frame(self, bg="white", bd=5)
        forgot_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_heading = ttk.Label(forgot_frame, text="Forgot Password", font=("Helvetica", 18, "bold"),
                                  background="white")
        username_label = ttk.Label(forgot_frame, text="Username:", background="white")
        username_entry_fp = ttk.Entry(forgot_frame, font=("Arial", 12), textvariable=self.verify_user_value)
        email_label = ttk.Label(forgot_frame, text="Email Address:", background="white")
        email_entry = ttk.Entry(forgot_frame, font=("Arial", 12), textvariable=self.verify_email_value)
        send_code_button = ttk.Button(forgot_frame, text="Send Code", command=lambda: self.send_code(str(self.code)))

        label_heading.grid(row=0, column=0, columnspan=2, pady=10)
        username_label.grid(row=1, column=0, pady=10, sticky="w")
        username_entry_fp.grid(row=1, column=1, pady=10)
        email_label.grid(row=2, column=0, pady=10, sticky="w")
        email_entry.grid(row=2, column=1, pady=10)
        send_code_button.grid(row=3, column=0, columnspan=2, pady=10)

    def send_code(self, code):
        to = self.verify_email_value.get()
        user = self.verify_user_value.get()
        try:
            courser.execute("select email from pro where userName='%s';" % user)
        except None:
            messagebox.showerror("Database", "User not found!")
            return

        if courser.fetchone()['email'] != to:
            messagebox.showerror("Error", "User entered dint matches email!")
            return

        global curr_user
        curr_user = user
        f = send_mail(to, "Your verification code is ", code)
        if f == 0:
            # *messagebox
            messagebox.showinfo("Success", "Verification code has been sent"
                                           " to your user email address successfully.")
            Author.rase_frame(self.parent, Verify)
        else:
            messagebox.showerror("Error", "Unable to send the email!")

class Verify(ttk.Frame, Author):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.verify_code_value = tk.IntVar()

        # verify --- your code
        canvas = tk.Canvas(self, width=500, height=450)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=parent.background_photo, anchor="nw")

        heading = ttk.Label(self, text="Verify your Email!", font=("Arial", 18, "bold"))
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        verify_f1 = ttk.Frame(self, padding="10")
        verify_f1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label1 = ttk.Label(verify_f1, text="The code has been sent to your email address.", font=("Arial", 15, "bold"))
        label2 = ttk.Label(verify_f1, text="Check your inbox and enter verification code below ot verify.",
                           font=("Arial", 13))
        verify_entry = ttk.Entry(verify_f1, textvariable=self.verify_code_value)
        submit_button = ttk.Button(verify_f1, text="Verify", width=15, command=lambda: self.now_verify())

        label1.pack(pady=8, padx=2)
        label2.pack(pady=8, padx=2)
        verify_entry.pack(pady=8, padx=2)
        submit_button.pack(pady=10)

    def now_verify(self):
        if self.verify_code_value.get() == Forgotpass.code:
            Author.rase_frame(self.parent, Login)

            courser.execute("select email, password from pro where userName='%s';" % curr_user)
            asq = courser.fetchone()

            send_mail(asq['email'], "your password: ", asq['password'])
            messagebox.showinfo("verification", "your password has been sent to your email address.")
        else:
            messagebox.showerror("Error", "Incorrect code entered!")


def send_mail(to, subject, message):
    g_username = os.environ.get('G_USERNAME')
    g_password = os.environ.get('G_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = g_username
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user=g_username, password=g_password)
        server.sendmail(from_addr=g_username, to_addrs=to, msg=msg.as_string())
        server.close()
        return 0
    except NameError:
        return 1


if __name__ == "__main__":
    courser = db.cursor()
    table_name = ""
    curr_user = ""

    author = Author()
    author.mainloop()
    author.quit()

    if table_name != "":
        app = App(table_name)
        app.mainloop()
