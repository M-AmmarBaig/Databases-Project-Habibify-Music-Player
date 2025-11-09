import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RevenueGraph(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Revenue Graph Example")
        self.setGeometry(200, 200, 800, 600)

        # --------------- Mock "Database" Data ---------------
        # Format: [ [month, revenue], [month, revenue], ... ]
        self.data = [
            ["January", 12000],
            ["February", 18000],
            ["March", 15000],
            ["April", 22000],
            ["May", 19000],
            ["June", 25000],
        ]

        # --------------- Set up central widget ---------------
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # --------------- Create and add the graph ---------------
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot(111)
        self.setCentralWidget(central_widget)

        # Plot the data
        self.plot_graph()

    def plot_graph(self):
        months = [row[0] for row in self.data]
        revenues = [row[1] for row in self.data]

        self.ax.clear()
        self.ax.plot(months, revenues, marker='o', linestyle='-', linewidth=2)
        self.ax.set_title("Revenue per Month", fontsize=14)
        self.ax.set_xlabel("Month")
        self.ax.set_ylabel("Revenue ($)")
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RevenueGraph()
    window.show()
    sys.exit(app.exec_())
