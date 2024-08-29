"""
This module generates SVG tables for overall results, results by model, and results by dataset,
based on CSV files containing pivoted metrics. The tables are styled with customizable parameters 
including font sizes, background colors, and border settings. The tables highlight specific cells 
based on the extreme values (e.g., maximum or minimum) within specified columns.

Main components:
- `filter_df_col_by_val`: Filters a DataFrame by a specific value in a column and optionally 
                          drops the column.
- `generate_table_svgs`: Reads data from CSV files, applies styling and cell highlighting, 
                        and generates SVG tables.

External dependencies:
- pandas for DataFrame manipulation.
- matplotlib for plotting.
- Custom utility modules for reading CSV files and configuring chart settings.
"""
import os

from utils import read_csv_as_df
from config import paths
from config.chart_cfg import (
    table_font_size,
    header_font_size,
    table_background_color,
    table_background_color2,
    table_first_row_background_color,
    table_outer_border_thickness,
    table_inner_border_thickness,
    table_outer_border_color,
    table_inner_border_color,
    font_type,
    highlight_color,
)
from charts.chart_utils import df_to_svg, find_extreme_cells
from config.variables import ordered_scenarios, metrics


def filter_df_col_by_val(df, col, val, drop_col=True):
    """
    Filter a DataFrame by a specific value in a column.
    """
    filtered_df = df[df[col] == val].copy()
    if drop_col:
        filtered_df.drop(col, axis=1, inplace=True)
    return filtered_df


def filter_df_by_min_max_metrics(df, metrics, min_max):
    """
    Filter a DataFrame by minimum or maximum values of specified metrics.

    Args:
    - df (pd.DataFrame): DataFrame containing metrics.
    - metrics (List[Dict]): List of dictionaries containing metric names and min or max type.
    - min_max (str): Type: "min" or "max".
    """
    filtered_metrics = [
        metric["name"] for metric in metrics if metric["min_max"] == min_max
    ]
    filtered_df = df[df["Metric"].isin(filtered_metrics)].copy()
    return filtered_df


def generate_table_svgs():
    common_params = {
        "bold_first_row": True,
        "bold_first_col": True,
        "header_font_size": header_font_size,
        "body_font_size": table_font_size,
        "header_bg_color": table_first_row_background_color,
        "body_bg_color": [table_background_color, table_background_color2],
        "outer_border_thickness": table_outer_border_thickness,
        "inner_border_thickness": table_inner_border_thickness,
        "outer_border_color": table_outer_border_color,
        "inner_border_color": table_inner_border_color,
        "font_type": font_type,
        "highlight_color": highlight_color,
    }

    # Overall results
    overall_results = read_csv_as_df(paths.OVERALL_PIVOTED_METRICS_FPATH)
    highlight_cells = {}
    for min_max in ["min", "max"]:
        filtered_df = filter_df_by_min_max_metrics(overall_results, metrics, min_max)
        highlight_cells.update(
            find_extreme_cells(
                filtered_df,
                ordered_scenarios,
                by="row",
                extreme=min_max,
            )
        )
    df_to_svg(
        overall_results,
        filepath=os.path.join(paths.CHARTS_DIR, "overall_results.svg"),
        highlight_cells=highlight_cells,
        center_align_columns=ordered_scenarios,
        column_widths={
            "Metric": 120,
            "Baseline": 150,
            "SMOTE": 150,
            "Class Weights": 150,
            "Decision Threshold": 210,
        },
        **common_params,
    )

    # Results by model and dataset
    by_model_results = read_csv_as_df(paths.BY_MODEL_PIVOTED_METRICS_FPATH)
    by_dataset_results = read_csv_as_df(paths.BY_DATASET_PIVOTED_METRICS_FPATH)

    for metric in [m["name"] for m in metrics]:
        # By model results
        by_model_results_filtered = filter_df_col_by_val(
            by_model_results, "Metric", metric, drop_col=True
        )
        extreme = (
            "max"
            if any(m["name"] == metric and m["min_max"] == "max" for m in metrics)
            else "min"
        )
        highlight_cells = find_extreme_cells(
            by_model_results_filtered, ordered_scenarios, by="row", extreme=extreme
        )
        df_to_svg(
            by_model_results_filtered,
            filepath=os.path.join(paths.CHARTS_DIR, f"{metric}_results_by_model.svg"),
            highlight_cells=highlight_cells,
            center_align_columns=ordered_scenarios,
            column_widths={
                "Model": 180,
                "Baseline": 150,
                "SMOTE": 150,
                "Class Weights": 150,
                "Decision Threshold": 210,
            },
            **common_params,
        )

        # By dataset results
        by_dataset_results_filtered = filter_df_col_by_val(
            by_dataset_results, "Metric", metric, drop_col=True
        )
        highlight_cells = find_extreme_cells(
            by_dataset_results_filtered, ordered_scenarios, by="row", extreme=extreme
        )
        df_to_svg(
            by_dataset_results_filtered,
            filepath=os.path.join(paths.CHARTS_DIR, f"{metric}_results_by_dataset.svg"),
            highlight_cells=highlight_cells,
            center_align_columns=ordered_scenarios,
            column_widths={
                "Dataset": 250,
                "Baseline": 150,
                "SMOTE": 150,
                "Class Weights": 150,
                "Decision Threshold": 210,
            },
            **common_params,
        )

    print("Table SVGs created.")


if __name__ == "__main__":
    generate_table_svgs()
