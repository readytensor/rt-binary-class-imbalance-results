import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import read_csv_as_df
from config import paths
from config.chart_cfg import (
    table_font_size,
    header_font_size,
    table_first_col_font_size,
    table_background_color,
    table_background_color2,
    table_first_row_background_color,
    table_first_col_background_color,
    table_outer_border_thickness,
    table_inner_border_thickness,
    table_outer_border_color,
    table_inner_border_color,
    font_type,
    highlight_color,
)
from charts.chart_utils import df_to_svg, find_extreme_cells
from config.variables import ordered_scenarios


def filter_df_col_by_val(df, col, val, drop_col=True):
    """
    Filter a DataFrame by a specific value in a column.
    """
    filtered_df = df[df[col] == val].copy()
    if drop_col:
        filtered_df.drop(col, axis=1, inplace=True)
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
    highlight_cells = find_extreme_cells(overall_results, ordered_scenarios)
    df_to_svg(
        overall_results,
        filepath=paths.OVERALL_RESULTS_TABLE_SVG,
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

    # Results by model
    by_model_results = read_csv_as_df(paths.BY_MODEL_PIVOTED_METRICS_FPATH)
    by_model_results_filtered = filter_df_col_by_val(
        by_model_results, "Metric", "F1-score", drop_col=True
    )
    highlight_cells = find_extreme_cells(by_model_results_filtered, ordered_scenarios)
    df_to_svg(
        by_model_results_filtered,
        filepath=paths.BY_MODEL_F1_RESULTS_TABLE_SVG,
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

    # Results by dataset
    by_dataset_results = read_csv_as_df(paths.BY_DATASET_PIVOTED_METRICS_FPATH)
    by_dataset_results_filtered = filter_df_col_by_val(
        by_dataset_results, "Metric", "F1-score", drop_col=True
    )
    highlight_cells = find_extreme_cells(by_dataset_results_filtered, ordered_scenarios)
    df_to_svg(
        by_dataset_results_filtered,
        filepath=paths.BY_DATASET_F1_RESULTS_TABLE_SVG,
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

    print("Table svgs created.")


if __name__ == "__main__":
    generate_table_svgs()
