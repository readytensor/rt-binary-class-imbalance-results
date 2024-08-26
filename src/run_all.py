from config import paths
from utils import read_csv_as_df
from f1_calculate_metrics import calculate_metrics
from f2_metrics_summary import summarize_metrics
from f3_create_charts import create_charts


if __name__ == "__main__":
    models_df = read_csv_as_df(paths.MODELS_FPATH)
    datasets_df = read_csv_as_df(paths.DATASETS_FPATH)
    calculate_metrics(models_df, datasets_df)
    summarize_metrics()
    create_charts()
