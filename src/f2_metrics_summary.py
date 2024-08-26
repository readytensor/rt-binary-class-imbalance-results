import pandas as pd

from utils import read_csv_as_df
from config.variables import metrics, chart_cfg
from config import paths


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
    prepared_df = prepared_df.merge(models, on="model").merge(datasets, on="dataset")
    return prepared_df


def aggregate_metrics(metrics_df: pd.DataFrame, by: str = "overall") -> pd.DataFrame:
    """
    Aggregate metrics for each scenario and metric. Calculates the mean across models,
    datasets, for each scenario, metric, and fold. Then calculates the mean and standard
    deviation across the 5 folds.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing the metrics for 9000 experiments.
        by (str): The level at which to aggregate the metrics. Can be 'overall', 'model', or 'dataset'.

    Returns:
        pd.DataFrame: Aggregated DataFrame with columns: 'scenario', 'metric', 'mean', 'std_dev'.
    """
    if by == "overall":
        groupby = []

    elif by == "model":
        groupby = ["model"]

    elif by == "dataset":
        groupby = ["dataset"]
        metrics_df["dataset"] = metrics_df["dataset"].str.replace(
            r"_fold_\d+", "", regex=True
        )

    elif by == "model_dataset":
        groupby = ["model", "dataset"]
        metrics_df["dataset"] = metrics_df["dataset"].str.replace(
            r"_fold_\d+", "", regex=True
        )

    # Calculate the mean across all models and datasets for each scenario, metric, and fold
    grouped = (
        metrics_df.groupby(["scenario", "fold_number"] + groupby)[metrics]
        .mean()
        .reset_index()
    )

    # Calculate the mean and standard deviation across the 5 folds
    aggregated = (
        grouped.groupby(["scenario"] + groupby)[metrics]
        .agg(["mean", "std"])
        .reset_index()
    )

    # Flatten the multi-level column index created by the aggregation
    aggregated.columns = ["_".join(col).strip("_") for col in aggregated.columns]

    # Reshape the DataFrame to have 'scenario', 'metric', 'mean', and 'std_dev' columns
    aggregated_melted = aggregated.melt(
        id_vars=(["scenario"] + groupby), var_name="metric_stat", value_name="value"
    )

    # Split the 'metric_stat' column into separate 'metric' and 'stat' columns
    aggregated_melted[["metric", "stat"]] = aggregated_melted["metric_stat"].str.rsplit(
        "_", n=1, expand=True
    )

    # Pivot the table to get 'mean' and 'std_dev' as separate columns
    aggregated_pivot = aggregated_melted.pivot_table(
        index=["scenario", "metric"] + groupby, columns="stat", values="value"
    ).reset_index()

    if "model" in groupby:
        aggregated_pivot["model"] = aggregated_pivot["model"].map(
            chart_cfg["ordered_models"], na_action="ignore"
        )

    # Rename the index
    aggregated_pivot.rename_axis(None, axis=1, inplace=True)
    aggregated_pivot["mean ± std"] = (
        aggregated_pivot["mean"].round(3).astype(str)
        + " ± "
        + aggregated_pivot["std"].round(4).astype(str)
    )
    aggregated_pivot.drop(columns=["mean", "std"], inplace=True)

    aggregated_pivot.set_index(["scenario", "metric"] + groupby, inplace=True)
    return aggregated_pivot


def summarize_metrics():
    models_df = read_csv_as_df(paths.MODELS_FPATH)
    datasets_df = read_csv_as_df(paths.DATASETS_FPATH)
    orig_metrics = read_csv_as_df(paths.METRICS_FPATH)
    prepared_metrics_df = merge_metrics_with_metadata(
        orig_metrics, models_df, datasets_df
    )
    aggregated_df = aggregate_metrics(prepared_metrics_df, by="overall")
    aggregated_df.to_csv(paths.OVERALL_METRICS_FPATH)

    aggregated_df = aggregate_metrics(prepared_metrics_df, by="dataset")
    aggregated_df.to_csv(paths.BY_DATASET_METRICS_FPATH)

    aggregated_df = aggregate_metrics(prepared_metrics_df, by="model")
    aggregated_df.to_csv(paths.BY_MODEL_METRICS_FPATH)

    aggregated_df = aggregate_metrics(prepared_metrics_df, by="model_dataset")
    aggregated_df.to_csv(paths.BY_MODEL_DATASET_METRICS_FPATH)


if __name__ == "__main__":
    summarize_metrics()
