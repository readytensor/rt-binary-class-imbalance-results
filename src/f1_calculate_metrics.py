"""
Calculate classification metrics for binary class imbalance experiments.

This script processes prediction results across multiple datasets, models, and
imbalance handling scenarios. It computes various performance metrics and saves
the results to a CSV file.

Usage:
    python f1_calculate_metrics.py

Requires:
    - Prediction files for each dataset-model-scenario combination
    - Dataset schema and test key files
    - CSV files listing models and datasets
"""

import pandas as pd
from tqdm import tqdm
import logging

from logging_config import ContextFilter, setup_logging
import config.paths as paths
from utils import (
    get_dataset_files,
    get_predictions,
    save_dataframe_as_csv,
)
from config.variables import scenarios_mapping, models_mapping, dataset_folds
from metrics import get_binary_classification_scores

logger = logging.getLogger(__name__)
setup_logging(paths.METRICS_CALCULATION_LOG_FPATH)


def calculate_metrics() -> pd.DataFrame:
    """
    Calculate metrics for a given dataframe.

    Returns:
        pd.DataFrame: Dataframe containing metrics.
    """
    print("Calculating metrics on all experiments' predictions...")
    all_metrics = []
    scenarios = list(scenarios_mapping.keys())
    models = list(models_mapping.keys())
    total_iterations = len(dataset_folds) * len(scenarios) * len(models)

    with tqdm(total=total_iterations, desc="Calculating Metrics", unit="task") as pbar:
        for dataset_fold in dataset_folds:
            # read the dataset schema and test key files
            data_schema, test_key = get_dataset_files(dataset_fold)

            for scenario in scenarios:
                for model in models:
                    # Create a ContextFilter with the current dataset_fold, scenario, and model
                    context_filter = ContextFilter(
                        dataset=dataset_fold,
                        scenario=scenario,
                        model=model,
                    )

                    # read the predictions
                    predictions = get_predictions(scenario, dataset_fold, model)
                    # calculate the metrics
                    metrics = get_binary_classification_scores(
                        data_schema,
                        test_key,
                        predictions,
                        context_filter,
                    )
                    metrics["Scenario"] = scenario
                    metrics["Dataset_Fold"] = dataset_fold
                    metrics["Model"] = model
                    all_metrics.append(metrics)
                    pbar.update(1)

    reordered_cols = [
        "Scenario",
        "Dataset_Fold",
        "Model",
        "Accuracy",
        "MCC",
        "Precision",
        "Recall",
        "F1-score",
        "F2-score",
        "AUC",
        "PR-AUC",
        "Log-Loss",
        "Brier-Score",
    ]
    results_df = pd.DataFrame(all_metrics)[reordered_cols]
    # map scenario names to scenario display names
    results_df["Scenario"] = results_df["Scenario"].map(scenarios_mapping)
    results_df["Model"] = results_df["Model"].map(models_mapping)
    # save the metrics
    save_dataframe_as_csv(results_df, paths.METRICS_FPATH)
    logger.info("Metrics calculated and saved.")


if __name__ == "__main__":
    calculate_metrics()
