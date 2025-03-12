import tkinter as tk
import numpy as np
from tkintermapview import TkinterMapView
from tkinter import simpledialog
import utm
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, PhotoImage
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.svm import SVR
from light_attenuation import LightAttenuationApp
from tkinter import scrolledtext
from PIL import Image, ImageTk
import csv
from tkinter import font
import os
import webview
from tkhtmlview import HTMLLabel
import json
import random


class App():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Non attenuation points
        self.coor_point = []
        self.sqm_value = []
        self.marker_list = []

        # Attenuation points
        self.coor_point2 = []
        self.sqm_value2 = []
        self.C1 = []
        self.C2 = []
        self.profile = []
        self.marker_list2 = []        
        self.SI_Choice = 0  # 0 IDW
        self.map_list = []
        self.win = tk.Tk()
        # Create a frame
        frame = tk.Frame(self.win, width=90, height=100, bg="gray")
        frame.pack(side="left", fill="y")  # Pack the frame to the left side and fill it vertically
        self.image_SQM = Image.open("button_img/SQM.png")
        self.photo_SQM = ImageTk.PhotoImage(self.image_SQM.resize((30,30)))
        label = tk.Label(frame, image=self.photo_SQM, text="SQM Values", bg="gray" , compound ="left" , font=("Helvetica", 12, "bold"))
        label.pack(pady=10)
        self.image_ping = Image.open("button_img/pin2.png")
        self.photo_ping = ImageTk.PhotoImage(self.image_ping.resize((30,30)))
        label_IDW = tk.Label(frame, image=self.photo_ping, text="IDW" , bg="gray" ,  compound ="left", font=("Helvetica", 12, "bold"), anchor="w")
        label_IDW.pack(pady=10, anchor="w")
        self.SQMvalue_IDW = 0  
        self.label_IDW_value = tk.Label(frame, text=str(0), fg="blue", bg="gray"  , font=("Helvetica", 12, "bold"))
        self.label_IDW_value.pack()
        label_OK = tk.Label(frame, image=self.photo_ping, text="OK" , bg="gray" ,  compound ="left", font=("Helvetica", 12, "bold"), anchor="w")
        label_OK.pack(pady=10, anchor="w")
        self.SQMvalue_OK = 0  
        self.label_OK_value = tk.Label(frame, text=str(0), fg="blue", bg="gray"  , font=("Helvetica", 12, "bold"))
        self.label_OK_value.pack()
        label_Shepard = tk.Label(frame, image=self.photo_ping, text="Shepard" , bg="gray" ,  compound ="left", font=("Helvetica", 12, "bold"), anchor="w")
        label_Shepard.pack(pady=10, anchor="w")
        self.SQMvalue_Shepard = 0  
        self.label_Shepard_value = tk.Label(frame, text=str(0), fg="blue", bg="gray"  , font=("Helvetica", 12, "bold"))
        self.label_Shepard_value.pack()
        label_SVR = tk.Label(frame, image=self.photo_ping, text="SVR" , bg="gray" ,  compound ="left", font=("Helvetica", 12, "bold"), anchor="w")
        label_SVR.pack(pady=10, anchor="w")
        self.SQMvalue_SVR = 0  
        self.label_SVR_value = tk.Label(frame, text=str(0), fg="blue" , bg="gray" , font=("Helvetica", 12, "bold"))
        self.label_SVR_value.pack()
        label_NNR = tk.Label(frame, image=self.photo_ping, text="NNR" , bg="gray" ,  compound ="left", font=("Helvetica", 12, "bold"), anchor="w")
        label_NNR.pack(pady=10, anchor="w")
        self.SQMvalue_NNR = 0  
        self.label_NNR_value = tk.Label(frame, text=str(0), fg="blue", bg="gray" , font=("Helvetica", 12, "bold"))
        self.label_NNR_value.pack()
        self.image = Image.open("button_img/remove.png")
        self.photo = ImageTk.PhotoImage(self.image.resize((30,30)))
        button = tk.Button(frame, image=self.photo, width = 150, text="Remove Marker", command=self.clear_marker_event , bg="gray", compound ="left" , font=("Helvetica", 12, "bold"))
        button.pack(side=tk.BOTTOM,pady=10)
        self.image2 = Image.open("button_img/map.png")
        self.photo2 = ImageTk.PhotoImage(self.image2.resize((30,30)))
        SC_button = tk.Button(frame, image=self.photo2, width = 150, text="South Carolina", command=self.change_to_SC , bg="gray" , compound ="left" , font=("Helvetica", 12, "bold"))
        SC_button.pack(side=tk.BOTTOM,pady=10)
        self.image3 = Image.open("button_img/map.png")
        self.photo3 = ImageTk.PhotoImage(self.image3.resize((30,30)))
        FL_button = tk.Button(frame, image=self.photo3, width = 150, text="Florida", command=self.change_to_FL , bg="gray" , compound ="left" , font=("Helvetica", 12, "bold"))
        FL_button.pack(side=tk.BOTTOM,pady=10)
        self.value = 0
        self.box = ttk.Combobox(frame,
                    width=23,
                    values=['Alachua County','Orange County','St.Johns County']) # values=['Alachua County','Orange County','St.Johns County', 'PI_Case'])
        self.box.pack(side=tk.BOTTOM,pady=10)
        default_text = "Choose County"
        self.box.set(default_text) 
        self.box2 = ttk.Combobox(frame,
                    width=23,
                    values=['profile_1','profile_2','profile_3', 'profile_4', 'profile_5', 'N/A', 'delete_marker'])
        self.box2.pack(side=tk.BOTTOM,pady=10)
        default_text = "Choose Light profile"
        self.box2.set(default_text) 
        self.image4 = Image.open("button_img/render.png")
        self.photo4 = ImageTk.PhotoImage(self.image4.resize((30,30)))
        Render_button = tk.Button(frame, image=self.photo4, width = 150, text='Render', command=self.on_render_button_click, bg="gray", compound = "left", font=("Helvetica", 12))
        Render_button.pack(side=tk.BOTTOM,pady=10)
        self.map_widget = TkinterMapView(self.win, width=750, height=600)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_address("Florida", marker=False)
        try:
            with open('maps_files/street_map_last_save.csv', 'r') as f:
                reader = csv.DictReader(f)
                
                # Initialize lists to store data
                coor_point2 = []
                sqm_value2 = []
                C1 = []
                C2 = []
                profile = []
                
                # Read data from CSV and store in lists
                for row in reader:
                    coor_point2.append((float(row['Latitude']), float(row['Longitude'])))
                    sqm_value2.append(int(row['sqm_value2']))
                    C1.append(float(row['C1']))
                    C2.append(float(row['C2']))
                    profile.append(row['profile'])
                
                # Assign data to class variables
                self.coor_point2 = coor_point2
                self.sqm_value2 = sqm_value2
                self.C1 = C1
                self.C2 = C2
                self.profile = profile
                
                # Set markers on map
                for i, coords in enumerate(self.coor_point2):
                    print(coords)
                    marker = self.map_widget.set_marker(coords[0], coords[1], text=str(i)+str(profile[i]))
                    self.marker_list2.append(marker)
        except FileNotFoundError:
            print("no such file")
        # Open the file
        with open('maps_files/converted_coordinates (Alachua).txt', 'r') as file:
            # Read each line in the file
            lines = file.readlines()
        # Create an empty list to store the coordinates
        coordinates = []
        # Iterate over each line of data
        for line in lines:
            # Use the split() function to separate the coordinates in each line
            # Assuming the coordinates are comma-separated and enclosed in parentheses
            # Remove the newline character from each line before splitting
            parts = line.strip().split(',')
            # Extract the coordinates from the split result and convert them to floating-point numbers
            # Get the first coordinate using index 0 and remove the left parenthesis
            latitude = float(parts[0].lstrip('('))
            # Get the second coordinate using index 1, and remove the right parenthesis and any whitespace characters
            longitude = float(parts[1].rstrip(')'))
            # Add the coordinates to the list
            coordinates.append((latitude, longitude))
        polygon_1 = self.map_widget.set_polygon(coordinates,
                                        fill_color=None,
                                        outline_color="red",
                                        border_width=2,
                                        name="Alachua county")
        # Open the file
        with open('maps_files/converted_coordinates (Orange).txt', 'r') as file:
            # Read each line in the file
            lines = file.readlines()
        # Create an empty list to store the coordinates
        coordinates = []
        # Iterate over each line of data
        for line in lines:
            # Use the split() function to separate the coordinates in each line
            # Assuming the coordinates are comma-separated and enclosed in parentheses
            # Remove the newline character from each line before splitting
            parts = line.strip().split(',')

            # Extract the coordinates from the split result and convert them to floating-point numbers
            # Get the first coordinate using index 0 and remove the left parenthesis
            latitude = float(parts[0].lstrip('('))
            
            # Get the second coordinate using index 1, and remove the right parenthesis and any whitespace characters
            longitude = float(parts[1].rstrip(')'))

            # Add the coordinates to the list
            coordinates.append((latitude, longitude))


        polygon_2 = self.map_widget.set_polygon(coordinates,
                                        fill_color=None,
                                        outline_color="red",
                                        border_width=2,
                                        name="Orange county")


        # Open the file
        with open('maps_files/converted_coordinates (St_Johns).txt', 'r') as file:
            # Read each line in the file
            lines = file.readlines()

        # Create an empty list to store the coordinates
        coordinates = []

        # Iterate over each line of data
        for line in lines:
            # Use the split() function to separate the coordinates in each line
            # Assuming the coordinates are comma-separated and enclosed in parentheses
            # Remove the newline character from each line before splitting
            parts = line.strip().split(',')

            # Extract the coordinates from the split result and convert them to floating-point numbers
            # Get the first coordinate using index 0 and remove the left parenthesis
            latitude = float(parts[0].lstrip('('))
            
            # Get the second coordinate using index 1, and remove the right parenthesis and any whitespace characters
            longitude = float(parts[1].rstrip(')'))

            # Add the coordinates to the list
            coordinates.append((latitude, longitude))


        polygon_3 = self.map_widget.set_polygon(coordinates,
                                        fill_color=None,
                                        outline_color="red",
                                        border_width=2,
                                        name="St_Johns")
        

        self.map_widget.add_right_click_menu_command(label="Add light source",
                                                command=self.add_marker_event,
                                                pass_coords=True)


        self.map_widget.add_right_click_menu_command(label="Add light source with attenuation",
                                                command=self.add_marker_event2,
                                                pass_coords=True)

            
        self.map_widget.add_left_click_map_command(self.left_click_event)


        # Create ScrolledText for log
        self.custom_font = font.Font(family="Helvetica", size=15, weight="bold")
        self.log_text = scrolledtext.ScrolledText(self.win, wrap=tk.WORD, width=40, height=10, font=self.custom_font)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log("Current Region: Florida (default)")
        self.log("Try to set point on the map.")

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.win, variable=self.progress_var, orient=tk.HORIZONTAL, length=147, mode='determinate')
        # ttk.Progressbar(self.win, variable=progress_var, length=200, mode='determinate')
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)


        # Create Canvas for drawing
        canvas_frame = tk.Frame(self.win, width=150, height=100 , bg="gray" )
        canvas_frame.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(canvas_frame, width=150, height=200 , bg="gray")
        self.canvas.pack()
        SQM = 16
        Red = 255 - int(((SQM - 16) / (22 - 16)) * 155)
        hex_value = format(Red, 'x').zfill(2)
        color_rgb = "#" + hex_value + "0000"
        self.draw_circle(self.canvas, 75, 75, 50, color_rgb)
        self.canvas.create_text(75, 150, text="LPM Indicator", fill="black", font=("Helvetica", 12, "bold"))

        self.win.geometry("800x800")
        self.win.title("LightViz")
        self.win.resizable(False, False)
        icon = PhotoImage(file="button_img/SQM.png")  # Ensure the file path is correct
        self.win.iconphoto(False, icon)


    def on_render_button_click(self):
        if len(self.coor_point) == 0:
            selected_county = self.box.get()
            selected_county_val = 0
            if selected_county == 'Alachua County':
                selected_county_val = 1
                self.light_field_plot(1)
            elif selected_county == 'Orange County':
                selected_county_val = 2
                self.light_field_plot(2)
            elif selected_county == 'St.Johns County':
                selected_county_val = 3
                self.light_field_plot(3)
            elif selected_county == 'PI_Case':
                selected_county_val = 4
                self.light_field_plot(4)
            elif selected_county == 'County 1':
                selected_county_val = 11
            elif selected_county == 'County 2':
                selected_county_val = 12
            elif selected_county == 'County 3':
                selected_county_val = 13
            else:
                self.log("Select county before rendering!")
                return
            js_file_path = os.path.join(os.getcwd(), 'src/selected_county.js')

            with open(js_file_path, 'w') as js_file:
                js_file.write(f"var selectedCounty = {selected_county_val};\n")
            html_file_path = os.path.join(os.getcwd(), 'src/example_directdraw.html')
            webview.create_window("Light-field Map", html_file_path, frameless=False, width=510, height=510)
            webview.start()
        else:
            self.log("Remove non-attentuation points before rendering!")

    


    def draw_circle(self, canvas, x, y, radius, color):
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)



    def change_to_SC(self):
        self.map_widget.set_address("South Carolina", marker=False)
        self.log("Current Region: South Carolina")
        self.log("Try to set point on the map.")
        self.box['values'] = []  #self.box['values'] = ["County 1", "County 2", "County 3"]

    def change_to_FL(self):
        self.map_widget.set_address("Florida", marker=False)
        self.log("Current Region: Florida")
        self.log("Try to set point on the map.")
        self.box['values'] = ['Alachua County','Orange County','St.Johns County']

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


    def light_field_plot(self, val):

        if (len(self.coor_point) > 0):
            self.log("Rendering only for light source with attenuation")
            return
        if (len(self.coor_point2) > 0):
            self.log("Plotting light pollution map....")  
            lats = [lat for lat, lon in self.coor_point2]
            lons = [lon for lat, lon in self.coor_point2]
            max_lat = max(lats)
            min_lat = min(lats)
            max_lon = max(lons)
            min_lon = min(lons)
            if(val == 1): 
                print("Alachua")
                max_lat = 29.95386
                min_lat = 29.41792
                max_lon = -82.04977
                min_lon = -82.66435
            elif(val ==2):
                print("Orange")
                max_lat = 28.8039593
                min_lat = 28.3420496
                max_lon = -80.8609920
                min_lon = -81.6657405
            elif(val == 3):
                print("St_Johns")
                max_lat = 30.2557993
                min_lat = 29.6203198
                max_lon = -81.1948947
                min_lon = -81.7098789
            elif(val == 4):
                print("PI_case")
                max_lat = 30.0585058
                min_lat = 30.050939
                max_lon = -81.609565
                min_lon = -81.62140
            print("max_lat: " + str(max_lat))
            print("min_lat: " + str(min_lat))
            print("max_lon: " + str(max_lon))
            print("min_lon: " + str(min_lon))
            grid_resolution = 100      # 40, 200, 500, 800
            lat_len = max_lat - min_lat
            lon_len = max_lon - min_lon
            ratio = 0
            grid_lat, grid_lon = np.meshgrid(np.linspace(min_lat - ratio*lat_len, max_lat + ratio*lat_len, grid_resolution),
                                            np.linspace(min_lon - ratio*lon_len, max_lon + ratio*lon_len, grid_resolution))
            grid_lat_flat, grid_lon_flat = grid_lat.flatten(), grid_lon.flatten()
            print("size: " + str(grid_lat_flat.shape))
            self.progress_var.set(0)
            self.progress_bar.start() 
            step = 1
            value_vec = []
            for lat_row, lon_row in zip(grid_lat, grid_lon):
                for lat, lon in zip(lat_row, lon_row):
                    target_coor = [lat, lon]
                    # Convert lan/lon to UTM
                    x_array = []
                    y_array = []
                    for (lat, lon) in self.coor_point2:
                        u = utm.from_latlon(lat, lon)
                        x_array.append(u[0])
                        y_array.append(u[1])
                    u = utm.from_latlon(target_coor[0], target_coor[1])
                    xi = u[0]
                    yi = u[1]
                    numeric_list = [float(x) for x in self.sqm_value2]
                    if len(numeric_list) < 1:
                        print("Number of points isn't enough.")
                        self.log("Number of points isn't enough.")
                        return
                    
                    distances = np.sqrt((np.array(x_array) - xi)**2 + (np.array(y_array) - yi)**2)
                    distances = distances   #1000 (km)
                    self.progress_var.set(step*100/(grid_resolution*grid_resolution))
                    step = step + 1
                    self.win.update_idletasks() 
                    # Filter out points with distance greater than the threshold
                    distance_threshold = 100  # Define your threshold here
                    mask = distances <= distance_threshold
                    if not np.any(mask):
                        # continue  # Skip if no points are within the threshold
                        value_vec.append(22)
                        continue
                    
                    filtered_distances = distances[mask]
                    filtered_sqm_values = np.array(self.sqm_value2)[mask]
                    filtered_C1 = np.array(self.C1)[mask]
                    filtered_C2 = np.array(self.C2)[mask]

                    # In IDW, weights are 1 / distance
                    weights = 1.0/(filtered_distances+1e-12)**2

                    # Make weights sum to one
                    weights /= weights.sum(axis=0)

                    y_values2 = []
                    for i in range(len(filtered_sqm_values)):
                        y_values = 1 / (1.0 + filtered_C1[i]*filtered_distances[i]/10 + filtered_C2[i]*filtered_distances[i]*filtered_distances[i]/100)
                        y_values2.append((22-filtered_sqm_values[i])*(1-y_values) + filtered_sqm_values[i])
                    value = np.dot(weights.T, y_values2)
                    value_vec.append(value)


            print("size: "+ str(len(value_vec)))
            # Combine the data into a list of tuples
            data = list(zip(grid_lat_flat, grid_lon_flat, value_vec))

            # Specify the CSV file path
            csv_file_path = "maps_files/Grid_data.csv"

            # Write to the CSV file
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                
                # Write the header row
                writer.writerow(['Lat', 'Long', 'Value'])
                
                # Write the data rows
                writer.writerows(data)

            print(f"CSV file '{csv_file_path}' has been created.")
            self.progress_var.set(100)
            self.win.update_idletasks() 
            self.progress_bar.stop()
            # self.progress_bar.pack_forget()
            self.log("Open GIS Map shortly...") 
            # GIS_MAP(val)
            self.log("Finish...")  
            # Additional code for reading, filtering, normalizing, and converting to JS
            def read_csv_to_list(csv_filename):
                with open(csv_filename, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader) 
                    data_list = [[float(row[0]), float(row[1]), float(row[2])] for row in reader]
                return data_list

            def filter_data(data_list, filter_value=22, keep_boundary_values=True, keep_percentage=2):
                if keep_boundary_values:
                    filtered_data = [data for data in data_list if data[2] != filter_value or (data[2] == filter_value and (data[0] == min_lat or data[0] == max_lat or data[1] == min_lon or data[1] == max_lon))]
                else:
                    filtered_data = [data for data in data_list if data[2] != filter_value]

                # Filter out 80% of the samples where data[2] == filter_value
                if keep_percentage <= 1:
                    samples_to_keep = [data for data in data_list if data[2] == filter_value]
                    random.shuffle(samples_to_keep)
                    num_to_keep = int(len(samples_to_keep) * keep_percentage)
                    filtered_data.extend(samples_to_keep[:num_to_keep])
                
                return filtered_data

            def normalize_data(data_list, min_value, max_value):
                normalized_list = []
                for data in data_list:
                    normalized_value = 1 - (data[2] - min_value) / (max_value - min_value)
                    normalized_list.append([data[0], data[1], normalized_value])
                return normalized_list

            def convert_to_js(data_list):
                js_content = f"var addressPoints = {json.dumps(data_list, indent=4)};"
                return js_content

            csv_filename = 'maps_files/Grid_data.csv'
            data_list = read_csv_to_list(csv_filename)

            filtered_data = filter_data(data_list, keep_boundary_values=True)

            min_value = min([data[2] for data in filtered_data])
            max_value = max([data[2] for data in filtered_data])

            normalized_data = normalize_data(filtered_data, 16, 22)

            js_content = convert_to_js(normalized_data)

            js_filename = 'src/normalized_filtered_grid_data.js'
            with open(js_filename, 'w', encoding='utf-8') as js_file:
                js_file.write(js_content)

            print(f'Data has been saved to {js_filename}')
        else:
            self.log("Not enought points.")  




    def add_marker_event(self, coords):
        print("Add marker:", coords)   
        self.log("Add marker:" + str(coords))
        self.coor_point.append(coords)
        self.open_input_dialog()
        self.marker_list.append(self.map_widget.set_marker(coords[0], coords[1], text=str(len(self.coor_point))))
        print(self.coor_point)
        print(self.sqm_value)

    def add_marker_event2(self, coords):
        new_window = tk.Toplevel(self.win)
        app = LightAttenuationApp(new_window)
        new_window.wait_window()
        print("SQM " + str(app.SQM_val))
        print("C1 " + str(app.C1))
        print("C2 " + str(app.C2))
        print("Add marker:", coords)   
        self.log("Add marker:" + str(coords))
        self.coor_point2.append(coords)
        # self.open_input_dialog()
        self.sqm_value2.append(app.SQM_val)
        self.C1.append(app.C1)
        self.C2.append(app.C2)
        self.marker_list2.append(self.map_widget.set_marker(coords[0], coords[1], text=str(len(self.coor_point2))))
        print(self.coor_point2)
        print(self.sqm_value2)
        print(self.C1)
        print(self.C2)
        print(self.marker_list2)
        data = {
            "coor_point2": self.coor_point2,
            "sqm_value2": self.sqm_value2,
            "C1": self.C1,
            "C2": self.C2,
            # "marker_list2": self.marker_list2
        }

        fieldnames = ['Latitude', 'Longitude', 'sqm_value2', 'C1', 'C2', 'profile']
        if len(self.coor_point) == 0:
            with open('maps_files/street_map_last_save.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                
                writer.writerow(fieldnames)
                
                for i in range(len(data['coor_point2'])):
                    row = [
                        data['coor_point2'][i][0],  # Latitude
                        data['coor_point2'][i][1],  # Longitude
                        data['sqm_value2'][i],      # sqm_value2
                        data['C1'][i],              # C1
                        data['C2'][i],              # C2
                        "original"                  # profile
                    ]
                    writer.writerow(row)


    def SI_SQM_values_estimate(self, target_coor):
        # Convert lan/lon to UTM
        try:
            x_array = []
            y_array = []
            for (lat, lon) in self.coor_point:
                u = utm.from_latlon(lat, lon)
                x_array.append(u[0])
                y_array.append(u[1])

            u = utm.from_latlon(target_coor[0], target_coor[1])
            xi = u[0]
            yi = u[1]

            numeric_list = [float(x) for x in self.sqm_value]
            if len(numeric_list) < 3:
                raise ValueError("Number of points isn't enough.")

            self.progress_var.set(0)
            self.progress_bar.start()

            self.SQMvalue_IDW = self.simple_idw(x_array, y_array, numeric_list, xi, yi, 2)
            self.progress_var.set(20)
            self.win.update_idletasks()
            self.log("IDW done.")

            self.SQMvalue_OK = self.OKrigin(x_array, y_array, numeric_list, xi, yi)
            self.progress_var.set(40)
            self.win.update_idletasks()
            self.log("OK done.")

            self.SQMvalue_Shepard = self.shepard_interpolation(x_array, y_array, numeric_list, xi, yi, 2)
            self.progress_var.set(60)
            self.win.update_idletasks()
            self.log("Shepard done.")       

            self.SQMvalue_SVR = self.SVR(x_array, y_array, numeric_list, xi, yi)
            self.progress_var.set(80)
            self.win.update_idletasks()  
            self.log("SVR done.")       

            self.SQMvalue_NNR = self.NNR(x_array, y_array, numeric_list, xi, yi)
            self.progress_var.set(100)
            self.win.update_idletasks()
            self.log("NNR done.") 
            self.log("-------------------") 

            self.label_IDW_value.config(text=str(float(self.SQMvalue_IDW[0])))
            self.label_OK_value.config(text=str(float(self.SQMvalue_OK)))
            self.label_Shepard_value.config(text=str(float(self.SQMvalue_Shepard)))        
            self.label_SVR_value.config(text=str(float(self.SQMvalue_SVR[0])))   
            self.label_NNR_value.config(text=str(float(self.SQMvalue_NNR[0][0])))   

            self.progress_bar.stop()

        except ValueError as ve:
            print(f"ValueError: {ve}")
            self.log(f"ValueError: {ve}")
            self.progress_bar.stop()
            self.log("Each lower bound must be strictly less than each upper bound. Try restart the app!")


    def SI_SQM_values_estimate2(self, target_coor):
        # Convert lan/lon to UTM
        x_array = []
        y_array = []
        for (lat, lon) in self.coor_point2:
            u = utm.from_latlon(lat, lon)
            x_array.append(u[0])
            y_array.append(u[1])
        u = utm.from_latlon(target_coor[0], target_coor[1])
        xi = u[0]
        yi = u[1]
        numeric_list = [float(x) for x in self.sqm_value2]
        if len(numeric_list) < 1:
            print("Number of points isn't enough.")
            self.log("Number of points isn't enough.")
            return
        
        distances = np.sqrt((np.array(x_array) - xi)**2 + (np.array(y_array) - yi)**2)
        distances = distances
        # print("distances: " + str(distances))

        # In IDW, weights are 1 / distance
        weights = 1.0/(distances+1e-12)**2

        # Make weights sum to one
        weights /= weights.sum(axis=0)

        # # Create a progress bar
        # progress_var = tk.IntVar()
        # progress_bar = ttk.Progressbar(self.win, variable=progress_var, length=200, mode='determinate')
        # progress_bar.pack(pady=10)

        self.progress_var.set(0)
        self.progress_bar.start()
        y_values2 = []
        for i in range(len(self.sqm_value2)):
            y_values = 1 / (1.0 + self.C1[i]*distances[i]/10 + self.C2[i]*distances[i]*distances[i]/100)
            y_values2.append((22-self.sqm_value2[i])*(1-y_values) + self.sqm_value2[i])
            self.progress_var.set(i*100/len(self.sqm_value2))
            self.win.update_idletasks()  

        value = np.dot(weights.T, y_values2)
        print(value)
        self.log("Estimated value: " + str(value))

        SQM = value
        Red = 255 - int((  (SQM-16) / (22-16) )*155)
        hex_value = format(Red, 'x')
        color_rgb = "#"+ str(hex_value) + "0000"
        print(color_rgb)
        # color_rgb = "#800000"
        self.draw_circle(self.canvas, 75, 75, 50, color_rgb)
        self.progress_bar.stop()
        # self.progress_bar.pack_forget()


    def left_click_setup_light_source(self, coords, val):
        # self.open_input_dialog() 
        if val == 1:   # profile 1
            sqm = 16
            c1 = 0
            c2 = 0.03
            L_profile = "profile_1"
        elif val == 2:
            sqm = 16
            c1 = 0.03
            c2 = 0.03
            L_profile = "profile_2"
        elif val == 3:
            sqm = 16
            c1 = 0.06
            c2 = 0.03   
            L_profile = "profile_3"    
        elif val == 4:
            sqm = 16
            c1 = 0.1
            c2 = 0.03   
            L_profile = "profile_4"   
        elif val == 5:
            sqm = 16
            c1 = 0.9
            c2 = 0.6   
            L_profile = "profile_5"   
        elif val == 0:
        # Convert lan/lon to UTM
            x_array = []
            y_array = []
            for (lat, lon) in self.coor_point2:
                u = utm.from_latlon(lat, lon)
                x_array.append(u[0])
                y_array.append(u[1])
            u = utm.from_latlon(coords[0], coords[1])
            xi = u[0]
            yi = u[1]
            numeric_list = [float(x) for x in self.sqm_value2]
            if len(numeric_list) < 1:
                print("Number of points isn't enough.")
                self.log("Number of points isn't enough.")
                return
            
            distances = np.sqrt((np.array(x_array) - xi)**2 + (np.array(y_array) - yi)**2)
            distances = distances

            min_index = np.argmin(distances)
            print(min_index)

            self.coor_point2.pop(min_index)
            self.sqm_value2.pop(min_index)
            self.C1.pop(min_index)
            self.C2.pop(min_index)
            last_marker2 = self.marker_list2[min_index]  
            last_marker2.delete()  
            self.marker_list2.pop(min_index)
            self.profile.pop(min_index)

            data = {
                "coor_point2": self.coor_point2,
                "sqm_value2": self.sqm_value2,
                "C1": self.C1,
                "C2": self.C2,
                "profile": self.profile
                # "marker_list2": self.marker_list2
            }

            fieldnames = ['Latitude', 'Longitude', 'sqm_value2', 'C1', 'C2', 'profile']
            if len(self.coor_point) == 0:
                with open('maps_files/street_map_last_save.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    
                    writer.writerow(fieldnames)
                    
                    for i in range(len(data['coor_point2'])):
                        row = [
                            data['coor_point2'][i][0],  # Latitude
                            data['coor_point2'][i][1],  # Longitude
                            data['sqm_value2'][i],      # sqm_value2
                            data['C1'][i],              # C1
                            data['C2'][i],              # C2
                            data['profile'][i]          # profile
                        ]
                        writer.writerow(row)
                return



        self.coor_point2.append(coords)
        self.sqm_value2.append(sqm)
        self.C1.append(c1)
        self.C2.append(c2)
        self.marker_list2.append(self.map_widget.set_marker(coords[0], coords[1], text=str(len(self.coor_point2) - 1) + str(L_profile)))
        self.profile.append(L_profile)
        data = {
            "coor_point2": self.coor_point2,
            "sqm_value2": self.sqm_value2,
            "C1": self.C1,
            "C2": self.C2,
            "profile": self.profile
            # "marker_list2": self.marker_list2
        }

        fieldnames = ['Latitude', 'Longitude', 'sqm_value2', 'C1', 'C2', 'profile']
        if len(self.coor_point) == 0:
            with open('maps_files/street_map_last_save.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                
                writer.writerow(fieldnames)
                
                for i in range(len(data['coor_point2'])):
                    row = [
                        data['coor_point2'][i][0],  # Latitude
                        data['coor_point2'][i][1],  # Longitude
                        data['sqm_value2'][i],      # sqm_value2
                        data['C1'][i],              # C1
                        data['C2'][i],              # C2
                        data['profile'][i]          # profile
                    ]
                    writer.writerow(row)



    def left_click_event(self,coordinates_tuple):
        print("Left click event with coordinates:", coordinates_tuple)
        # ['profile_1','profile_2','profile_3', 'profile_4', 'profile_5', 'N/A', 'delete_marker']
        selected_light_profile = self.box2.get()
        if selected_light_profile == 'profile_1':
            self.left_click_setup_light_source(coords = coordinates_tuple, val = 1)
            return
        elif selected_light_profile == 'profile_2':
            self.left_click_setup_light_source(coords = coordinates_tuple, val = 2)
            return
        elif selected_light_profile == 'profile_3':
            self.left_click_setup_light_source(coords = coordinates_tuple, val = 3)
            return
        elif selected_light_profile == 'profile_4':
            self.left_click_setup_light_source(coords = coordinates_tuple, val = 4)
            return
        elif selected_light_profile == 'profile_5':
            self.left_click_setup_light_source(coords = coordinates_tuple, val = 5)
            return
        elif selected_light_profile == 'delete_marker':
            self.left_click_setup_light_source(coords = coordinates_tuple, val = 0)
            return



        if (len(self.coor_point) > 0) and (len(self.coor_point2) > 0):
            print("Error: don't mix non atten with atten.")
            self.log("Error: don't mix non atten with atten.")
        elif (len(self.coor_point) > 0) and (len(self.coor_point2) == 0):
            # Non attenuation 
            print("Non Attenuation")
            self.log("Non Attenuation")
            self.SI_SQM_values_estimate(coordinates_tuple)
        elif (len(self.coor_point) == 0) and (len(self.coor_point2) > 0):
            # Attenuation
            print("Attenuation")
            self.log("Attenuation")
            self.SI_SQM_values_estimate2(coordinates_tuple)
        else:
            print("Error: No point.")
            self.log("Error: No point.")
        print(self.coor_point)
        print(self.sqm_value)
        print(self.coor_point2)
        print(self.sqm_value2)
        print(self.C1)
        print(self.C2)


    def clear_marker_event(self):
        try:
            if (len(self.coor_point) > 0) and (len(self.coor_point2) > 0):
                last_marker = self.marker_list[-1]  
                last_marker.delete()  
                self.marker_list.pop()  
                self.coor_point = self.coor_point[:-1]
                self.sqm_value = self.sqm_value[:-1]
                last_marker2 = self.marker_list2[-1]  
                last_marker2.delete()  
                self.marker_list2.pop()  
                self.coor_point2 = self.coor_point2[:-1]
                self.sqm_value2 = self.sqm_value2[:-1]
                self.C1 = self.C1[:-1]
                self.C2 = self.C2[:-1]
                self.profile = self.profile[:-1]
            elif len(self.coor_point) > 0:
                last_marker = self.marker_list[-1]  
                last_marker.delete()  
                self.marker_list.pop()  
                self.coor_point = self.coor_point[:-1]
                self.sqm_value = self.sqm_value[:-1]
            elif len(self.coor_point2) > 0:
                last_marker2 = self.marker_list2[-1]  
                last_marker2.delete()  
                self.marker_list2.pop()  
                self.coor_point2 = self.coor_point2[:-1]
                self.sqm_value2 = self.sqm_value2[:-1]
                self.C1 = self.C1[:-1]
                self.C2 = self.C2[:-1]
                self.profile = self.profile[:-1]

            data = {
                "coor_point2": self.coor_point2,
                "sqm_value2": self.sqm_value2,
                "C1": self.C1,
                "C2": self.C2,
                "profile": self.profile
                # "marker_list2": self.marker_list2
            }

            fieldnames = ['Latitude', 'Longitude', 'sqm_value2', 'C1', 'C2', 'profile']
            if len(self.coor_point) == 0:
                with open('maps_files/street_map_last_save.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    
                    writer.writerow(fieldnames)
                    
                    for i in range(len(data['coor_point2'])):
                        row = [
                            data['coor_point2'][i][0],  # Latitude
                            data['coor_point2'][i][1],  # Longitude
                            data['sqm_value2'][i],      # sqm_value2
                            data['C1'][i],              # C1
                            data['C2'][i],              # C2
                            data['profile'][i]          # profile
                        ]
                        writer.writerow(row)
        except Exception as e:
            print("An error occurred while deleting the last marker:", e)
        print(self.coor_point)
        print(self.sqm_value)
        print(self.coor_point2)
        print(self.sqm_value2)
        print(self.C1)
        print(self.C2)

    def open_input_dialog(self):
        value = simpledialog.askstring("Input", "Enter a value:")
        self.sqm_value.append(value)
        if value is not None:
            print("Entered value:", value)
        else:
            print("No value entered.")
            last_marker = self.marker_list[-1]  
            last_marker.delete()  
            self.marker_list.pop()  
            self.coor_point = self.coor_point[:-1]
            self.sqm_value = self.sqm_value[:-1]

    def start(self):
        self.win.mainloop()



## Interpolation methods

    def distance_matrix(self, x0, y0, x1, y1):
        """ Make a distance matrix between pairwise observations.
        Note: from <http://stackoverflow.com/questions/1871536> 
        """
        
        obs = np.vstack((x0, y0)).T
        interp = np.vstack((x1, y1)).T

        d0 = np.subtract.outer(obs[:,0], interp[:,0])
        d1 = np.subtract.outer(obs[:,1], interp[:,1])
        
        # calculate hypotenuse
        return np.hypot(d0, d1)


    def simple_idw(self, x, y, z, xi, yi, power=1):
        dist = self.distance_matrix(x,y, xi,yi)

        # In IDW, weights are 1 / distance
        weights = 1.0/(dist+1e-12)**power

        # Make weights sum to one
        weights /= weights.sum(axis=0)
        # Multiply the weights for each interpolated point by all observed Z-values
        return np.dot(weights.T, z)

    def OKrigin(self, x, y, z, xi, yi):
        OK = OrdinaryKriging(
                x, 
                y, 
                z, 
                variogram_model='gaussian',
                verbose=False,
                enable_plotting=False,
                nlags=6)
        # OK.variogram_model_parameters
        zstar, ss = OK.execute("grid", xi, yi)
        return zstar

    def shepard_interpolation(self, x, y, z, x_target, y_target, power=2):
        distances = np.sqrt((x - x_target)**2 + (y - y_target)**2)
        distances[distances == 0] = 1e-10
        weights = 1 / distances**power
        weights /= np.sum(weights)
        z_target = np.sum(weights * z)
        return z_target
    
    def SVR(self, x, y, z, xi, yi):
        # Separate features (predictors) and target variable
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        X = np.column_stack((x, y))  
        y = z  

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Feature scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create and train the SVR model
        svr = SVR(kernel='rbf')  # You can adjust other parameters such as C, gamma, etc.
        svr.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        # y_pred = svr.predict(X_test_scaled)

        # # Calculate mean squared error
        # mse = mean_squared_error(y_test, y_pred)
        # print("Mean Squared Error:", mse)

        point_scaled = scaler.transform(np.column_stack((xi, yi)))
        predicted_values = svr.predict(point_scaled)

        return predicted_values

    def NNR(self, x, y, z, xi, yi):
        # Separate features (predictors) and target variable
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        X = np.column_stack((x, y))  
        y = z  

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Feature scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Define the neural network model
        model = Sequential([
            Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(1)  # Output layer
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=1)

        # # Make predictions on the test set
        # y_pred = model.predict(X_test_scaled).flatten()

        # Calculate mean squared error
        # mse = mean_squared_error(y_test, y_pred)
        # print("Mean Squared Error:", mse)

        point_scaled = scaler.transform(np.column_stack((xi, yi)))
        predicted_values = model.predict(point_scaled)

        return predicted_values


if __name__=="__main__":
    app = App()
    app.start()

