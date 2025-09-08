import io
from imports import os
from imports import Client
from imports import tk, ttk
from imports import datetime
from imports import load_dotenv
from imports import Image, ImageTk
from tkinter.filedialog import askopenfilename
from imports import db

class PersonalizePage(tk.Tk):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.title("Personalize Page")
        self.iconbitmap("logo.ico")
        self.geometry("890x570+175+90")
        self.configure(bg="#eef2f7")
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)

        # Styles
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 12), background="#eef2f7", foreground="#333")
        style.configure("TButton", font=("Segoe UI", 11), background="#0078D7", foreground="black")
        style.map("TButton", background=[("active", "#005A9E")], foreground=[("active", "black")])

        center_frame = tk.Frame(self, bg="#eef2f7")
        center_frame.pack(expand=True, fill="both")
        # Title
        ttk.Label(center_frame,text="Personalize Page",font=("Times", 20, "bold"),anchor="center",background="#eef2f7").pack(pady=10)

        ttk.Label(center_frame,text="Scan this QR code to send a message and use our WhatsApp services.",
            anchor="center",wraplength=700,font=("Segoe UI", 11),background="#eef2f7",).pack(pady=5)

        # placeholders
        self.file = tk.StringVar(value="No file selected")
        fName_value = tk.StringVar()
        phone_value = tk.StringVar(value="+91")
        balanceOn_value = tk.DoubleVar()
        balanceOf_value = tk.DoubleVar()
        goal_value = tk.IntVar()
        gender_value = tk.StringVar(value="Select")
        age_value = tk.IntVar()

        # Main Frame for Content
        main_frame = ttk.Frame(center_frame, padding=10)
        main_frame.pack(padx=20, pady=20, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=20, sticky="n")

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=20, sticky="n")

        # QR Code
        qr_image = Image.open("whatsapp QR.jpg").resize((200, 200), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(image=qr_image)
        canvas = tk.Canvas(left_frame, width=200, height=200, bg="white", highlightthickness=0)
        canvas.create_image((100, 100), image=self.photo_image)
        canvas.pack(pady=10)
        ttk.Label(right_frame, text="Upload Photo:").grid(row=0, column=0, pady=8, sticky="w")
        ttk.Button(right_frame, text="Upload", command=self.upload_file).grid(row=0, column=1, pady=8, padx=10, sticky="w")
        ttk.Label(right_frame,textvariable=self.file,font=("Segoe UI", 9),
                  foreground="#555").grid(row=0, column=2, padx=5, pady=8, sticky="w")

        # Input Layout
        inputs = [
            ("Full Name:", ttk.Entry(right_frame, textvariable=fName_value)),
            ("Phone No:", ttk.Entry(right_frame, textvariable=phone_value)),
            ("Balance Online:", ttk.Entry(right_frame, textvariable=balanceOn_value)),
            ("Balance Offline:", ttk.Entry(right_frame, textvariable=balanceOf_value)),
            ("Monthly Goal:", ttk.Entry(right_frame, textvariable=goal_value)),
            ("Gender:", ttk.Combobox(right_frame, textvariable=gender_value,
                                     values=["Male", "Female", "Other"],state="readonly")),
            ("Age:", ttk.Entry(right_frame, textvariable=age_value)),
        ]

        for idx, (label, widget) in enumerate(inputs):
            ttk.Label(right_frame, text=label).grid(row=idx+1, column=0, pady=8, sticky="w")
            widget.grid(row=idx+1, column=1, pady=8, padx=10, sticky="w")

        # Save Button
        ttk.Button(right_frame, text="Save Data",command=lambda: self.save_data(
            fName_value, phone_value, balanceOn_value, balanceOf_value, goal_value, gender_value, age_value)
                   ).grid(row=8, column=0, columnspan=2, pady=20)

    def upload_file(self):
        f_types = [('Jpg Files', '*.jpg'), ('Png files','*.png')]
        file = askopenfilename(filetypes=f_types)
        self.file.set(file)

    def save_data(self,fName_value,phone_value,balanceOn_value,balanceOf_value,goal_value, gender_value, age_value):
        # first message by twilio
        load_dotenv()
        account_sid = os.environ.get('Twilio_sid')
        auth_token = os.environ.get('Twilio_token')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body="""Welcome to our WhatsApp services.
To add your transactions efficiently use the following formate:

"Note" "mode:onl/off" "amount"

Ex- "english event" onl 250

For correct functioning keep this in mind
Money given --> -250
Money get   -->  250

Use sync button in add transition page to update entries. Thank you""",
            to=f'whatsapp:{phone_value.get()}'
        )

        courser = db.cursor()
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = (fName_value.get(), phone_value.get(), gender_value.get(), age_value.get(),
               balanceOn_value.get(), balanceOf_value.get(), goal_value.get(), time, self.table)
        courser.execute("update pro set fullName=%s, phoneNo=%s, gender=%s, age=%s, balanceOn=%s,"
                        "balanceOf=%s, goal=%s, lastSync=%s where userId=%s;", row)

        if self.file.get() == "No file selected": self.file.set("testImage.jpg")
        img = open(self.file.get(), "rb").read()
        courser.execute("select max(SNo) from proImg;")
        temp_no = courser.fetchone()['max(SNo)'] + 1
        courser.execute("insert into proImg values(%s,%s,%s);", (temp_no, self.table, img))
        db.commit()

        print("Saving...personal data.")
        self.destroy()
        self.quit()
