import matplotlib.pyplot as plt

metrics=[
    {"name":"Accuracy", "unit":"(%)", "data": [65.67,66.12,69.1,86.01]},
    {"name":"Recall", "unit":"(%)", "data": [53.44,57.25,66.77,75.98]},
    {"name":"Precision", "unit":"(%)", "data": [46.29,57.55,72.94,77]},
    {"name":"F1", "unit":"", "data": [0.46,0.49,0.63,0.76]},
    {"name":"MCC", "unit":"", "data": [0.37,0.41,0.51,0.63]}
    ]

# Sample data
x = [400, 800, 1200, 1600]

for metric in metrics:
    # Plotting the lines
    plt.plot(x, metric["data"], 'o-', label=metric["name"])

    # Legend, axis labels, and title
    plt.legend()
    plt.xlabel('Training sample count')
    plt.ylabel(f'{metric["name"]} {metric["unit"]}')
    plt.title(f'{metric["name"]} vs Training sample count')

    # Displaying the plot
    plt.savefig(f'plots/{metric["name"]}-line-plot.pdf', dpi=300, bbox_inches='tight')
    plt.clf()

