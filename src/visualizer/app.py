import matplotlib
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from visualization import Visualizer


# matplotlib.use("TkAgg")


class App(tk.Tk):
    def __init__(self, visualization: Visualizer):
        super().__init__()
        self.title("ROSA")
        self.style = ttk.Style(self)
        self.minsize(750, 600)
        self.frame1 = tk.Frame(self)

        self.frame_interval = 0.025

        self.visualize = visualization
        self.figure_canvas = FigureCanvasTkAgg(self.visualize.figure, self)
        self.figure_canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self, pack_toolbar=False)
        self.toolbar.update()

        columns = ("ID", "Position")
        self.obj_treeview = ttk.Treeview(self, height=20, columns=columns)
        self.obj_treeview.heading("ID", text="ID")
        self.obj_treeview.heading("Position", text="Position")
        self.obj_treeview.column("#0", minwidth=30, width=30, stretch=tk.NO)
        self.obj_treeview.column("ID", minwidth=100, width=100, stretch=False)
        self.obj_treeview.column("Position", minwidth=150, width=150, stretch=False)
        for obj in self.visualize.data["shapes"]:
            if obj not in self.visualize.data["owners"]:
                self.obj_treeview.insert("", tk.END, values=(obj, ""), iid=obj)
        for obj in self.visualize.data["owners"]:
            self.obj_treeview.insert(self.visualize.data["owners"][obj], tk.END, values=(obj, ""), iid=obj)

        self.slider = ttk.Scale(self.frame1, from_=0, to=len(self.visualize.data) - 3, length=400
                                , orient=tk.HORIZONTAL, command=self.__update_figure)

        self.button_quit = ttk.Button(self, text="Quit", width=20, command=self.quit)

        self.button_addition = ttk.Button(self.frame1, text="+", width=3, command=self.__add_one_frame)
        self.button_subtraction = ttk.Button(self.frame1, text="-", width=3, command=self.__subtract_one_frame)

        self.time_input = ttk.Entry(self.frame1)
        self.button_enter = ttk.Button(self.frame1, text="Enter", command=self.__time_entered)
        self.label_massage = ttk.Label(self, text="", foreground="red", width=70, font=18)

        self.__geometry_widgets()
        self.mainloop()

    def __update_figure(self, slider_index):
        """update data and figure by slider time"""
        time_index = format(round(float(slider_index)), ".0f")
        self.visualize.animate(int(time_index))
        self.figure_canvas.draw()
        time = round(float(time_index) * self.frame_interval, 3)
        self.label_massage.config(text=f"Time :{time}", foreground="green")
        self.time_input.delete(0, tk.END)
        self.__update_position(time)

    def __add_one_frame(self):
        """add one frame in figure and update figure"""
        slider_index = self.slider.get()
        new_index = (float(slider_index) + 1.0)
        self.slider.set(str(new_index))
        self.label_massage.config(text=f"Time :{round(round(new_index) * self.frame_interval, 3)}"
                                  , foreground="green")
        self.time_input.delete(0, tk.END)

        if (slider_index + 1) > (len(self.visualize.data) - 3):
            top_time = round(float(len(self.visualize.data) - 3) * self.frame_interval, 3)
            self.label_massage.config(text=f"Error!.The time is outside the defined range(top range is {top_time} !)"
                                      , foreground="red")

    def __subtract_one_frame(self):
        """subtract one frame in figure and update figure"""
        slider_index = self.slider.get()
        new_index = (float(slider_index) - 1.0)
        self.slider.set(str(slider_index - 1.0))
        self.label_massage.config(text=f"Time :{round(round(new_index) * self.frame_interval, 3)}"
                                  , foreground="green")
        self.time_input.delete(0, tk.END)

        if (slider_index - 1) < 0:
            self.label_massage.config(text="Error!.The time is outside the defined range(less range is 0 !)"
                                      , foreground="red")

    def __time_entered(self):
        """update data and figure by time input"""
        try:
            time_input = float(self.time_input.get())
            index = time_input / self.frame_interval
            if 0 <= float(index) <= (len(self.visualize.data) - 3):
                self.slider.set(index)
                self.label_massage.config(text=f"Time :{round(round(index) * self.frame_interval, 3)}"
                                          , foreground="green")
                self.time_input.delete(0, tk.END)
            else:
                top_time = round(float(len(self.visualize.data) - 3) * self.frame_interval, 3)
                self.label_massage.config(text=f"Error!.The time is outside the defined range(less range is 0, and "
                                               f"top range is {top_time}!)"
                                          , foreground="red")
        except:
            self.label_massage.config(text="Error!.Please inter the right time", foreground="red")

    def __update_position(self, ind):
        """update and set info. of object's position in Treeview"""
        ind = format(ind, ".3f")
        for obj in self.visualize.data["shapes"]:
            position = list()
            for i in self.visualize.data[ind][obj]:
                position.append(round(i, 2))
            self.obj_treeview.item(obj, values=(obj, f"{position}"))

    def __geometry_widgets(self) -> None:
        """grid the widget by using pack and grid"""
        self.label_massage.pack(side=tk.TOP, fill=tk.X)
        self.button_quit.pack(side=tk.BOTTOM, pady=15)
        self.frame1.pack(side=tk.BOTTOM)
        self.time_input.grid(row=0, column=4)
        self.button_enter.grid(row=1, column=4, pady=10)
        self.slider.grid(row=0, column=1)
        self.button_addition.grid(row=0, column=2, padx=15)
        self.button_subtraction.grid(row=0, column=0, padx=15)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.obj_treeview.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
