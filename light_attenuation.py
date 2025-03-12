import numpy as np
import matplotlib
import tkinter as Tk
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LightAttenuationApp:
    # Initialize SQM value and coefficients
    SQM_val = 16
    C1 = 0.03
    C2 = 0.154
    def __init__(self, master):
        self.master = master
        self.master.wm_title("Light Attenuation (1: brightness; 0: Darkness)")
        
        # Create a figure
        self.fig = plt.Figure(figsize=(8, 6)) 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        # Create the first axes for the light attenuation plot
        self.ax1 = self.fig.add_axes([0.05, 0.5, 0.4, 0.4])
        self.plot_attenuation_curve()
        
        # Create sliders
        self.create_sliders()
        
        # Create the second axes for plotting the SQM function
        self.ax2 = self.fig.add_axes([0.58, 0.5, 0.4, 0.4])
        self.plot_sqm_curve()
        
        # Add a button to open the input window
        self.button_open_input = Tk.Button(master=self.master, text="Open Input Window (SQM)", command=self.open_input_window)
        self.button_open_input.pack(side=Tk.BOTTOM)
        
        # Add a button to close the window
        self.button_close = Tk.Button(master=self.master, text="Confirm and close", command=self.close_window)
        self.button_close.pack(side=Tk.BOTTOM)
        
    def plot_attenuation_curve(self):
        x_values = np.arange(0, 200, 0.1)
        y_values = 1 / (1.0 + self.C1*x_values/10 + self.C2*x_values*x_values/100)
        
        self.ax1.axis([0, 200, 0, 1])
        (self.l1,) = self.ax1.plot(x_values, y_values, color='red', linewidth=3)
        self.ax1.set_xlabel('Distance (m)')
        self.ax1.set_title("Attenuation curve")
        
    def create_sliders(self):
        # Adjust the position of the first slider
        self.ax1_value = self.fig.add_axes([0.3, 0.35, 0.4, 0.03])
        self.s_time = Slider(self.ax1_value, 'C1 (wavelength-based)', 0, 10.0, valinit=0.65)   # 4.0
        
        # Adjust the position of the second slider
        self.ax2_value = self.fig.add_axes([0.3, 0.3, 0.4, 0.03])
        self.s_time2 = Slider(self.ax2_value, 'C2 (wavelength-based)', 0, 10.0, valinit=0.03)  # 4.0
        
        self.s_time.on_changed(self.update)
        self.s_time2.on_changed(self.update)
        
    def plot_sqm_curve(self):
        x_values = np.arange(0, 200, 0.1)
        y_values = 1 / (1.0 + self.C1*x_values/10 + self.C2*x_values*x_values/100)
        y_values2 = (22-self.SQM_val)*(1-y_values) + self.SQM_val
        
        (self.l2,) = self.ax2.plot(x_values, y_values2 , color='green', linewidth=3)
        self.ax2.axis([0, 200, 14, 22])
        self.ax2.set_xlabel('Distance (m)')
        self.ax2.set_ylabel('SQM value (mag/arcsec2)')
        self.ax2.set_title("Corresponding SQM curve")
        
    def update(self, val):
        pos = self.s_time.val
        pos2 = self.s_time2.val
        x_values = np.arange(0, 200, 0.1)
        self.C1 = pos
        self.C2 = pos2
        temp_val = 1 / (1.0 + pos * x_values/10 + pos2 * x_values * x_values/100)

        self.l1.set_ydata(temp_val)
        self.l2.set_ydata((22-self.SQM_val)*(1-temp_val) + self.SQM_val)
        self.fig.canvas.draw_idle()
        
    def open_input_window(self):
        input_window = Tk.Toplevel()
        input_window.wm_title("Input SQM Value")
        
        self.entry_SQM = Tk.Entry(input_window)
        self.entry_SQM.insert(0, str(self.SQM_val))
        self.entry_SQM.pack()
        
        button_update = Tk.Button(input_window, text="Update", command=self.update_SQM)
        button_update.pack()
        
    def update_SQM(self):
        self.SQM_val = float(self.entry_SQM.get())
        self.update(None)
        
    def close_window(self):
        self.master.destroy()

if __name__ == "__main__":
    root = Tk.Tk()
    app = LightAttenuationApp(root)
    root.mainloop()
