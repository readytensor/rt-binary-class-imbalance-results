# rt-smote-project-results

## Project Description

This project delves into the analysis of model performance on imbalanced datasets, specifically investigating the impact of the Synthetic Minority Over-sampling Technique (SMOTE) against scenarios where it is not applied. Given the challenges of imbalanced datasets in machine learning, especially in classification tasks where the distribution of classes is skewed, effective techniques like SMOTE are often considered to balance the scales and potentially improve model performance.

### Objective

The primary goal is to compare and evaluate how different models perform on binary classification imbalanced datasets when SMOTE is applied versus when it isn't.

### Methods

Various models were trained on several imbalanced datasets, both with and without applying SMOTE. Performance metrics such as accuracy, precision, recall, F1-score, and AUC were captured and analyzed.

### Key Findings

The preliminary analysis revealed variations in recall and precision between the two scenarios. Some models showed marked improvement with SMOTE, while others did not.

### Significance

Understanding the impact of techniques like SMOTE is crucial for practitioners dealing with imbalanced data. This project provides insights into when and where SMOTE might be most beneficial.

---

## Project Structure

The following is the directory structure of the project:

- **`data/`**: This directory contains files for the datasets used in the project. Three files are included:
  - **`SMOTE project datasets.csv`**: This file contains information about the datasets used in tha analysis.
  - **`Imbalanced datasets SMOTE results.csv`**: This file contains the results of running multiple benchmarks on the datasets with and without applying SMOTE.
  - **`license`**: This file contains the license for the data.
- **`results/`**: This directory contains the result of running the Jupyter notebook.
  - **`figure/`**: This directory contains figures generated by the project code.
  - **`paired t-test results.csv`**: This file contains results of the paired t-test.
- **`.gitignore`**: This file specifies the files and folders that should be ignored by Git.
- **`license`**: This file contains the license for the project code.
- **`README.md`**: This file (this particular document) contains the documentation for the project.
- **`requirements.txt`**: This file contains the requirements for running the project.
- **`SMOTE_analysis.ipynb`**: This notebook contains the code for the analysis and the results.

## Table of Contents (**`SMOTE_analysis.ipynb`**)

1. **[Imports](#imports)**: Setting up the required libraries.
2. **[Reading the Data](#reading-the-data)**: Loading the datasets for analysis.
3. **[Percentage Analysis](#percentage-analysis)**: Analyzing the percentage of models that perform better for each scenario.
4. **[Dataset-wise Analysis](#dataset-wise-analysis)**: Evaluating the percentage of models that outperform for each scenario, broken down by dataset.
5. **[Observations](#observations)**: Key insights derived from the above analyses.
6. **[Distribution of Differences](#distribution-of-differences)**: Checking the distribution of differences in results for each metric.
7. **[Statistical Tests](#statistical-tests)**: Performing paired t-tests to ascertain the significance of observed differences.
8. **[Visual Analysis](#visual-analysis)**: Employing box plots and bar charts to visualize the direction of change in results.
9. **[Conclusions](#conclusions)**: Summarizing the findings and drawing conclusions.

## Classifiers used for analysis:

1. [rt_bin_class_adaboost_sklearn](https://github.com/readytensor/rt_bin_class_adaboost_sklearn)
2. [rt_bin_class_catboost](https://github.com/readytensor/rt_bin_class_catboost)
3. [rt_bin_class_decision_tree_sklearn](https://github.com/readytensor/rt_bin_class_decision_tree_sklearn)
4. [rt_bin_class_ebm_interpretml](https://github.com/readytensor/rt_bin_class_ebm_interpretml)
5. [rt_bin_class_extra_trees_sklearn](https://github.com/readytensor/rt_bin_class_extra_trees_sklearn)
6. [rt_bin_class_knn_sklearn](https://github.com/readytensor/rt_bin_class_knn_sklearn)
7. [rt_bin_class_lightgbm](https://github.com/readytensor/rt_bin_class_lightgbm)
8. [rt_bin_class_logistic_regression_sklearn](https://github.com/readytensor/rt_bin_class_logistic_regression_sklearn)
9. [rt_bin_class_mlp_sklearn](https://github.com/readytensor/rt_bin_class_mlp_sklearn)
10. [rt_bin_class_naive_bayes_sklearn](https://github.com/readytensor/rt_bin_class_naive_bayes_sklearn)
11. [rt_bin_class_rf_hyperopt](https://github.com/readytensor/rt_bin_class_rf_hyperopt)
12. [rt_bin_class_simple_ann_pt_cpu](https://github.com/readytensor/rt_bin_class_simple_ann_pt_cpu)
13. [t_bin_class_stacking_sklearn](https://github.com/readytensor/rt_bin_class_stacking_sklearn)
14. [rt_bin_class_svc_sklearn](https://github.com/readytensor/rt_bin_class_svc_sklearn)
15. [rt_bin_class_xgboost](https://github.com/readytensor/rt_bin_class_xgboost)

## LICENSE

The code in this repository is licensed under the MIT License. See [license](license) for details.
The data in this repository is dedicated to the public domain under CC0 1.0 Universal. See `data/license`(./data/license)for details.
This project is provided under the MIT License. Please see the file for more information.

## Contact Information

Repository created by Ready Tensor, Inc. (https://www.readytensor.ai/)
