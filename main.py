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
        self.bd = 0

        self.map_widget = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.map_widget.place(relx=0.2, rely=0, relwidth=0.8, relheight=1, anchor='nw')

        # set current widget position and zoom
        self.map_widget.set_position(36.32899462230168, 59.6146859874632)  # Paris, France
        self.map_widget.set_zoom(19)

        self.side = SideBar(self)
        self.side.place(relx=0, rely=0, relwidth=0.2, relheight=1, anchor='nw')

        self.entry = ctk.CTkEntry(self, fg_color=ENTRY_BG, corner_radius=0, font=(TEXT_FONT, TEXT_SIZE))
        self.entry.place(relx=0.6, rely=0.95, anchor='center')
        self.entry.bind('<Return>', self.change_address)
        self.entry.bind('<BackSpace>', self.test)

    def change_address(self, _):
        city = self.entry.get()
        city_name = tkintermapview.convert_address_to_coordinates(city)

        if city_name:
            self.map_widget.set_position(*city_name)

            adr = tkintermapview.convert_coordinates_to_address(*city_name)
            label = f'{adr.city}, {adr.country}'
            LocationFrame(parent=self.side.scrollable_frame,
                          label=label,
                          loc=city_name,
                          map_obj=self.map_widget)
            self.entry.delete(0, 'end')
        else:
            self.change_entry_color()

            LocationFrame(parent=self.side.scrollable_frame,
                          label='test',
                          loc=(43, 45),
                          map_obj=self.map_widget)

            print('Doesn\'t exist')

    def test(self, _):
        self.bd = 0
        self.entry.configure(border_width=0, text_color=TEXT_COLOR)

    def change_entry_color(self):
        self.bd += 1

        self.entry.configure(border_color='red',
                             border_width=self.bd)
        if self.bd < 5:
            self.after(100, self.change_entry_color)
        else:
            self.entry.configure(text_color='red')


if __name__ == '__main__':
    app = MapViewer()
    app.mainloop()
