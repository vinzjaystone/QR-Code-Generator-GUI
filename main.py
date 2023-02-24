# This is a sample Python script.
import customtkinter as ctk
from tkinter import *
import json
import qrcode
import os
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
appWidth, appHeight = 400, 600


class App2(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("QR Generator")
        self.geometry(f"{appWidth}x{appHeight}")
        # Prevents the window from resizing
        self.resizable(False, False)

        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.isfile("data/settings.cfg"):
            f = open("data/settings.cfg", "w")
            x = {"entries": []}
            json.dump(x, f)
            f.close()

        # # Try to read config files for list of data to be collected
        file = open("data/settings.cfg", "r")
        cfg = json.load(file)
        file.close()

        # Now fill entries based on read files from config
        self.entries = []
        for e in cfg['entries']:
            self.entries.append(e)
        self.dynamic_widgets = {}
        self.text_variables = {}
        self.grid_columnconfigure(1, weight=3)

        # Create our Dynamic Widgets
        index = 0
        for w in self.entries:
            # Create text variable
            self.text_variables[w] = StringVar()
            self.text_variables[w].set("")

            # Create our Label
            col = 0
            widget = ctk.CTkLabel(self, text=str(w).capitalize() + ":")
            widget.grid(row=index, column=0, padx=5, pady=5, sticky="nsw")

            # Create our Entry
            widget_entry = ctk.CTkEntry(self, textvariable=self.text_variables[w])
            widget_entry.grid(row=index, column=col + 1, padx=5, pady=5, sticky="nsew")

            # Now add to our list/dictionary for reference/pointer later
            self.dynamic_widgets[w] = (widget, widget_entry)
            index += 1
            col += 1

        # Create our Generate button
        self.generateBtn = ctk.CTkButton(self, font=ctk.CTkFont(size=18, weight="bold"), text="GENERATE",
                                         command=self.generate)
        self.generateBtn.grid(row=index, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        index += 1

        # Create our QR PlaceHolder
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        # self.image = ctk.CTkImage(Image.open(os.path.join(image_path, "placeholderqr.png")), size=(300, 300))
        self.image = ctk.CTkImage(Image.open("data/placeholderqr.png"), size=(300, 300))
        # print(type(self.image))

        self.img_label = ctk.CTkLabel(self, image=self.image, compound="top", text="")
        self.img_label.grid(row=index, column=0, rowspan=index, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Resize window size(height, width) based on number of widgets
        total_height = 0
        for w in self.entries:
            total_height += self.dynamic_widgets[w][0].winfo_reqheight()
            total_height += 10
        total_height += self.generateBtn.winfo_reqheight()
        total_height += 10
        # Add qr image size
        total_height += 300
        total_height += 10

        print(total_height)
        self.update_idletasks()
        self.geometry("%dx%d" % (appWidth, total_height))

    def generate(self):
        result = {}
        name = self.entries[0]
        filename = self.text_variables[name].get()
        for w in self.entries:
            # get entries text variable values
            result[w] = self.text_variables[w].get()
        final = json.dumps(result)
        print(f"Json object : {final}")

        # Generate QR
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(final)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{filename}-QR.png")

        # Update our QR Preview Image
        self.image = ctk.CTkImage(img.get_image(), size=(300, 300))
        self.img_label.configure(image=self.image)
        self.img_label.image = self.image

        # Now clear or entry to prepare new entry
        # self.clear_inputs()

    def clear_inputs(self):
        for e in self.entries:
            self.text_variables[e].set("")


if __name__ == "__main__":
    app = App2()
    app.mainloop()
