import os

f_path = os.path.abspath(__file__)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(f_path)))

# input data
DATA_DIR = os.path.join(ROOT_PATH, "data")
DATASETS_DIR = os.path.join(DATA_DIR, "datasets")
PREDICTIONS_DIR = os.path.join(DATA_DIR, "predictions")

# config
CONFIG_DIR = os.path.join(ROOT_PATH, "src", "config")
MODELS_FPATH = os.path.join(CONFIG_DIR, "models.csv")
DATASETS_FPATH = os.path.join(CONFIG_DIR, "datasets.csv")

# outputs
RESULTS_DIR = os.path.join(ROOT_PATH, "results")
CHARTS_DIR = os.path.join(RESULTS_DIR, "charts")
METRICS_DIR = os.path.join(RESULTS_DIR, "metrics")


# output files
METRICS_FPATH = os.path.join(METRICS_DIR, "all_metrics.csv")
OVERALL_METRICS_FPATH = os.path.join(METRICS_DIR, "overall_metric_summary.csv")
BY_MODEL_METRICS_FPATH = os.path.join(METRICS_DIR, "by_model_metric_summary.csv")
BY_DATASET_METRICS_FPATH = os.path.join(METRICS_DIR, "by_dataset_metric_summary.csv")
BY_MODEL_DATASET_METRICS_FPATH = os.path.join(
    METRICS_DIR, "by_model_dataset_metric_summary.csv"
)

WHICH_IS_BETTER_CHART_FPATH = os.path.join(CHARTS_DIR, "better_scenario.png")
BAR_CHART_FPATH = os.path.join(CHARTS_DIR, "bar_chart.png")
DATASET_IMPACT_CHART = os.path.join(CHARTS_DIR, "dataset_impact.png")
MODEL_IMPACT_CHART = os.path.join(CHARTS_DIR, "model_impact.png")


# logs
LOGS_DIR = os.path.join(RESULTS_DIR, "logs")
METRICS_CALCULATION_LOG_FPATH = os.path.join(LOGS_DIR, "metrics_calculation.log")
