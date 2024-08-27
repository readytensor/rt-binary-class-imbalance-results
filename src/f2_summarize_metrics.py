"""
Aggregate and summarize classification metrics from binary class imbalance experiments.

This script processes the raw metrics CSV file generated by the 'f1_calculate_metrics.py' script.
It merges these metrics with model and dataset metadata, then aggregates them at various 
levels (overall, by dataset, by model, and by model-dataset combination), computing mean 
and standard deviation across folds.

Prerequisites:
    - Raw metrics CSV file generated by 'f1_calculate_metrics.py'

Usage:
    python f2_summarize_metrics.py

Outputs:
    CSV files containing summarized metrics at different aggregation levels.
"""

import pandas as pd
from typing import List, Optional

from utils import read_csv_as_df, save_dataframe_as_csv
from config.variables import ordered_scenarios, ordered_metrics, ordered_models
from config import paths, variables


def prepare_metrics_df_with_metadata(
    metrics_df: pd.DataFrame,
    ordered_models: List[str],
) -> pd.DataFrame:
    """
    Prepare metrics dataframe with metadata from models and datasets.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing the metrics for all experiments.
        ordered_models List[str]: Ordered list of all models.

    Returns:
        pd.DataFrame: DataFrame containing the metrics with metadata (e.g., dataset, fold, model order).
    """
    prepared_df = metrics_df.copy()
    prepared_df["Dataset"] = prepared_df["Dataset_Fold"].map(
        lambda x: x.split("_fold")[0]
    )
    prepared_df["Fold"] = prepared_df["Dataset_Fold"].map(lambda x: x[-1]).astype(int)
    
    # Create a mapping of model names to their order
    models_order = {model: i for i, model in enumerate(ordered_models)}
    prepared_df["Model Order"] = prepared_df["Model"].map(models_order)
    
    return prepared_df


def aggregate_metrics(metrics_df: pd.DataFrame, by: str = "overall") -> pd.DataFrame:
    """
    Aggregate metrics for each scenario and metric. Calculates the mean across models,
    datasets, for each scenario, metric, and fold. Then calculates the mean and standard
    deviation across the 5 folds.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing the metrics for 9000 experiments.
        by (str): The level at which to aggregate the metrics. Can be 'overall', 'model', 'dataset', or 'model_dataset'.

    Returns:
        pd.DataFrame: Aggregated DataFrame with columns: 'Scenario', 'Metric', 'Mean ± Std Dev'.
    """
    if by == "overall":
        groupby_columns = []

    elif by == "model":
        groupby_columns = ["Model", "Model Order"]

    elif by == "dataset":
        groupby_columns = ["Dataset"]
        metrics_df["Dataset"] = metrics_df["Dataset"].str.replace(
            r"_fold_\d+", "", regex=True
        )

    elif by == "model_dataset":
        groupby_columns = ["Model", "Model Order", "Dataset"]
        metrics_df["Dataset"] = metrics_df["Dataset"].str.replace(
            r"_fold_\d+", "", regex=True
        )

    # Calculate the mean across all models and datasets for each scenario, metric, and fold
    grouped = (
        metrics_df.groupby(["Scenario", "Fold"] + groupby_columns)[ordered_metrics]
        .mean()
        .reset_index()
    )

    # Calculate the mean and standard deviation across the 5 folds
    aggregated = (
        grouped.groupby(["Scenario"] + groupby_columns)[ordered_metrics]
        .agg(["mean", "std"])
        .reset_index()
    )

    # Flatten the multi-level column index created by the aggregation
    aggregated.columns = ["_".join(col).strip("_") for col in aggregated.columns]

    # Reshape the DataFrame to have 'Scenario', 'Metric', 'Mean ± Std Dev' columns
    aggregated_melted = aggregated.melt(
        id_vars=(["Scenario"] + groupby_columns), var_name="metric_stat", value_name="value"
    )

    # Split the 'metric_stat' column into separate 'metric' and 'stat' columns
    aggregated_melted[["Metric", "Stat"]] = aggregated_melted["metric_stat"].str.rsplit(
        "_", n=1, expand=True
    )

    # Pivot the table to get 'mean' and 'std_dev' as separate columns
    aggregated_pivot = aggregated_melted.pivot_table(
        index=["Scenario", "Metric"] + groupby_columns, columns="Stat", values="value"
    ).reset_index()

    # Combine the mean and standard deviation into a single column
    aggregated_pivot["Mean ± Std Dev"] = (
        aggregated_pivot["mean"].round(variables.rounding).astype(str)
        + " ± "
        + aggregated_pivot["std"].round(variables.rounding).astype(str)
    )

    # Drop the 'mean' and 'std' columns as they are now combined
    aggregated_pivot.drop(columns=["mean", "std"], inplace=True)

    # Set the index back
    aggregated_pivot.set_index(["Scenario", "Metric"] + groupby_columns, inplace=True)
    
    return aggregated_pivot


def summarize_metrics():
    """
    Summarize the metrics by aggregating them at various levels (overall, by dataset, by model, 
    and by model-dataset combination) and saving the summarized metrics to CSV files.
    """
    orig_metrics = read_csv_as_df(paths.METRICS_FPATH)
    prepared_metrics_df = prepare_metrics_df_with_metadata(orig_metrics, ordered_models)

    # Summarize at various levels and save the results
    aggregated_df = aggregate_metrics(prepared_metrics_df, by="overall")
    save_dataframe_as_csv(aggregated_df, paths.OVERALL_METRICS_FPATH, index=True)

    aggregated_df = aggregate_metrics(prepared_metrics_df, by="dataset")
    save_dataframe_as_csv(aggregated_df, paths.BY_DATASET_METRICS_FPATH, index=True)

    aggregated_df = aggregate_metrics(prepared_metrics_df, by="model")
    save_dataframe_as_csv(aggregated_df, paths.BY_MODEL_METRICS_FPATH, index=True)

    aggregated_df = aggregate_metrics(prepared_metrics_df, by="model_dataset")
    save_dataframe_as_csv(
        aggregated_df, paths.BY_MODEL_DATASET_METRICS_FPATH, index=True
    )

    print("Metrics summarized.")


def pivot_and_order_table(
    df: pd.DataFrame,
    index_cols: List[str],
    ordered_scenarios: List[str],
    ordered_metrics: List[str],
    models: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Pivot the table and order the columns and rows according to specified orders.

    Args:
        df (pd.DataFrame): DataFrame to pivot.
        index_cols (List[str]): Columns to use as the index in the pivot table.
        ordered_scenarios (List[str]): Ordered list of scenario names.
        ordered_metrics (List[str]): Ordered list of metric names.
        models (Optional[List[str]]): Ordered list of model names, if applicable.

    Returns:
        pd.DataFrame: Pivoted and ordered DataFrame.
    """
    # Pivot the table
    pivoted = df.pivot(index=index_cols, columns="Scenario", values="Mean ± Std Dev")

    # Reorder the columns (scenarios)
    pivoted = pivoted.reindex(columns=ordered_scenarios)

    # Reset index to make all columns available
    pivoted.reset_index(inplace=True)

    # Create a sorting key based on the order of metrics and models
    sort_columns = []
    if "Metric" in index_cols:
        pivoted["Metric"] = pd.Categorical(
            pivoted["Metric"], categories=ordered_metrics, ordered=True
        )
        sort_columns.append("Metric")

    if "Model" in index_cols and models:
        sort_columns.append("Model Order")

    # Sort the dataframe
    if sort_columns:
        pivoted.sort_values(sort_columns, inplace=True)
    
    # Remove the temporary 'Model Order' column if it was created
    if "Model Order" in pivoted.columns:
        pivoted.drop("Model Order", axis=1, inplace=True)

    return pivoted


def create_pivoted_tables():
    """
    Create pivoted tables from the aggregated metrics and save them to CSV files.
    """
    # Read the CSV files
    overall_df = read_csv_as_df(paths.OVERALL_METRICS_FPATH)
    by_dataset_df = read_csv_as_df(paths.BY_DATASET_METRICS_FPATH)
    by_model_df = read_csv_as_df(paths.BY_MODEL_METRICS_FPATH)
    by_model_dataset_df = read_csv_as_df(paths.BY_MODEL_DATASET_METRICS_FPATH)

    # Create pivoted tables
    overall_pivoted = pivot_and_order_table(overall_df, ["Metric"], 
        ordered_scenarios,
        ordered_metrics
    )
    by_dataset_pivoted = pivot_and_order_table(
        by_dataset_df, ["Metric", "Dataset"], 
        ordered_scenarios,
        ordered_metrics,
    )
    by_model_pivoted = pivot_and_order_table(
        by_model_df,
        ["Metric", "Model", "Model Order"],
        ordered_scenarios,
        ordered_metrics,
        ordered_models,
    )
    by_model_dataset_pivoted = pivot_and_order_table(
        by_model_dataset_df,
        ["Metric", "Dataset", "Model", "Model Order"],
        ordered_scenarios,
        ordered_metrics,
        ordered_models,
    )

    # Save the pivoted tables
    save_dataframe_as_csv(overall_pivoted, paths.OVERALL_PIVOTED_METRICS_FPATH)
    save_dataframe_as_csv(by_dataset_pivoted, paths.BY_DATASET_PIVOTED_METRICS_FPATH)
    save_dataframe_as_csv(by_model_pivoted, paths.BY_MODEL_PIVOTED_METRICS_FPATH)
    save_dataframe_as_csv(
        by_model_dataset_pivoted, paths.BY_MODEL_DATASET_PIVOTED_METRICS_FPATH
    )

    print("Pivoted tables created and saved.")


if __name__ == "__main__":
    summarize_metrics()
    create_pivoted_tables()
