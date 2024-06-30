import customtkinter as ctk
from tkintermapview import TkinterMapView
from sidebar import SideBar, LocationFrame
from settings import *
from geopy.geocoders import Nominatim
from collections import namedtuple

AddressObj = namedtuple('AddressObj', field_names=['latitude', 'longitude', 'city', 'country'])


def get_city_coordinates(city_name: str) -> None | AddressObj:
    """
    Retrieve the coordinates and address details for a given city name.

    Args:
        city_name (str): The name of the city to search for.

    Returns:
        None | AddressObj: An AddressObj containing latitude, longitude, city, and country if found,
                           or None if the location is not found.
    """

    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")

    # Make the API call
    location = geolocator.geocode(city_name)

    # Check if location is found
    if location:
        address = location.address.split(',')
        city = address[0].strip()
        country = address[-1].strip()

        return AddressObj(
            location.latitude,
            location.longitude,
            city,
            country,
        )
    else:  # If location is not found
        return None


class MapViewer(ctk.CTk):
    """
    A custom map viewer application using customtkinter and tkintermapview.

    This class creates a window with a map widget and a sidebar for location management.
    """

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light')
        # window setup
        self.geometry('1200x800+100+50')
        self.title('Map')
        self.iconbitmap('map.ico')
        self.minsize(800, 600)

        self.error = False
        # Create widgets
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
        """
        Search for an address based on the user input and update the map.

        This method is triggered when the user presses Enter in the search entry.
        It searches for the entered city, updates the map position, and adds the location to the sidebar.

        Args:
            _ : Ignored parameter (event object from key binding).
        """

        entered_city_name: str = self.string_var.get()
        address: AddressObj | None = get_city_coordinates(entered_city_name)

        if address:  # If the address exists
            # Go to new coordinates
            self.map_widget.set_position(address.latitude, address.longitude)

            if address.city != address.country:
                label: str = f'{address.city}, {address.country}'
            else:
                label: str = address.country

            LocationFrame(parent=self.side.scrollable_frame,
                          label=label,
                          loc=(address.latitude, address.longitude),
                          map_obj=self.map_widget)
            # Clear the entry box
            self.string_var.set(value='')
        else:  # If the name is wrong
            # Change the entry border and text color to indicate a wrong location
            self.change_entry_color()

    def change_entry_color(self, *args, reset=False):
        """
        Change the color of the entry widget to indicate search status.

        This method animates the entry border and text color when an error occurs in the search,
        or resets it to the default state.

        Args:
            *args: Variable length argument list (unused).
            reset (bool): If True, resets the entry color to default. If False, starts the error animation.
        """

        def animate():
            nonlocal color_index

            hex_border: str = COLOR_RANGE[color_index]
            hex_text: str = COLOR_RANGE[abs(color_index - 15)]

            border_color: str = f'#F{hex_border * 2}'
            text_color: str = f'#{hex_text}00'

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
