import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import normalize

sample_size_data = [
    {"size": 400, "matrix":np.array([[98.7,  0.4, 34.9],
                             [19.7,  0. ,  3.3],
                             [2.8,  0. , 18.2]])},

    {"size": 800, "matrix":np.array([[96.7,  1.3, 36.],
                             [17.2,  1. ,  4.8],
                             [0.8,  0.2, 20. ]])},

    {"size": 1200, "matrix":np.array([[94.8,  4.5, 34.7],
                             [10.9, 11.4,  0.7],
                             [3.1,  1.1, 16.8]])},

    {"size": 1600, "matrix":np.array([[124.5, 6.3, 3.2],
                             [8.7,  14.1,   0.2],
                             [5.1,   1.1,  14.8]])}
]

for sample_size in sample_size_data:
    # Create a figure and axes
    fig, ax = plt.subplots()
    normalized_matrix = normalize(sample_size["matrix"], axis=1, norm='l1')
    # Create heatmap using seaborn
    sns.heatmap(normalized_matrix, annot=True, cmap='Blues', fmt='f', cbar=True, ax=ax)

    # Set labels, title, and ticks
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(f'Normalized Confusion Matrix (N={sample_size["size"]})')
    ax.xaxis.set_ticklabels(['Class 0', 'Class 1', 'Class 2'])
    ax.yaxis.set_ticklabels(['Class 0', 'Class 1', 'Class 2'])

    plt.savefig(f'plots/n{sample_size["size"]}-confusion-matrix.pdf', dpi=300, bbox_inches='tight')
    plt.clf()

