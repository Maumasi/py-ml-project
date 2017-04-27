import matplotlib.pyplot as plt

class lab_chart(object):
    """docstring for lab_chart."""
    def __init__(self):
        super(lab_chart, self).__init__()

    def add_line(self, data, color = 'green', label = 'Pridicted'):
        # plot a line
        plt.plot(
            data,
            color = color,
            label = label
        )

    def render(self, title = 'Predictions', xlabel = 'Time', ylabel = 'Price'):
        # pretty up chart
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()
