import customtkinter as ctk
from PIL import Image
from settings import *


class SideBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=BUTTON_COLOR)
        self.scrollable_frame.pack(expand=True, fill='both')

        self.buttons_frame = ctk.CTkFrame(self, fg_color=SIDE_PANEL_BG)
        self.buttons_frame.pack(fill='x', ipady=15)

        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')

        # images
        street_img = ctk.CTkImage(Image.open(map_image_path))
        terrain_img = ctk.CTkImage(Image.open(terrain_image_path))
        paint_img = ctk.CTkImage(Image.open(paint_image_path))

        self.streets_button = ctk.CTkButton(self.buttons_frame,
                                            text='',
                                            image=street_img,
                                            width=60,
                                            height=30,
                                            fg_color=BUTTON_COLOR,
                                            hover_color=BUTTON_HOVER_COLOR,
                                            command=lambda: self.change_map(MAIN_URL))
        self.streets_button.grid(row=0, column=0)
        self.terrain_button = ctk.CTkButton(self.buttons_frame,
                                            text='',
                                            image=terrain_img,
                                            width=60,
                                            height=30,
                                            fg_color=BUTTON_COLOR,
                                            hover_color=BUTTON_HOVER_COLOR,
                                            command=lambda: self.change_map(TERRAIN_URL)
                                            )
        self.terrain_button.grid(row=0, column=1)

        self.paint_button = ctk.CTkButton(self.buttons_frame,
                                          text='',
                                          image=paint_img,
                                          width=60,
                                          height=30,
                                          fg_color=BUTTON_COLOR,
                                          hover_color=BUTTON_HOVER_COLOR,
                                          command=lambda: self.change_map(PAINT_URL)
                                          )
        self.paint_button.grid(row=0, column=2)

    def change_map(self, map):
        self.parent.map_widget.set_tile_server(map)
