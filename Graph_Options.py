import pandas as pd
import os
import matplotlib.pyplot as plt


def graph_all(region_code):
    # Check if the file exists
    file_path = f"trending_videos{region_code}.csv"
    if not os.path.exists(file_path):
        print(f"The data for region code {region_code} has not been added to a file.\n")
        return
    df = pd.read_csv(f"trending_videos{region_code}.csv")
    category_counts = df['Categories'].value_counts()
    rainbow_cmap = plt.cm.rainbow

    # Create a range of colors based on the number of categories
    colors = [rainbow_cmap(i / len(category_counts)) for i in range(len(category_counts))]

    # Create the horizontal bar chart with rainbow colors
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(category_counts.index, category_counts.values, color=colors)
    region_title = region_code.upper()
    plt.title("Category Distribution (" + region_title + ")")
    plt.xlabel("Categories")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

