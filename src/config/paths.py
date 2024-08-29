import os

f_path = os.path.abspath(__file__)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(f_path)))

# input data
DATA_DIR = os.path.join(ROOT_PATH, "data")
DATASETS_DIR = os.path.join(DATA_DIR, "datasets")
PREDICTIONS_DIR = os.path.join(DATA_DIR, "predictions")
ZIPPED_DATASETS_FILE = os.path.join(DATA_DIR, "datasets.zip")
ZIPPED_PREDICTIONS_FILE = os.path.join(DATA_DIR, "predictions.zip")


# config
CONFIG_DIR = os.path.join(ROOT_PATH, "src", "config")
MODELS_FPATH = os.path.join(CONFIG_DIR, "models.csv")
DATASETS_FPATH = os.path.join(CONFIG_DIR, "datasets.csv")

# output directories
RESULTS_DIR = os.path.join(ROOT_PATH, "results")
CHARTS_DIR = os.path.join(RESULTS_DIR, "charts")
METRICS_DIR = os.path.join(RESULTS_DIR, "metrics")
STATISTICAL_TESTS_DIR = os.path.join(RESULTS_DIR, "statistical_tests")


# output files

# raw metrics
METRICS_FPATH = os.path.join(METRICS_DIR, "all_metrics.csv")

# summarized metrics
OVERALL_METRICS_FPATH = os.path.join(METRICS_DIR, "overall_metrics_summary.csv")
BY_MODEL_METRICS_FPATH = os.path.join(METRICS_DIR, "by_model_metrics_summary.csv")
BY_DATASET_METRICS_FPATH = os.path.join(METRICS_DIR, "by_dataset_metrics_summary.csv")
BY_MODEL_DATASET_METRICS_FPATH = os.path.join(
    METRICS_DIR, "by_model_dataset_metrics_summary.csv"
)

# pivoted tables
# pivoted summarized metrics
OVERALL_PIVOTED_METRICS_FPATH = os.path.join(
    METRICS_DIR, "overall_metrics_summary_pivoted.csv"
)
BY_MODEL_PIVOTED_METRICS_FPATH = os.path.join(
    METRICS_DIR, "by_model_metrics_summary_pivoted.csv"
)
BY_DATASET_PIVOTED_METRICS_FPATH = os.path.join(
    METRICS_DIR, "by_dataset_metrics_summary_pivoted.csv"
)
BY_MODEL_DATASET_PIVOTED_METRICS_FPATH = os.path.join(
    METRICS_DIR, "by_model_dataset_metrics_summary_pivoted.csv"
)

# Charts
OVERALL_RESULTS_TABLE_SVG = os.path.join(CHARTS_DIR, "overall_metrics.svg")
BY_METRIC_SVG_RESULTS_DIR = os.path.join(CHARTS_DIR, "by_metric")


WHICH_IS_BETTER_CHART_FPATH = os.path.join(CHARTS_DIR, "better_scenario.png")
BAR_CHART_FPATH = os.path.join(CHARTS_DIR, "bar_chart.png")
DATASET_IMPACT_CHART = os.path.join(CHARTS_DIR, "dataset_impact.png")
MODEL_IMPACT_CHART = os.path.join(CHARTS_DIR, "model_impact.png")

# Statistical tests
ANOVA_RESULTS_FPATH = os.path.join(STATISTICAL_TESTS_DIR, "anova_results.csv")
TTEST_RESULTS_FPATH = os.path.join(STATISTICAL_TESTS_DIR, "ttest_results.csv")


# logs
LOGS_DIR = os.path.join(RESULTS_DIR, "logs")
METRICS_CALCULATION_LOG_FPATH = os.path.join(LOGS_DIR, "metrics_calculation.log")
