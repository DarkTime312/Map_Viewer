import customtkinter as ctk
import geopy
from tkintermapview import TkinterMapView
import tkintermapview
from sidebar import SideBar


class MapViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        # window setup
        self.geometry('1200x800')
        self.title('Map')
        self.iconbitmap('map.ico')
        self.minsize(800, 600)

        self.map_widget = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.map_widget.place(relx=0.2, rely=0, relwidth=0.8, relheight=1, anchor='nw')

        # set current widget position and zoom
        # map_widget.set_position(36.32899462230168, 59.6146859874632)  # Paris, France
        # map_widget.set_zoom(19)
        # self.map_widget.set_address("بیرجند")
        # adr = self.map_widget.get_position()
        #
        # adr = tkintermapview.convert_coordinates_to_address(*adr)
        # print(adr.street, adr.housenumber, adr.postal, adr.city, adr.state, adr.country, adr.latlng)

        SideBar(self).place(relx=0, rely=0, relwidth=0.2, relheight=1, anchor='nw')

        self.entry = ctk.CTkEntry(self)
        self.entry.place(relx=0.6, rely=0.95, anchor='center')
        self.entry.bind('<Return>', self.change_address)


    def change_address(self, _):
        city = self.entry.get()
        city_name = tkintermapview.convert_address_to_coordinates(city)

        if city_name:
            self.map_widget.set_position(*city_name)
            # self.map_widget.set_address(city)

            # adr = self.map_widget.get_position()
            adr = tkintermapview.convert_coordinates_to_address(*city_name)
            print(adr.city, adr.state, adr.country)
        else:
            self.entry.configure(border_color='red',
                                 border_width=1)
            print('Doesn\'t exist')

if __name__ == '__main__':
    app = MapViewer()
    app.mainloop()
