import matplotlib.pyplot as plt
import numpy as np

# Test if 6-chart layout works
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle("Test Dashboard - 6 Charts", fontsize=20, fontweight='bold')

# Flatten axes for easier indexing
axes = axes.flatten()

# Create 6 simple test charts
for i in range(6):
    ax = axes[i]
    x = np.linspace(0, 10, 100)
    y = np.sin(x + i)
    ax.plot(x, y)
    ax.set_title(f'Chart {i+1}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Data/test_6_charts.png', dpi=300, bbox_inches='tight')
plt.close()

print("Test chart saved to Data/test_6_charts.png")
print("Check if you can see all 6 charts in this test file!")