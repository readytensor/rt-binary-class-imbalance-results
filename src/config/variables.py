"""This module contains the variables used in the project."""

scenarios = [
    "baseline",
    "smote",
    "class_weights",
    "decision_threshold",
]

metrics = [
    "accuracy",
    "auc_score",
    "pr_auc_score",
    "precision",
    "recall",
    "f1_score",
    "f2_score",
]

# chart config
chart_cfg = {
    "border_visible": False,
    "transparency": True,
    "title_font_size": 20,
    "xlabel_font_size": 16,
    "ylabel_font_size": 16,
    "tick_font_size": 12,
    "font_color": "#000000",
    "legend_font_color": "#000000",
    "legend_font_size": 16,
    "colors": {
        "baseline": "#7986CB",
        "class_weights": "#f5b507",
        "decision_threshold": "#5BC8A0",
        "smote": "#FF9B61",
        "tie": "#B3BEC4",
    },
    "ordered_models": {
        "rt_bin_class_adaboost_sklearn": "AdaBoost",
        "rt_bin_class_bagging_sklearn": "Bagging Classifier",
        "rt_bin_class_decision_tree_sklearn": "Decision Tree",
        "rt_bin_class_extra_trees_sklearn": "Extra Trees",
        "rt_bin_class_gradient_boosting_sklearn": "Gradient Boosting",
        "rt_bin_class_lightgbm": "LightGBM",
        "rt_bin_class_logistic_regression_sklearn": "Logistic Regression",
        "rt_bin_class_rf_hyperopt": "Random Forest",
        "rt_bin_class_simple_ann_pt_gpu": "Simple ANN",
        "rt_bin_class_svc_sklearn": "SVM",
        "rt_bin_class_xgboost": "XGBoost",
    },
    "ordered_metrics": ["accuracy", "auc_score", "precision", "recall", "f1_score"],
}


def apply_chart_cfg(ax):
    ax.spines["top"].set_visible(chart_cfg["border_visible"])
    ax.spines["right"].set_visible(chart_cfg["border_visible"])
    ax.spines["bottom"].set_visible(chart_cfg["border_visible"])
    ax.spines["left"].set_visible(chart_cfg["border_visible"])

    ax.set_facecolor("none")

    ax.set_title(
        ax.get_title(),
        color=chart_cfg["font_color"],
        fontsize=chart_cfg["title_font_size"],
    )
    ax.set_xlabel(
        ax.get_xlabel(),
        color=chart_cfg["font_color"],
        fontsize=chart_cfg["xlabel_font_size"],
    )
    ax.set_ylabel(
        ax.get_ylabel(),
        color=chart_cfg["font_color"],
        fontsize=chart_cfg["ylabel_font_size"],
    )

    ax.tick_params(
        axis="x", colors=chart_cfg["font_color"], labelsize=chart_cfg["tick_font_size"]
    )
    ax.tick_params(
        axis="y", colors=chart_cfg["font_color"], labelsize=chart_cfg["tick_font_size"]
    )

    if chart_cfg["transparency"]:
        ax.patch.set_alpha(0)
