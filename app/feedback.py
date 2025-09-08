from imports import tk, ttk, messagebox, db, datetime
from random import randint

# This class for FeedBack page
class FBPage(ttk.Frame):
    def __init__(self, parent, container, table):
        super().__init__(container)
        self.parent = parent
        self.table = table
        self.courser = db.cursor()

        f1 = ttk.Frame(self, padding=10)
        f2 = ttk.Frame(self, padding=10, relief="solid", borderwidth=1)
        f2.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        f1.pack(side='right', fill='y', expand=True, padx=10, pady=10)

        ttk.Label(f1, text="Developer", font=('Times', '20', 'bold')).pack(padx=4, pady=5)
        developers = ["--Akshat Chourey--", "--Shorya Pathak--", "--Rudra Gupta--",
                      "--Tanushri Rajesh--", "--Vanshika Dhaka--"]
        for dev in developers:
            ttk.Label(f1, text=dev, font=('Helvetica', 12)).pack(padx=1, pady=3)
        ttk.Label(f1, text="Contact Info", font=('Times', '20', 'bold')).pack(pady=5)
        ttk.Label(f1, text="achourey09@..").pack(pady=3)
        ttk.Label(f1, text="shoryapathak07@..").pack(pady=3)

        # values
        self.name = tk.StringVar()
        self.age = tk.IntVar()
        self.email = tk.StringVar()

        ttk.Label(f2, text="Feedback Form", font=("Times", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(f2, text="Name:", font=("Helvetica", 15)).grid(row=1, column=0, pady=7, padx=5, sticky='e')
        ttk.Entry(f2, textvariable=self.name,font=("Helvetica", 15)).grid(row=1, column=1, pady=7, padx=5, sticky='w')
        ttk.Label(f2, text="Age:", font=("Helvetica", 15)).grid(row=2, column=0, pady=7, padx=5, sticky='e')
        ttk.Entry(f2, textvariable=self.age, font=("Helvetica", 15)).grid(row=2, column=1, pady=7, padx=5, sticky='w')
        ttk.Label(f2, text="Email:", font=("Helvetica", 15)).grid(row=3, column=0, pady=7, padx=5, sticky='e')
        ttk.Entry(f2, textvariable=self.email, font=("Helvetica", 15)).grid(row=3, column=1, pady=7, padx=5, sticky='w')
        ttk.Label(f2, text="Feedback:", font=("Helvetica", 15)).grid(row=4, column=0, pady=7, padx=5, sticky='ne')
        self.test_box = tk.Text(f2, height=7, width=30,font=("Helvetica", 15))
        self.test_box.grid(row=4, column=1, pady=7, padx=5, sticky='w')

        submit_button = ttk.Button(f2, text="Submit", command=lambda: self.submit_feedback())
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_feedback(self):
        note = self.test_box.get("1.0", tk.END)
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = (randint(10000, 99999), self.table, self.name.get(), self.age.get(), self.email.get(), note, time)
        self.courser.execute("insert into money.feedback value(Sno=''+1, %s,%s,%s,%s,%s,%s,%s);", row)
        db.commit()
        messagebox.showinfo("Feedback", "Thank you for your valuable feedback.")
