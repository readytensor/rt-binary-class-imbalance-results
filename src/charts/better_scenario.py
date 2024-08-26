import pandas as pd
import matplotlib.pyplot as plt
from config.variables import chart_cfg, apply_chart_cfg
from utils import prepare_data


def classify_comparison(row):
    smote_val = row["smote"]
    original_val = row["baseline"]
    threshold_val = row["decision_threshold"]
    class_weights_val = row["class_weights"]

    maxx = max(smote_val, original_val, threshold_val, class_weights_val)
    if (
        maxx == smote_val
        and maxx == original_val
        and maxx == threshold_val
        and maxx == class_weights_val
    ):
        return "tie"
    elif maxx == smote_val:
        return "smote_is_better"
    elif maxx == original_val:
        return "baseline_is_better"
    elif maxx == threshold_val:
        return "decision_threshold_is_better"
    elif maxx == class_weights_val:
        return "class_weights_is_better"


def create_which_is_better_chart(metrics_df: pd.DataFrame, save_fig_path: str) -> None:
    metrics = metrics_df.copy()
    metrics = prepare_data(metrics)
    metrics["comparison"] = metrics.apply(lambda row: classify_comparison(row), axis=1)

    comparison_columns = [
        "baseline_is_better",
        "class_weights_is_better",
        "decision_threshold_is_better",
        "smote_is_better",
        "tie",
    ]
    comparison_counts = (
        metrics.groupby("metric")["comparison"]
        .value_counts(normalize=True)
        .unstack()
        .loc[chart_cfg["ordered_metrics"]]
    )

    comparison_counts = comparison_counts[comparison_columns]

    # Create sub-plots with 5 columns (one for each metric) and 1 row
    fig, axes = plt.subplots(1, 5, figsize=(16, 3), sharey=True)

    # Plot each subplot
    for ax, metric in zip(axes, chart_cfg["ordered_metrics"]):
        comparison_counts.loc[[metric]][comparison_columns].plot(
            kind="barh",
            stacked=True,
            color=chart_cfg["colors"].values(),
            ax=ax,
            legend=False,
            width=0.6,
        )
        ax.set_title(
            metric, fontsize=chart_cfg["title_font_size"], color=chart_cfg["font_color"]
        )
        # ax.set_xlabel('Percentage', fontsize=chart_cfg['xlabel_font_size'], color=chart_cfg['font_color'])
        ax.tick_params(
            axis="x",
            colors=chart_cfg["font_color"],
            labelsize=chart_cfg["tick_font_size"],
        )
        ax.tick_params(
            axis="y",
            colors=chart_cfg["font_color"],
            labelsize=chart_cfg["tick_font_size"],
        )
        ax.set_xlim(0, 1)
        ax.xaxis.set_major_formatter(lambda x, _: f"{100*x:.0f}%")
        apply_chart_cfg(ax)
        ax.set_ylabel("")
        ax.set_yticklabels("")

        # Annotate each stack with its value
        for p in ax.patches:
            width = p.get_width()
            if width > 0.25:  # Displaying percentage only if it's greater than 25%
                ax.annotate(
                    f"{width*100:.1f}%",
                    (p.get_x() + width / 2, p.get_y() + p.get_height() / 2),
                    ha="center",
                    va="center",
                    color="#444444",
                    fontsize=10,
                )

    plt.suptitle(
        "% Times When Smote vs original is Better",
        fontsize=chart_cfg["title_font_size"],
        color=chart_cfg["font_color"],
    )

    # Adjust layout and show the plot
    legend = axes[4].legend(
        #         title='Scenario',
        bbox_to_anchor=(1.0, 0.85),
        facecolor="none",
        edgecolor="none",
        fontsize=12,
        title_fontsize=chart_cfg["tick_font_size"],
        #         color='#ccc'
    )

    # Set font color for the legend text
    for text in legend.get_texts():
        text.set_color(chart_cfg["legend_font_color"])
        text.set_fontsize(chart_cfg["legend_font_size"])
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.35)

    plt.savefig(save_fig_path)


def create_scenario_impact_chart(
    metrics_df: pd.DataFrame, save_fig_path: str, by: str = "model"
) -> None:
    metrics = metrics_df.copy()
    metrics = prepare_data(metrics)
    metrics["dataset"] = metrics["dataset"].str.replace(r"_fold_\d+", "", regex=True)
    metrics = metrics.groupby(["dataset", "model", "metric"]).mean().reset_index()
    datasets = metrics["dataset"].unique()

    metrics["comparison"] = metrics.apply(lambda row: classify_comparison(row), axis=1)

    comparison_counts_model = (
        metrics.groupby(["metric", by])["comparison"]
        .value_counts(normalize=True)
        .unstack()
        .fillna(0)
    )
    comparison_columns = [
        "baseline_is_better",
        "class_weights_is_better",
        "decision_threshold_is_better",
        "smote_is_better",
        "tie",
    ]

    # Create sub-plots with 5 columns (one for each metric) and 1 row
    fig, axes = plt.subplots(1, 5, figsize=(20, 10), sharey=True)

    for col, metric in enumerate(chart_cfg["ordered_metrics"]):
        ax = axes[col]
        df = comparison_counts_model.loc[metric]

        if by == "dataset":
            df = df.reindex(datasets[::-1])

        elif by == "model":
            df.index = df.index.map(chart_cfg["ordered_models"])
            df = df.reindex(list(chart_cfg["ordered_models"].values())[::-1])

        df[comparison_columns].plot(
            kind="barh",
            stacked=True,
            ax=ax,
            color=chart_cfg["colors"].values(),
            legend=False,
            width=0.6,
        )
        ax.set_xlim(0, 1)
        ax.set_title(
            metric, fontsize=chart_cfg["title_font_size"], color=chart_cfg["font_color"]
        )
        ax.xaxis.set_major_formatter(lambda x, _: f"{100*x:.0f}%")
        ax.tick_params(
            axis="x",
            colors=chart_cfg["font_color"],
            labelsize=chart_cfg["tick_font_size"],
        )
        ax.tick_params(
            axis="y",
            colors=chart_cfg["font_color"],
            labelsize=chart_cfg["tick_font_size"],
        )
        apply_chart_cfg(ax)

    if by == "model":
        title = "Different Scenarios' Impact on Algorithm Performance"
    elif by == "dataset":
        title = "Different Scenarios' Impact on Dataset Performance"

    plt.suptitle(
        title,
        fontsize=chart_cfg["title_font_size"],
        color=chart_cfg["font_color"],
    )

    # Adjust layout and show the plot
    legend = axes[2].legend(
        title="Impact",
        bbox_to_anchor=(0.0, -0.15),
        loc="lower center",
        facecolor="none",
        edgecolor="none",
        fontsize=chart_cfg["tick_font_size"],
        title_fontsize=chart_cfg["tick_font_size"],
        ncol=3,
    )
    # Set font color for the legend text
    for text in legend.get_texts():
        text.set_color(chart_cfg["legend_font_color"])
        text.set_fontsize(chart_cfg["legend_font_size"])
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.savefig(save_fig_path)
