from f1_calculate_metrics import calculate_metrics
from f2_summarize_metrics import summarize_metrics
from f3_create_table_svgs import generate_table_svgs
from f4_create_charts import create_charts
from f5_run_statistical_tests import run_statistical_tests


if __name__ == "__main__":
    calculate_metrics()
    summarize_metrics()
    generate_table_svgs()
    create_charts()
    run_statistical_tests()
