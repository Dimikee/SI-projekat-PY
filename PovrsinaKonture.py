import tkinter as tk
from shapely.geometry import Polygon

class ContourAreaCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Contour Area Calculator")
        self.master.geometry("400x400")

        self.canvas = tk.Canvas(self.master, bg="white", width=300, height=300)
        self.canvas.pack()

        self.undo_button = tk.Button(self.master, text="Undo", command=self.undo_last_point)
        self.undo_button.pack()

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        self.points = []
        self.lines = []
        self.area_label = tk.Label(self.master, text="Area: 0", font=("Arial", 12))
        self.area_label.pack()

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))

        if len(self.points) > 1:
            x0, y0 = self.points[-2]
            x1, y1 = self.points[-1]
            line = self.canvas.create_line(x0, y0, x1, y1)
            self.lines.append(line)

        if len(self.points) >= 3 and self.is_closed_contour():
            self.calculate_area()

    def is_closed_contour(self):
        return len(self.points) >= 3 and self.points[0] == self.points[-1]

    def calculate_area(self):
        if not self.is_closed_contour():
            self.area_label.config(text="Contour is not closed!")
            return

        polygon = Polygon(self.points)
        area = polygon.area
        self.area_label.config(text="Area: {:.2f}".format(area))

    def undo_last_point(self):
        if self.points:
            self.points.pop()
            if self.lines:
                self.canvas.delete(self.lines.pop())
            self.area_label.config(text="Area: 0" if not self.is_closed_contour() else "Calculating...")
            if len(self.points) >= 3 and self.is_closed_contour():
                self.calculate_area()
            else:
                self.area_label.config(text="Area: 0")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.lines = []
        self.area_label.config(text="Area: 0")

def main():
    root = tk.Tk()
    app = ContourAreaCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
