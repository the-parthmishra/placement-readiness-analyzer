import matplotlib
matplotlib.use('Agg')   # Important: use non-interactive backend (no GUI popup)
import matplotlib.pyplot as plt

def generate_chart(scores):
    categories = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(6, 4))          # Fixed size — prevents overflow on page
    colors = ['#4CAF50' if v >= 0.6 else '#f44336' for v in values]
    bars = plt.bar(categories, values, color=colors, edgecolor='white', linewidth=0.5)

    plt.ylim(0, 1)
    plt.ylabel("Score (0 to 1)")
    plt.title("Your Skill Scores by Category")
    plt.xticks(rotation=15, fontsize=9)

    # Add value label on top of each bar
    for bar, val in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{round(val * 100)}%",
            ha='center', va='bottom', fontsize=8
        )

    plt.tight_layout()                  # Prevents labels from getting cut off
    plt.savefig("static/chart.png", dpi=100)
    plt.close()                         # Important: closes figure to free memory
