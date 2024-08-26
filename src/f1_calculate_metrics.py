import pandas as pd
from tqdm import tqdm
import logging

from logging_config import ContextFilter, setup_logging
import config.paths as paths
from utils import read_csv_as_df, get_dataset_files, get_predictions, save_df_as_csv
from config.variables import scenarios
from metrics import get_binary_classification_scores

logger = logging.getLogger(__name__)
setup_logging(paths.METRICS_CALCULATION_LOG_FPATH)


def calculate_metrics(models: pd.DataFrame, datasets: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate metrics for a given dataframe.

    Args:
        models (pd.DataFrame): Dataframe containing list of models.
        datasets (pd.DataFrame): Dataframe containing list of datasets.

    Returns:
        pd.DataFrame: Dataframe containing metrics.
    """
    all_metrics = []

    total_iterations = len(datasets) * len(scenarios) * len(models)

    with tqdm(total=total_iterations, desc="Calculating Metrics", unit="task") as pbar:
        for _, dataset_row in datasets.iterrows():
            dataset = dataset_row["dataset"]
            # read the dataset schema and test key files
            data_schema, test_key = get_dataset_files(dataset)

            for scenario in scenarios:
                for _, model_row in models.iterrows():
                    model = model_row["model"]

                    # Create a ContextFilter with the current dataset, scenario, and model
                    context_filter = ContextFilter(
                        dataset=dataset,
                        scenario=scenario,
                        model=model,
                    )

                    # read the predictions
                    predictions = get_predictions(scenario, dataset, model)
                    # calculate the metrics
                    metrics = get_binary_classification_scores(
                        data_schema,
                        test_key,
                        predictions,
                        context_filter,
                    )
                    metrics["scenario"] = scenario
                    metrics["dataset"] = dataset
                    metrics["model"] = model
                    metrics["fold_number"] = int(dataset[-1])
                    all_metrics.append(metrics)
                    pbar.update(1)

    reordered_cols = [
        "scenario",
        "dataset",
        "model",
        "fold_number",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "f2_score",
        "auc_score",
        "pr_auc_score",
    ]
    results_df = pd.DataFrame(all_metrics)[reordered_cols]
    # save the metrics
    save_df_as_csv(results_df, paths.METRICS_FPATH)
    logger.info("Metrics calculated and saved.")


if __name__ == "__main__":
    models_df = read_csv_as_df(paths.MODELS_FPATH)
    datasets_df = read_csv_as_df(paths.DATASETS_FPATH)
    calculate_metrics(models_df, datasets_df)
