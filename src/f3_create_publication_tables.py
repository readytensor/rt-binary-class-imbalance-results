import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Optional
from utils import read_csv_as_df, save_dataframe_as_csv
from config import paths
from config.variables import scenarios, metrics, models


def create_markdown_table(df):
    # Function to bold the highest value in a row
    def bold_max(row):
        # Extract numeric values
        values = row.iloc[1:].apply(lambda x: float(x.split("±")[0].strip()))
        max_value = values.max()
        return row.apply(
            lambda x: f"**{x}**"
            if isinstance(x, str) and x.split("±")[0].strip() == str(max_value)
            else x
        )

    # Apply bold_max to each row
    df_bold = df.apply(bold_max, axis=1)

    # Convert to markdown
    markdown_table = df_bold.to_markdown(index=False)
    return markdown_table


def create_table_image(df):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(4, len(df) * 0.2))

    # Hide axes
    ax.axis("tight")
    ax.axis("off")

    # Create the table
    table = ax.table(
        cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center"
    )

    # Highlight the maximum values
    for row in range(len(df)):
        values = df.iloc[row, 1:].apply(lambda x: float(x.split("±")[0].strip()))
        max_value = values.max()
        for col in range(1, len(df.columns)):
            cell = table[row + 1, col]
            if df.iloc[row, col].split("±")[0].strip() == str(max_value):
                cell.set_text_props(weight="bold", color="red")

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(paths.OVERALL_TABLE_IMAGE_PATH, dpi=300, bbox_inches="tight")
    plt.close()


def process_overall_results():
    # Read the overall pivoted metrics
    df = read_csv_as_df(paths.OVERALL_PIVOTED_METRICS_FPATH)

    # Create markdown table
    markdown_table = create_markdown_table(df)
    with open(paths.OVERALL_MARKDOWN_TABLE_PATH, "w") as f:
        f.write(markdown_table)

    # Create table image
    create_table_image(df)

    print("Overall results processed: markdown table and heatmap created.")


if __name__ == "__main__":
    process_overall_results()
