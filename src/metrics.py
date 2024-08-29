import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    fbeta_score,
    precision_recall_curve,
    auc,
    log_loss,
    brier_score_loss,
    matthews_corrcoef,
)
import logging

from logging_config import ContextFilter

logger = logging.getLogger(__name__)


def get_binary_classification_scores(
    data_schema: dict,
    test_key: pd.DataFrame,
    predictions: pd.DataFrame,
    context_filter: ContextFilter,
):
    """
    Calculates various metrics given the test_key, predictions, and schema file.

    Args:
        data_schema (dict): Dictionary containing data schema.
        test_key (pd.DataFrame): Dataframe containing test key.
        predictions (pd.DataFrame): Dataframe containing predictions.
        context_filter (ContextFilter): Logging filter with context info (dataset, scenario, model).

    Returns:
        dict: JSON object with metric names as keys and metric values as values.
    """
    logger.addFilter(context_filter)  # Add the context filter to the logger
    logger.info(
        "Starting metric calculation for dataset: %s, scenario: %s, model: %s",
        context_filter.dataset,
        context_filter.scenario,
        context_filter.model,
    )

    # Extract necessary fields from the schema
    id_field = data_schema["id"]["name"]
    target_class = str(data_schema["target"]["classes"][1])
    target_field = data_schema["target"]["name"]
    target_classes = data_schema["target"]["classes"]

    # Extract true labels
    Y = test_key[target_field].astype(str)
    obs_class_names = list(set(Y))

    # Rename prediction columns to match class names
    pred_class_names = [str(c) for c in predictions[obs_class_names]]
    predictions.columns = [str(c) for c in list(predictions.columns)]

    # Apply decision threshold if available
    if "decision_threshold" in predictions.columns:
        logger.debug("Applying decision threshold.")
        predictions["__pred_class"] = predictions.apply(
            lambda row: target_classes[1]
            if row[target_classes[1]] >= row["decision_threshold"]
            else target_classes[0],
            axis=1,
        )
    else:
        predictions["__pred_class"] = pd.DataFrame(
            predictions[pred_class_names], columns=pred_class_names
        ).idxmax(axis=1)

    # Merge predictions with the true labels
    predictions = predictions.merge(test_key[[id_field, target_field]], on=[id_field])
    Y_hat = predictions["__pred_class"].astype(str)

    # Check for all negative predictions
    if len(set(Y_hat)) == 1:
        logger.warning("All predictions are of a single class: %s", Y_hat.iloc[0])

    # Convert to binary labels for metric calculation
    y_true = np.where(Y == target_class, 1.0, 0.0)
    y_pred = np.where(Y_hat == target_class, 1.0, 0.0)
    y_pred_proba = predictions[target_class].values

    logger.debug("Calculating metrics.")
    # Calculate metrics with zero_division parameter
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    f2 = fbeta_score(y_true, y_pred, beta=2, zero_division=0)

    # ROC-AUC score
    roc_auc = roc_auc_score(y_true, y_pred_proba)

    # PR-AUC score
    precision_curve, recall_curve, _ = precision_recall_curve(y_true, y_pred_proba)
    pr_auc = auc(recall_curve, precision_curve)

    logloss = log_loss(y_true, y_pred_proba)
    brier = brier_score_loss(y_true, y_pred_proba)
    mcc = matthews_corrcoef(y_true, y_pred)

    # Compile all metrics into a dictionary
    scores = {
        "Accuracy": np.round(accuracy, 4),
        "Precision": np.round(precision, 4),
        "Recall": np.round(recall, 4),
        "F1-score": np.round(f1, 4),
        "F2-score": np.round(f2, 4),
        "AUC": np.round(roc_auc, 4),
        "PR-AUC": np.round(pr_auc, 4),
        "Log-Loss": np.round(logloss, 4),
        "Brier-Score": np.round(brier, 4),
        "MCC": np.round(mcc, 4),
    }

    logger.info("Metric calculation complete.")
    logger.removeFilter(context_filter)
    return scores
