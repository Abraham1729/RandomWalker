import plotly.express as px
import numpy as np
import time
# Sample data
data_start = time.time()
data = {
    'x': [np.random.rand() for _ in range(1000000)],
    'y': [np.random.rand() for _ in range(1000000)],
}
data_end = time.time()
print(f"DATA:\t{data_end - data_start}")

# Create a scatterplot using Plotly Express
plot_start = time.time()
fig = px.scatter(data, x='x', y='y', title='Scatterplot Example', labels={'x': 'X-axis', 'y': 'Y-axis'})

# Customize the layout (optional)
fig.update_layout(
    showlegend=False,  # Disable the legend
    xaxis_title="X-axis",
    yaxis_title="Y-axis",
)
plot_middle = time.time()
# Show the plot
fig.show()
plot_end = time.time()

print(f"Scattering:\t{plot_middle - plot_start:.4f}")
print(f"Showing:\t{plot_end-plot_middle:.4f}")