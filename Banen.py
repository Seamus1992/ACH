import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sample DataFrame (replace this with your actual DataFrame)
df = pd.DataFrame({
    'location.x': np.random.uniform(0, 100, 100),
    'location.y': np.random.uniform(0, 100, 100)
})

# Define conditions
conditions = [
    (df['location.x'] <= 30) & ((df['location.y'] <= 19) | (df['location.y'] >= 81)),
    (df['location.x'] <= 30) & ((df['location.y'] >= 19) & (df['location.y'] <= 81)),
    ((df['location.x'] >= 30) & (df['location.x'] <= 50)) & ((df['location.y'] <= 15) | (df['location.y'] >= 84)),
    ((df['location.x'] >= 30) & (df['location.x'] <= 50)) & ((df['location.y'] >= 15) & (df['location.y'] <= 84)),
    ((df['location.x'] >= 50) & (df['location.x'] <= 70)) & ((df['location.y'] <= 15) | (df['location.y'] >= 84)),
    ((df['location.x'] >= 50) & (df['location.x'] <= 70)) & ((df['location.y'] >= 15) & (df['location.y'] <= 84)),
    ((df['location.x'] >= 70) & ((df['location.y'] <= 15) | (df['location.y'] >= 84))),
    (((df['location.x'] >= 70) & (df['location.x'] <= 84)) & ((df['location.y'] >= 15) & (df['location.y'] <= 84))),
    ((df['location.x'] >= 84) & ((df['location.y'] >= 15) & (df['location.y'] <= 37)) | ((df['location.x'] >= 84) & (df['location.y'] <= 84) & (df['location.y'] >= 63))),
    ((df['location.x'] >= 84) & ((df['location.y'] >= 37) & (df['location.y'] <= 63)))
]

# Plot the zones on a white background
plt.figure(figsize=(8, 8))

for i, condition in enumerate(conditions):
    plt.scatter(df['location.x'][condition], df['location.y'][condition], label=f'Zone {i + 1}')

plt.xlabel('Location X')
plt.ylabel('Location Y')
plt.title('Zones on White Background')
plt.legend()
plt.grid(True)
plt.show()
