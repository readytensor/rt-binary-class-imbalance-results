import pandas as pd
import paths

from utils import read_csv_as_df
from variables import metrics


def merge_metrics_with_metadata(
    metrics_df: pd.DataFrame,
    models: pd.DataFrame,
    datasets: pd.DataFrame,
) -> pd.DataFrame:
    """Merge metrics with metadata from models and datasets.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing the metrics for all experiments.
        models (pd.DataFrame): DataFrame containing the metadata for all models.
        datasets (pd.DataFrame): DataFrame containing the metadata for all datasets.

    Returns:
        pd.DataFrame: DataFrame containing the metrics with metadata.
    """
    prepared_df = metrics_df.copy()
    prepared_df = prepared_df.merge(models, on="model").merge(
        datasets, on="dataset"
    )
    return prepared_df


def aggregate_overall_metrics(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate metrics for each scenario and metric. Calculates the mean across models,
    datasets, for each scenario, metric, and fold. Then calculates the mean and standard
    deviation across the 5 folds.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing the metrics for 9000 experiments.

    Returns:
        pd.DataFrame: Aggregated DataFrame with columns: 'scenario', 'metric', 'mean', 'std_dev'.
    """

    # Calculate the mean across all models and datasets for each scenario, metric, and fold
    grouped = (
        metrics_df.groupby(["scenario", "fold_number"])[metrics]
        .mean()
        .reset_index()
    )

    # Calculate the mean and standard deviation across the 5 folds
    aggregated = (
        grouped.groupby("scenario")[metrics].agg(["mean", "std"]).reset_index()
    )

    # Flatten the multi-level column index created by the aggregation
    aggregated.columns = ["_".join(col).strip("_") for col in aggregated.columns]

    # Reshape the DataFrame to have 'scenario', 'metric', 'mean', and 'std_dev' columns
    aggregated_melted = aggregated.melt(
        id_vars="scenario", var_name="metric_stat", value_name="value"
    )

    # Split the 'metric_stat' column into separate 'metric' and 'stat' columns
    aggregated_melted[["metric", "stat"]] = aggregated_melted["metric_stat"].str.rsplit(
        "_", n=1, expand=True
    )

    # Pivot the table to get 'mean' and 'std_dev' as separate columns
    aggregated_pivot = aggregated_melted.pivot_table(
        index=["scenario", "metric"], columns="stat", values="value"
    ).reset_index()

    # Rename the columns
    aggregated_pivot.columns = ["scenario", "metric", "mean", "std_dev"]

    return aggregated_pivot


def summarize_metrics():
    models_df = read_csv_as_df(paths.MODELS_FPATH)
    datasets_df = read_csv_as_df(paths.DATASETS_FPATH)
    orig_metrics = read_csv_as_df(paths.METRICS_FPATH)
    prepared_metrics_df = merge_metrics_with_metadata(
        orig_metrics, models_df, datasets_df
    )
    aggregated_df = aggregate_overall_metrics(prepared_metrics_df)
    print(aggregated_df)


if __name__ == "__main__":
    summarize_metrics()
