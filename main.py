import customtkinter as ctk
import geopy
from tkintermapview import TkinterMapView
import tkintermapview
from sidebar import SideBar, LocationFrame
from settings import *


class MapViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        # window setup
        self.geometry('1200x800')
        self.title('Map')
        self.iconbitmap('map.ico')
        self.minsize(800, 600)
        self.entry_border_width = 0

        self.map_widget = TkinterMapView(self)
        self.map_widget.place(relx=0.2, rely=0, relwidth=0.8, relheight=1, anchor='nw')

        self.side = SideBar(self, self.map_widget)
        self.side.place(relx=0, rely=0, relwidth=0.2, relheight=1, anchor='nw')

        self.string_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self,
                                  fg_color=ENTRY_BG,
                                  corner_radius=0,
                                  font=(TEXT_FONT, TEXT_SIZE),
                                  textvariable=self.string_var)
        self.entry.place(relx=0.6, rely=0.95, anchor='center')

        self.entry.bind('<Return>', self.search_address)
        self.string_var.trace('w', self.reset_entry)

    def search_address(self, _):
        entered_city_name: str = self.string_var.get()
        city_coordinates: tuple | None = tkintermapview.convert_address_to_coordinates(entered_city_name)

        if city_coordinates:  # If the address exists
            # Go to new coordinates
            self.map_widget.set_position(*city_coordinates)
            # reset the zoom level
            self.map_widget.set_zoom(DEFAULT_ZOOM)

            # Get the address of new coordinates as an address object
            adr = tkintermapview.convert_coordinates_to_address(*city_coordinates)
            label: str = f'{adr.city}, {adr.country}'
            LocationFrame(parent=self.side.scrollable_frame,
                          label=label,
                          loc=city_coordinates,
                          map_obj=self.map_widget)
            # Clear the entry box
            self.string_var.set(value='')
        else:  # If the name is wrong
            # Change the entry border and text color to indicate a wrong location
            self.change_entry_color()
            # Debug prints
            print(city_coordinates)
            print('Doesn\'t exist')

    def reset_entry(self, *args):
        if self.entry_border_width != 0:
            self.change_entry_color(reset=True)

    def change_entry_color(self, reset=False):
        if reset:
            self.entry_border_width = 0
            self.entry.configure(border_width=0,
                                 text_color=TEXT_COLOR)
        else:
            self.entry_border_width += 1

            self.entry.configure(border_color='red',
                                 border_width=self.entry_border_width)
            if self.entry_border_width < 5:
                self.after(100, self.change_entry_color)
            else:
                # At the end change the color
                self.entry.configure(text_color='red')


if __name__ == '__main__':
    app = MapViewer()
    app.mainloop()
