import customtkinter as ctk
from tkintermapview import TkinterMapView
import tkintermapview
from sidebar import SideBar, LocationFrame
from settings import *
from geopy.geocoders import Nominatim


def get_city_coordinates(city_name: str) -> None | tuple:
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")

    # Make the API call
    location = geolocator.geocode(city_name)
    print(location)

    # Check if location is found
    if location:
        return location.latitude, location.longitude
    else:
        return None


class MapViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light')
        # window setup
        self.geometry('1200x800+100+50')
        self.title('Map')
        self.iconbitmap('map.ico')
        self.minsize(800, 600)
        self.error = False

        self.map_widget = TkinterMapView(self)
        self.map_widget.place(relx=0.2, rely=0, relwidth=0.8, relheight=1, anchor='nw')

        self.side = SideBar(self, self.map_widget)
        self.side.place(relx=0, rely=0, relwidth=0.2, relheight=1, anchor='nw')

        self.string_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self,
                                  fg_color=ENTRY_BG,
                                  corner_radius=0,
                                  font=(TEXT_FONT, TEXT_SIZE),
                                  border_width=4,
                                  border_color=ENTRY_BG,
                                  textvariable=self.string_var,
                                  text_color=TEXT_COLOR)
        self.entry.place(relx=0.6, rely=0.95, anchor='center')

        self.entry.bind('<Return>', self.search_address)
        self.string_var.trace('w', lambda *args: self.change_entry_color(reset=True))

    def search_address(self, _):
        entered_city_name: str = self.string_var.get()
        # city_coordinates: tuple | None = tkintermapview.convert_address_to_coordinates(entered_city_name)
        city_coordinates: tuple | None = get_city_coordinates(entered_city_name)

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

    def change_entry_color(self, *args, reset=False):
        def animate():
            nonlocal color_index

            hex_border: str = COLOR_RANGE[color_index]
            hex_text: str = COLOR_RANGE[abs(color_index - 15)]

            border_color: str = f'#F{hex_border * 2}'
            text_color: str = f'#{hex_text}00'
            print(text_color)

            color_index -= 1
            self.entry.configure(border_color=border_color,
                                 text_color=text_color)
            if color_index >= 0:
                self.after(100, animate)

        color_index: int = 15

        if reset:
            if self.error:
                self.entry.configure(border_color=ENTRY_BG,
                                 text_color=TEXT_COLOR)
                self.error = False
        else:  # Error
            animate()
            self.error = True


if __name__ == '__main__':
    app = MapViewer()
    app.mainloop()
