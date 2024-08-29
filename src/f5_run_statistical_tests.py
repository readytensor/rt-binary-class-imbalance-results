import os
import itertools
import pandas as pd
from config import paths
from config.variables import metrics as metrics_dict
from scipy.stats import ttest_rel
from statsmodels.stats.anova import AnovaRM


def run_anova(
    metrics_df: pd.DataFrame, save_file_path: str = paths.ANOVA_RESULTS_FPATH
) -> pd.DataFrame:
    print("Running ANOVA test...")
    metrics = metrics_df.copy()
    metrics["Dataset"] = metrics["Dataset_Fold"].str.split("_").str[0]
    ordered_metrics = [metric["name"] for metric in metrics_dict]

    metrics = (
        metrics.groupby(["Scenario", "Dataset", "Model"])[ordered_metrics]
        .mean()
        .reset_index()
    )

    metrics = (
        metrics.groupby(["Scenario", "Dataset"])[ordered_metrics].mean().reset_index()
    )

    metrics = metrics.melt(
        id_vars=["Scenario", "Dataset"], var_name="Metric", value_name="Value"
    )

    metrics.columns = ["group", "subject", "metric", "value"]

    unique_metrics = metrics["metric"].unique()
    anova_results = {"metric": [], "P-Value": []}
    for metric in unique_metrics:
        data_subset = metrics[metrics["metric"] == metric]
        model = AnovaRM(
            data=data_subset, depvar="value", subject="subject", within=["group"]
        )
        res = model.fit()
        anova_results["metric"].append(metric)
        anova_results["P-Value"].append(res.anova_table["Pr > F"].iloc[0])

    anova_results = pd.DataFrame(anova_results)
    anova_results["P-Value"] = anova_results["P-Value"]
    anova_results.to_csv(save_file_path, index=False)
    print("ANOVA test results saved to", save_file_path)
    return anova_results


def run_paired_t_tests(
    metrics_df: pd.DataFrame, save_dir_path: str = paths.STATISTICAL_TESTS_DIR
) -> pd.DataFrame:
    print("Running paired t-tests...")
    metrics = metrics_df.copy()
    metrics["Dataset"] = metrics["Dataset_Fold"].str.split("_").str[0]
    ordered_metrics = [metric["name"] for metric in metrics_dict]

    metrics = (
        metrics.groupby(["Scenario", "Dataset", "Model"])[ordered_metrics]
        .mean()
        .reset_index()
    )

    metrics = (
        metrics.groupby(["Scenario", "Dataset"])[ordered_metrics].mean().reset_index()
    )

    metrics = metrics.melt(
        id_vars=["Scenario", "Dataset"], var_name="Metric", value_name="Value"
    )

    metrics = metrics.pivot_table(
        index="Dataset", columns=["Scenario", "Metric"], values="Value", aggfunc="mean"
    )

    groups = metrics.columns.levels[0]
    unique_metrics = metrics.columns.levels[1]
    results_dict = {}

    for metric in unique_metrics:
        pairs = list(itertools.combinations(groups, 2))
        t_stat_matrix = pd.DataFrame(index=groups, columns=groups)
        p_value_matrix = pd.DataFrame(index=groups, columns=groups)
        for pair in pairs:
            group1, group2 = pair
            t_stat, p_value = ttest_rel(
                metrics[group1][metric], metrics[group2][metric]
            )
            t_stat_matrix.loc[group1, group2] = t_stat
            t_stat_matrix.loc[group2, group1] = "-"

            p_value_matrix.loc[group1, group2] = p_value
            p_value_matrix.loc[group2, group1] = "-"

        p_value_matrix = p_value_matrix.fillna("-")
        t_stat_matrix = t_stat_matrix.fillna("-")

        p_value_matrix = p_value_matrix.drop(p_value_matrix.columns[0], axis=1)
        t_stat_matrix = t_stat_matrix.drop(t_stat_matrix.columns[0], axis=1)

        results_dict[metric] = {
            "t_stat_matrix": t_stat_matrix,
            "p_value_matrix": p_value_matrix,
        }

    for metric, results in results_dict.items():
        metric_dir_path = os.path.join(save_dir_path, "ttest", metric)
        os.makedirs(metric_dir_path, exist_ok=True)
        results["t_stat_matrix"].to_csv(f"{metric_dir_path}/t_stat.csv")
        results["p_value_matrix"].to_csv(f"{metric_dir_path}/p_value.csv")

    print("Paired t-test results saved to", save_dir_path)


def run_statistical_tests() -> None:
    metrics = pd.read_csv(paths.METRICS_FPATH)
    run_anova(metrics)
    run_paired_t_tests(metrics)


if __name__ == "__main__":
    run_statistical_tests()
