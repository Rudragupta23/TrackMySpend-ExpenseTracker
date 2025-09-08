from imports import tk, ttk
from imports import Image, ImageTk

# This class only has image
class HomePage(ttk.Frame):
    def __init__(self, parent, container, table):
        super().__init__(container)

        # Importing image(in variable background), creating canvas, pack image in canvas in nw.
        self.background = Image.open("img1.jpg").resize((948,767))
        self.background_tk = ImageTk.PhotoImage(self.background)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')
        self.canvas.create_image(0, 0, image=self.background_tk, anchor='nw')
        self.canvas.bind('<Configure>', self.resize_image)

    # this function resizes the image according to img aspect ratio.
    def resize_image(self, event):
        image_ratio = 1.75
        canvas_ratio = event.width / event.height

        if canvas_ratio > image_ratio:  # canvas is wider then image
            width = event.width
            height = int(event.width / image_ratio)
        else:  # canvas is narrower then image
            height = event.height
            width = int(event.height * image_ratio)

        new_background = self.background.resize((width, height))
        self.background_tk = ImageTk.PhotoImage(new_background)
        self.canvas.create_image(int(event.width/2), int(event.height/2), image=self.background_tk, anchor='center')
