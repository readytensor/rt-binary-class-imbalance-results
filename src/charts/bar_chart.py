import pandas as pd
import matplotlib.pyplot as plt
from config.variables import chart_cfg, apply_chart_cfg
from utils import prepare_data


def create_bar_chart(metrics_df: pd.DataFrame, save_fig_path: str) -> None:
    metrics = metrics_df.copy()
    metrics = prepare_data(metrics)

    avg_metrics = metrics.groupby(["metric", "fold_number"])[
        ["baseline", "class_weights", "decision_threshold", "smote"]
    ].mean()

    avg_metrics = avg_metrics.groupby("metric").mean()
    avg_metrics = avg_metrics.reindex(chart_cfg["ordered_metrics"])

    plt.figure(figsize=(16, 6))
    ax = avg_metrics.plot(
        kind="bar",
        color=[
            chart_cfg["colors"]["baseline"],
            chart_cfg["colors"]["class_weights"],
            chart_cfg["colors"]["decision_threshold"],
            chart_cfg["colors"]["smote"],
        ],
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
            color=chart_cfg["font_color"],
        )

    plt.title("Average Metric Values for Different Scenarios")
    plt.ylabel("Average Value")
    plt.xlabel("Metric")
    legend = plt.legend(
        facecolor="none", edgecolor="none", fontsize=chart_cfg["tick_font_size"]
    )
    plt.setp(legend.get_texts(), color=chart_cfg["legend_font_color"])
    plt.xticks(rotation=45)
    apply_chart_cfg(plt.gca())
    plt.tight_layout()
    plt.savefig(save_fig_path)
