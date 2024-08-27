import json
import os
import pandas as pd
from typing import Any, Dict, List, Tuple, Union

import config.paths as paths


def read_json_as_dict(input_path: str) -> Dict:
    """
    Reads a JSON file and returns its content as a dictionary.
    """
    with open(input_path, "r", encoding="utf-8") as file:
        json_data_as_dict = json.load(file)

    return json_data_as_dict


def read_csv_as_df(input_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns its content as a pandas DataFrame.
    """
    return pd.read_csv(input_path)


def save_df_as_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Saves a pandas dataframe to a CSV file in the given directory path.
    Float values are saved with 4 decimal places.
    """
    df.to_csv(file_path, index=False, float_format="%.4f")


def save_dataframe_as_csv(dataframe: pd.DataFrame, file_path: str) -> None:
    """
    Saves a pandas dataframe to a CSV file in the given directory path.
    Float values are saved with 4 decimal places.

    Args:
    - df (pd.DataFrame): The pandas dataframe to be saved.
    - file_path (str): File path and name to save the CSV file.
    """
    dataframe.to_csv(file_path, index=False, float_format="%.4f")


def get_dataset_files(dataset_name: str):
    """Read the test_key and schema files for a given dataset.

    Args:
    - dataset_name (str): The name of the dataset.

    Returns:
    - data_schema (Dict): The schema of the dataset.
    - test_key (pd.DataFrame): The test key of the dataset.
    """
    data_schema_path = os.path.join(
        paths.DATASETS_DIR, dataset_name, f"{dataset_name}_schema.json"
    )
    with open(data_schema_path, "r", encoding="utf-8") as f:
        data_schema = json.load(f)

    test_key = pd.read_csv(
        os.path.join(
            paths.DATASETS_DIR, dataset_name, f"{dataset_name}_test_key.csv.gz"
        )
    )
    return data_schema, test_key


def get_predictions(
    scenario_name: str, dataset_name: str, model_name: str
) -> pd.DataFrame:
    """Read the predictions for a given dataset and model.

    Args:
    - scenario_name (str): The name of the scenario.
    - dataset_name (str): The name of the dataset.
    - model_name (str): The name of the model.

    Returns:
    - predictions (pd.DataFrame): The predictions of the dataset.
    """
    compressed_path = os.path.join(
        paths.PREDICTIONS_DIR,
        scenario_name,
        model_name,
        dataset_name,
        "predictions.csv.gz",
    )

    path = os.path.join(
        paths.PREDICTIONS_DIR,
        scenario_name,
        model_name,
        dataset_name,
        "predictions.csv",
    )
    predictions = pd.read_csv(
        compressed_path if os.path.exists(compressed_path) else path
    )
    return predictions


def prepare_data(metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the data for visualization by melting the dataframe and sorting the values.
    """
    metrics = metrics.melt(
        id_vars=["scenario", "model", "dataset", "fold_number"],
        value_vars=[
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "f2_score",
            "auc_score",
            "pr_auc_score",
        ],
        var_name="metric",
        value_name="score",
    )

    metrics = metrics.pivot_table(
        index=["model", "dataset", "metric", "fold_number"],
        columns="scenario",
        values="score",
    ).reset_index()
    return metrics