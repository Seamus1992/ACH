import matplotlib.pyplot as plt
import numpy as np

# Assuming a standard football field size
field_length = 100
field_width = 100

# Create a grid of points within the field
x = np.linspace(0, field_length, 100)
y = np.linspace(0, field_width, 100)
X, Y = np.meshgrid(x, y)

# Initialize a figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

# Define the conditions
conditions = [
    (X <= 30) & ((Y <= 19) | (Y >= 81)),
    (X <= 30) & ((Y >= 19) & (Y <= 81)),
    ((X >= 30) & (X <= 50)) & ((Y <= 15) | (Y >= 84)),
    ((X >= 30) & (X <= 50)) & ((Y >= 15) & (Y <= 84)),
    ((X >= 50) & (X <= 70)) & ((Y <= 15) | (Y >= 84)),
    ((X >= 50) & (X <= 70)) & ((Y >= 15) & (Y <= 84)),
    ((X >= 70) & ((Y <= 15) | (Y >= 84))),
    (((X >= 70) & (X <= 84)) & ((Y >= 15) & (Y <= 84))),
    ((X >= 84) & ((Y >= 15) & (Y <= 37)) | (((X >= 84) & (Y <= 84) & (Y >= 63)))),
    ((X >= 84) & ((Y >= 37) & (Y <= 63)))
]

# Define corresponding zone values
zone_labels = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'Zone 7', 'Zone 8', 'Zone 9', 'Zone 10']

# Plot the football field and label zones
for i, condition in enumerate(conditions):
    ax.contour(X, Y, condition, colors='black', linewidths=2)
    
    # Calculate the center of mass for each zone
    zone_center_x = np.sum(X[condition]) / np.sum(condition)
    zone_center_y = np.sum(Y[condition]) / np.sum(condition)
    

# Set axis labels and title

# Show the plot
plt.grid(True)
plt.show()

