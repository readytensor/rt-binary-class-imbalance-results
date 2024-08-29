import pandas as pd
import matplotlib.pyplot as plt
from .chart_utils import apply_chart_cfg
from config.variables import metrics as metrics_dict, ordered_scenarios
from config.chart_cfg import *
from utils import prepare_data_for_visualization


def create_bar_chart(metrics_df: pd.DataFrame, save_fig_path: str) -> None:
    metrics = metrics_df.copy()
    metrics = prepare_data_for_visualization(metrics)

    metrics["fold_number"] = metrics["Dataset_Fold"].str.split("_").str[-1].astype(int)
    avg_metrics = metrics.groupby(["Metric", "fold_number"])[ordered_scenarios].mean()

    avg_metrics = avg_metrics.groupby("Metric").mean()
    ordered_metrics = [metric["name"] for metric in metrics_dict]
    avg_metrics = avg_metrics.reindex(ordered_metrics)
    ordered_colors = [colors[k] for k in ordered_scenarios]

    plt.figure(figsize=(16, 6))
    ax = avg_metrics.plot(
        kind="bar",
        color=ordered_colors,
        figsize=(16, 8),
    )

    # Annotating bars with their rounded values
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.2f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(1, 5),
            textcoords="offset points",
            fontsize=10,
            color=font_color,
        )

    plt.title("Average Metric Values for Different Scenarios")
    plt.ylabel("Average Value")
    plt.xlabel("Metric")
    legend = plt.legend(facecolor="none", edgecolor="none", fontsize=tick_font_size)
    plt.setp(legend.get_texts(), color=legend_font_color)
    plt.xticks(rotation=45)
    apply_chart_cfg(plt.gca())
    plt.tight_layout()
    plt.savefig(save_fig_path)
