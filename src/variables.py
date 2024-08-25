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
        "smote": "#FF9B61",
        "class_weights": "#5BC8A0",
        "decision_threshold": "#5BC8A0",
        "tie": "#B3BEC4",
    },
    "ordered_models": [
        "naive_bayes",
        "logistic_regression",
        "k_nearest_neighbors",
        "adaboost",
        "decision_tree",
        "support_vector_classifier",
        "artificial_neural_network",
        "multi_layer_perceptron",
        "explainable_boosting_machine",
        "extra_trees",
        "random_forest",
        "stacking_classifier",
        "catboost",
        "lightgbm",
        "xgboost",
    ],
}
