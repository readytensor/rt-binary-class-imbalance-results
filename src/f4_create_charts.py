from config import paths
import pandas as pd
from charts.bar_chart import create_bar_chart

from charts.better_scenario import (
    create_which_is_better_chart,
    create_scenario_impact_chart,
)


def create_charts():
    metrics = pd.read_csv(paths.METRICS_FPATH)
    create_bar_chart(metrics, paths.BAR_CHART_FPATH)
    create_which_is_better_chart(metrics, paths.WHICH_IS_BETTER_CHART_FPATH)
    create_scenario_impact_chart(metrics, paths.DATASET_IMPACT_CHART, by="Dataset")
    create_scenario_impact_chart(metrics, paths.MODEL_IMPACT_CHART, by="Model")


if __name__ == "__main__":
    create_charts()
