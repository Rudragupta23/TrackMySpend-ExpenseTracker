from imports import tk, ttk, database
import numpy as np
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# This class is for analyzing the data.
class AnalysePage(ttk.Frame):
    def __init__(self, parent, container, table):
        super().__init__(container)
        self.table = table
        self.courser = database().cursor()
        self.data = self.get_data()

        menu = ttk.Frame(self)
        menu.pack(side='top', fill='x')

        home = ttk.Button(menu, text="Home Page", command=lambda: self.create_frame(AnalyseHome))
        graph1 = ttk.Button(menu, text="Graph 1", command=lambda: self.create_frame(GraphP1))
        graph2 = ttk.Button(menu, text="Graph 2", command=lambda: self.create_frame(GraphP2))
        graph3 = ttk.Button(menu, text="Graph 3", command=lambda: self.create_frame(GraphP3))

        home.pack(side='left')
        graph1.pack(side='left')
        graph2.pack(side='left')
        graph3.pack(side='left')

        self.container = ttk.Frame(self)
        self.container.pack(side="top", expand=True, fill="both")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.create_frame(AnalyseHome)

    def create_frame(self, frame):
        if frame not in self.frames:
            new_frame = frame(self, self.container)
            self.frames[frame] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")

        self.frames[frame].tkraise()

    def get_data(self):
        self.courser.execute("select * from %s order by Date desc;" % self.table)
        return [list(row.values()) for row in self.courser.fetchall()]

class AnalyseHome(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        ttk.Label(self, text="linear regression graph", width=False).pack()

        parent.courser.execute(f'''SELECT DATE_FORMAT(date, '%Y-%m') AS month,
                                    SUM(CASE WHEN Amount < 0 THEN Amount ELSE 0 END) AS negative_amount
                                        FROM {parent.table} GROUP BY DATE_FORMAT(date, '%Y-%m') ORDER BY month''')

        negative_amount = []
        for i in parent.courser.fetchall():
            negative_amount.append(float(abs(i["negative_amount"])))

        x = np.arange(len(negative_amount))
        y = np.array(negative_amount)

        fig = Figure(figsize=(7, 6), dpi=110)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(expand=True, fill='both', padx=20, pady=20)
        plt = fig.add_subplot(111)

        m, b = np.polyfit(x, y, 1)
        plt.scatter(x, y, label='Data points')
        plt.plot(x, m * x + b, color='red', linestyle='--', label=f'y = {m:.1f}x + {b:.1f}')

        plt.set_xlabel('Months')
        plt.set_ylabel('Amount')
        plt.legend()
        canvas.draw()

class GraphP1(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        type_value = tk.StringVar(value="all entries")

        frame1 = ttk.Frame(self)
        frame1.pack()
        ttk.Label(frame1, text="Graph page 1").pack()
        ttk.Button(frame1, command=lambda: self.draw_graph(type_value.get()), text="Draw Graph").pack(side='left')
        ttk.Button(frame1, command=lambda: self.clear_graph(), text="Clear Graph").pack(side='left')

        types = ["food", "pocket money", "friend/partner", "stationary", "events", "personal", "shopping", "other", "all entries"]
        type_entry = ttk.Combobox(frame1, textvariable=type_value)
        type_entry['value'] = types
        type_entry.pack()

        self.fig = Figure(figsize=(7, 6), dpi=110)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand=True, fill='both', padx=20, pady=20)
        self.plt = self.fig.add_subplot(111)
        self.plt.set_title("Graph")
        self.plt.set_ylabel("Amount")
        self.plt.set_xlabel("Entries")

    def clear_graph(self):
        self.fig.clf()
        self.plt = self.fig.add_subplot(111)
        self.plt.set_title("Graph")
        self.plt.set_ylabel("Amount")
        self.plt.set_xlabel("Entries")
        self.canvas.draw()

    def draw_graph(self, name):
        if name == "all entries":
            arr = [i[5] for i in self.parent.data]
        else:
            arr = []
            for i in self.parent.data:
                if i[3] == name: arr.append(i[5])

        x_axis = np.arange(len(arr))
        self.plt.plot(x_axis, arr, label=name)
        self.plt.legend()
        self.canvas.draw()


class GraphP2(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        ttk.Label(self, text="Spending by months", width=False).pack()

        parent.courser.execute(f'''SELECT DATE_FORMAT(date, '%Y-%m') AS month,
                                SUM(CASE WHEN Amount > 0 THEN Amount ELSE 0 END) AS positive_amount,
                                SUM(CASE WHEN Amount < 0 THEN Amount ELSE 0 END) AS negative_amount
                                FROM {parent.table} GROUP BY DATE_FORMAT(date, '%Y-%m') ORDER BY month''')

        months, positive_amount, negative_amount = [],[],[]
        for i in parent.courser.fetchall():
            months.append(i["month"])
            positive_amount.append(i["positive_amount"])
            negative_amount.append(abs(i["negative_amount"]))

        x_axis = np.arange(len(months))

        fig = Figure(figsize=(7, 6), dpi=110)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(expand=True, fill='both', padx=20, pady=20)
        plt = fig.add_subplot(111)

        bar_width = 0.35
        opacity = 0.8
        plt.bar(x_axis, positive_amount, bar_width, alpha=opacity, color='b', label="Credited Amounts")
        plt.bar(x_axis + bar_width, negative_amount, bar_width, alpha=opacity, color='g', label="Debited Amounts")

        plt.set_xlabel('Months')
        plt.set_ylabel('Amount')
        plt.set_xticks(x_axis + bar_width, months)
        plt.legend()
        canvas.draw()

class GraphP3(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        ttk.Label(self, text="Distribution of Data", width=False).pack()
        parent.courser.execute("select Type, sum(Amount) as totalPrice from %s group by Type;" % parent.table)
        data = [list(row.values()) for row in parent.courser.fetchall()]
        labels = [i[0] for i in data]
        total_price = [abs(i[1]) for i in data]

        fig = Figure(figsize=(5, 4), dpi=110)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(expand=True, fill='both', padx=10, pady=10)
        plt = fig.add_subplot(111)
        sns.set_style("whitegrid")
        plt.pie(total_price, labels=labels, autopct='%1.1f%%', startangle=140)

        canvas.draw()
