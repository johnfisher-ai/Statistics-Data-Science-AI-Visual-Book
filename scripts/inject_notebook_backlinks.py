#!/usr/bin/env python3
"""Inject a styled "Back to the book" card into the rendered notebook HTML pages.

Run AFTER `nbconvert`. The card is added only to the View-Notebook HTML (which opens
in the same browser tab) — NOT to the .ipynb files (those open in their own Colab tab,
so they need no back-link). Wired into both scripts/build_notebook_html.sh and the
GitHub Actions deploy workflow so it survives every re-render.

Add a chapter's notebooks to MAP as they ship.
"""
import os

HTML_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chapters", "notebooks", "html")

# notebook-html filename -> (relative href to the chapter section, kicker, title)
MAP = {
    "what-is-machine-learning.html":
        ("../../what-is-machine-learning.html#notebook", "Back to the book", "Chapter 104 · What Is Machine Learning?"),
    "what-is-machine-learning--solutions.html":
        ("../../what-is-machine-learning.html#quiz", "Back to the book", "Chapter 104 · Take the quiz &amp; aim for 100%"),
    "the-machine-learning-workflow.html":
        ("../../the-machine-learning-workflow.html#notebook", "Back to the book", "Chapter 105 · The Machine Learning Workflow"),
    "the-machine-learning-workflow--solutions.html":
        ("../../the-machine-learning-workflow.html#quiz", "Back to the book", "Chapter 105 · Take the quiz &amp; aim for 100%"),
    "distance-metrics.html":
        ("../../distance-metrics.html#notebook", "Back to the book", "Chapter 106 · Distance Metrics"),
    "distance-metrics--solutions.html":
        ("../../distance-metrics.html#quiz", "Back to the book", "Chapter 106 · Take the quiz &amp; aim for 100%"),
    "core-classification-and-regression-algorithms.html":
        ("../../core-classification-and-regression-algorithms.html#notebook", "Back to the book", "Chapter 107 · Core Classification &amp; Regression Algorithms"),
    "core-classification-and-regression-algorithms--solutions.html":
        ("../../core-classification-and-regression-algorithms.html#quiz", "Back to the book", "Chapter 107 · Take the quiz &amp; aim for 100%"),
    "ensemble-methods.html":
        ("../../ensemble-methods.html#notebook", "Back to the book", "Chapter 108 · Ensemble Methods"),
    "ensemble-methods--solutions.html":
        ("../../ensemble-methods.html#quiz", "Back to the book", "Chapter 108 · Take the quiz &amp; aim for 100%"),
    "feature-selection.html":
        ("../../feature-selection.html#notebook", "Back to the book", "Chapter 109 · Feature Selection"),
    "feature-selection--solutions.html":
        ("../../feature-selection.html#quiz", "Back to the book", "Chapter 109 · Take the quiz &amp; aim for 100%"),
    "optimization-and-gradient-descent.html":
        ("../../optimization-and-gradient-descent.html#notebook", "Back to the book", "Chapter 110 · Optimization &amp; Gradient Descent"),
    "optimization-and-gradient-descent--solutions.html":
        ("../../optimization-and-gradient-descent.html#quiz", "Back to the book", "Chapter 110 · Take the quiz &amp; aim for 100%"),
    "model-evaluation.html":
        ("../../model-evaluation.html#notebook", "Back to the book", "Chapter 111 · Model Evaluation"),
    "model-evaluation--solutions.html":
        ("../../model-evaluation.html#quiz", "Back to the book", "Chapter 111 · Take the quiz &amp; aim for 100%"),
    "model-pitfalls.html":
        ("../../model-pitfalls.html#notebook", "Back to the book", "Chapter 112 · Model Pitfalls"),
    "model-pitfalls--solutions.html":
        ("../../model-pitfalls.html#quiz", "Back to the book", "Chapter 112 · Take the quiz &amp; aim for 100%"),
    "model-interpretability-and-explainability.html":
        ("../../model-interpretability-and-explainability.html#notebook", "Back to the book", "Chapter 113 · Model Interpretability &amp; Explainability"),
    "model-interpretability-and-explainability--solutions.html":
        ("../../model-interpretability-and-explainability.html#quiz", "Back to the book", "Chapter 113 · Take the quiz &amp; aim for 100%"),
    "clustering.html":
        ("../../clustering.html#notebook", "Back to the book", "Chapter 114 · Clustering"),
    "clustering--solutions.html":
        ("../../clustering.html#quiz", "Back to the book", "Chapter 114 · Take the quiz &amp; aim for 100%"),
    "dimensionality-reduction.html":
        ("../../dimensionality-reduction.html#notebook", "Back to the book", "Chapter 115 · Dimensionality Reduction"),
    "dimensionality-reduction--solutions.html":
        ("../../dimensionality-reduction.html#quiz", "Back to the book", "Chapter 115 · Take the quiz &amp; aim for 100%"),
    "association-rule-mining.html":
        ("../../association-rule-mining.html#notebook", "Back to the book", "Chapter 116 · Association Rule Mining"),
    "association-rule-mining--solutions.html":
        ("../../association-rule-mining.html#quiz", "Back to the book", "Chapter 116 · Take the quiz &amp; aim for 100%"),
    "anomaly-detection.html":
        ("../../anomaly-detection.html#notebook", "Back to the book", "Chapter 117 · Anomaly Detection"),
    "anomaly-detection--solutions.html":
        ("../../anomaly-detection.html#quiz", "Back to the book", "Chapter 117 · Take the quiz &amp; aim for 100%"),
    "reinforcement-learning-primer.html":
        ("../../reinforcement-learning-primer.html#notebook", "Back to the book", "Chapter 118 · Reinforcement Learning Primer"),
    "reinforcement-learning-primer--solutions.html":
        ("../../reinforcement-learning-primer.html#quiz", "Back to the book", "Chapter 118 · Take the quiz &amp; aim for 100%"),
    "deep-rl-and-applications.html":
        ("../../deep-rl-and-applications.html#notebook", "Back to the book", "Chapter 119 · Deep RL &amp; Applications"),
    "deep-rl-and-applications--solutions.html":
        ("../../deep-rl-and-applications.html#quiz", "Back to the book", "Chapter 119 · Take the quiz &amp; aim for 100%"),
    "case-study-an-end-to-end-ml-project.html":
        ("../../case-study-an-end-to-end-ml-project.html#notebook", "Back to the book", "Chapter 120 · An End-to-End ML Project"),
    "case-study-an-end-to-end-ml-project--take-it-further.html":
        ("../../case-study-an-end-to-end-ml-project.html#challenges", "Back to the book", "Chapter 120 · Take it further"),
    "case-study-fraud-detection.html":
        ("../../case-study-fraud-detection.html#notebook", "Back to the book", "Chapter 121 · Fraud Detection"),
    "case-study-fraud-detection--take-it-further.html":
        ("../../case-study-fraud-detection.html#challenges", "Back to the book", "Chapter 121 · Take it further"),
    "case-study-predictive-maintenance.html":
        ("../../case-study-predictive-maintenance.html#notebook", "Back to the book", "Chapter 122 · Predictive Maintenance"),
    "case-study-predictive-maintenance--take-it-further.html":
        ("../../case-study-predictive-maintenance.html#challenges", "Back to the book", "Chapter 122 · Take it further"),
    "case-study-customer-segmentation-and-targeting.html":
        ("../../case-study-customer-segmentation-and-targeting.html#notebook", "Back to the book", "Chapter 123 · Customer Segmentation &amp; Targeting"),
    "case-study-customer-segmentation-and-targeting--take-it-further.html":
        ("../../case-study-customer-segmentation-and-targeting.html#challenges", "Back to the book", "Chapter 123 · Take it further"),
    "case-study-loan-default-risk.html":
        ("../../case-study-loan-default-risk.html#notebook", "Back to the book", "Chapter 124 · Loan Default Risk"),
    "case-study-loan-default-risk--take-it-further.html":
        ("../../case-study-loan-default-risk.html#challenges", "Back to the book", "Chapter 124 · Take it further"),
    "case-study-from-model-to-decision.html":
        ("../../case-study-from-model-to-decision.html#notebook", "Back to the book", "Chapter 125 · From Model to Decision"),
    "case-study-from-model-to-decision--take-it-further.html":
        ("../../case-study-from-model-to-decision.html#challenges", "Back to the book", "Chapter 125 · Take it further"),
    "case-study-operationalizing-the-model-mlops.html":
        ("../../case-study-operationalizing-the-model-mlops.html#notebook", "Back to the book", "Chapter 126 · Operationalizing the Model"),
    "case-study-operationalizing-the-model-mlops--take-it-further.html":
        ("../../case-study-operationalizing-the-model-mlops.html#challenges", "Back to the book", "Chapter 126 · Take it further"),
    "components-of-a-time-series.html":
        ("../../components-of-a-time-series.html#notebook", "Back to the book", "Chapter 127 · Components of a Time Series"),
    "components-of-a-time-series--solutions.html":
        ("../../components-of-a-time-series.html#challenges", "Back to the book", "Chapter 127 · Challenge solutions"),
    "forecasting-models.html":
        ("../../forecasting-models.html#notebook", "Back to the book", "Chapter 128 · Forecasting Models"),
    "forecasting-models--solutions.html":
        ("../../forecasting-models.html#challenges", "Back to the book", "Chapter 128 · Challenge solutions"),
    "volatility-and-advanced-models.html":
        ("../../volatility-and-advanced-models.html#notebook", "Back to the book", "Chapter 129 · Volatility & Advanced Models"),
    "volatility-and-advanced-models--solutions.html":
        ("../../volatility-and-advanced-models.html#challenges", "Back to the book", "Chapter 129 · Challenge solutions"),
    "forecast-accuracy.html":
        ("../../forecast-accuracy.html#notebook", "Back to the book", "Chapter 130 · Forecast Accuracy"),
    "forecast-accuracy--solutions.html":
        ("../../forecast-accuracy.html#challenges", "Back to the book", "Chapter 130 · Challenge solutions"),
    "case-study-forecasting-retail-sales.html":
        ("../../case-study-forecasting-retail-sales.html#notebook", "Back to the book", "Chapter 131 · Forecasting Retail Sales"),
    "case-study-forecasting-retail-sales--take-it-further.html":
        ("../../case-study-forecasting-retail-sales.html#challenges", "Back to the book", "Chapter 131 · Take it further"),
    "case-study-financial-volatility-and-risk.html":
        ("../../case-study-financial-volatility-and-risk.html#notebook", "Back to the book", "Chapter 132 · Financial Volatility & Risk"),
    "case-study-financial-volatility-and-risk--take-it-further.html":
        ("../../case-study-financial-volatility-and-risk.html#challenges", "Back to the book", "Chapter 132 · Take it further"),
    "case-study-energy-demand-forecasting.html":
        ("../../case-study-energy-demand-forecasting.html#notebook", "Back to the book", "Chapter 133 · Energy Demand Forecasting"),
    "case-study-energy-demand-forecasting--take-it-further.html":
        ("../../case-study-energy-demand-forecasting.html#challenges", "Back to the book", "Chapter 133 · Take it further"),
    "case-study-from-forecast-to-decision.html":
        ("../../case-study-from-forecast-to-decision.html#notebook", "Back to the book", "Chapter 134 · From Forecast to Decision"),
    "case-study-from-forecast-to-decision--take-it-further.html":
        ("../../case-study-from-forecast-to-decision.html#challenges", "Back to the book", "Chapter 134 · Take it further"),
    "case-study-operationalizing-a-forecast.html":
        ("../../case-study-operationalizing-a-forecast.html#notebook", "Back to the book", "Chapter 135 · Operationalizing a Forecast"),
    "case-study-operationalizing-a-forecast--take-it-further.html":
        ("../../case-study-operationalizing-a-forecast.html#challenges", "Back to the book", "Chapter 135 · Take it further"),
    "case-study-designing-and-analyzing-a-survey.html":
        ("../../case-study-designing-and-analyzing-a-survey.html#notebook", "Back to the book", "Chapter 136 · Designing and Analyzing a Survey"),
    "case-study-designing-and-analyzing-a-survey--take-it-further.html":
        ("../../case-study-designing-and-analyzing-a-survey.html#challenges", "Back to the book", "Chapter 136 · Take it further"),
    "case-study-difference-in-differences.html":
        ("../../case-study-difference-in-differences.html#notebook", "Back to the book", "Chapter 137 · Difference-in-Differences"),
    "case-study-difference-in-differences--take-it-further.html":
        ("../../case-study-difference-in-differences.html#challenges", "Back to the book", "Chapter 137 · Take it further"),
    "case-study-a-paired-pre-post-study.html":
        ("../../case-study-a-paired-pre-post-study.html#notebook", "Back to the book", "Chapter 138 · A Paired Pre/Post Study"),
    "case-study-a-paired-pre-post-study--take-it-further.html":
        ("../../case-study-a-paired-pre-post-study.html#challenges", "Back to the book", "Chapter 138 · Take it further"),
    "case-study-customer-lifetime-value.html":
        ("../../case-study-customer-lifetime-value.html#notebook", "Back to the book", "Chapter 139 · Customer Lifetime Value"),
    "case-study-customer-lifetime-value--take-it-further.html":
        ("../../case-study-customer-lifetime-value.html#challenges", "Back to the book", "Chapter 139 · Take it further"),
    "case-study-forecasting-with-drivers.html":
        ("../../case-study-forecasting-with-drivers.html#notebook", "Back to the book", "Chapter 140 · Forecasting with Drivers"),
    "case-study-forecasting-with-drivers--take-it-further.html":
        ("../../case-study-forecasting-with-drivers.html#challenges", "Back to the book", "Chapter 140 · Take it further"),
    "case-study-multi-file-and-datetime-eda.html":
        ("../../case-study-multi-file-and-datetime-eda.html#notebook", "Back to the book", "Chapter 141 · Multi-File, Multi-Date EDA"),
    "case-study-multi-file-and-datetime-eda--take-it-further.html":
        ("../../case-study-multi-file-and-datetime-eda.html#challenges", "Back to the book", "Chapter 141 · Take it further"),
    "what-is-statistics.html":
        ("../../what-is-statistics.html#notebook", "Back to the book", "Chapter 1 · What Is Statistics?"),
    "what-is-statistics--solutions.html":
        ("../../what-is-statistics.html#quiz", "Back to the book", "Chapter 1 · Take the quiz &amp; aim for 100%"),
    "statistics-data-science-and-ai.html":
        ("../../statistics-data-science-and-ai.html#notebook", "Back to the book", "Chapter 2 · Statistics, Data Science &amp; AI"),
    "statistics-data-science-and-ai--solutions.html":
        ("../../statistics-data-science-and-ai.html#quiz", "Back to the book", "Chapter 2 · Take the quiz &amp; aim for 100%"),
    "the-data-science-lifecycle.html":
        ("../../the-data-science-lifecycle.html#notebook", "Back to the book", "Chapter 3 · The Data Science Lifecycle"),
    "the-data-science-lifecycle--solutions.html":
        ("../../the-data-science-lifecycle.html#quiz", "Back to the book", "Chapter 3 · Take the quiz &amp; aim for 100%"),
    "types-of-data-and-variables.html":
        ("../../types-of-data-and-variables.html#notebook", "Back to the book", "Chapter 4 · Types of Data &amp; Variables"),
    "types-of-data-and-variables--solutions.html":
        ("../../types-of-data-and-variables.html#quiz", "Back to the book", "Chapter 4 · Take the quiz &amp; aim for 100%"),
    "levels-of-measurement.html":
        ("../../levels-of-measurement.html#notebook", "Back to the book", "Chapter 5 · Levels of Measurement"),
    "levels-of-measurement--solutions.html":
        ("../../levels-of-measurement.html#quiz", "Back to the book", "Chapter 5 · Take the quiz &amp; aim for 100%"),
    "population-vs-sample-parameter-vs-statistic.html":
        ("../../population-vs-sample-parameter-vs-statistic.html#notebook", "Back to the book", "Chapter 6 · Population vs. Sample"),
    "population-vs-sample-parameter-vs-statistic--solutions.html":
        ("../../population-vs-sample-parameter-vs-statistic.html#quiz", "Back to the book", "Chapter 6 · Take the quiz &amp; aim for 100%"),
    "math-refresher-for-statistics.html":
        ("../../math-refresher-for-statistics.html#notebook", "Back to the book", "Chapter 7 · Math Refresher for Statistics"),
    "math-refresher-for-statistics--solutions.html":
        ("../../math-refresher-for-statistics.html#quiz", "Back to the book", "Chapter 7 · Take the quiz &amp; aim for 100%"),
    "measures-of-central-tendency.html":
        ("../../measures-of-central-tendency.html#notebook", "Back to the book", "Chapter 8 · Measures of Central Tendency"),
    "measures-of-central-tendency--solutions.html":
        ("../../measures-of-central-tendency.html#quiz", "Back to the book", "Chapter 8 · Take the quiz &amp; aim for 100%"),
    "measures-of-dispersion.html":
        ("../../measures-of-dispersion.html#notebook", "Back to the book", "Chapter 9 · Measures of Dispersion"),
    "measures-of-dispersion--solutions.html":
        ("../../measures-of-dispersion.html#quiz", "Back to the book", "Chapter 9 · Take the quiz &amp; aim for 100%"),
    "measures-of-position.html":
        ("../../measures-of-position.html#notebook", "Back to the book", "Chapter 10 · Measures of Position"),
    "measures-of-position--solutions.html":
        ("../../measures-of-position.html#quiz", "Back to the book", "Chapter 10 · Take the quiz &amp; aim for 100%"),
    "shape-of-a-distribution.html":
        ("../../shape-of-a-distribution.html#notebook", "Back to the book", "Chapter 11 · Shape of a Distribution"),
    "shape-of-a-distribution--solutions.html":
        ("../../shape-of-a-distribution.html#quiz", "Back to the book", "Chapter 11 · Take the quiz &amp; aim for 100%"),
    "standardization-and-z-scores.html":
        ("../../standardization-and-z-scores.html#notebook", "Back to the book", "Chapter 12 · Standardization & z-scores"),
    "standardization-and-z-scores--solutions.html":
        ("../../standardization-and-z-scores.html#quiz", "Back to the book", "Chapter 12 · Take the quiz &amp; aim for 100%"),
    "frequency-distributions.html":
        ("../../frequency-distributions.html#notebook", "Back to the book", "Chapter 13 · Frequency Distributions"),
    "frequency-distributions--solutions.html":
        ("../../frequency-distributions.html#quiz", "Back to the book", "Chapter 13 · Take the quiz &amp; aim for 100%"),
    "charts-for-categorical-data.html":
        ("../../charts-for-categorical-data.html#notebook", "Back to the book", "Chapter 14 · Charts for Categorical Data"),
    "charts-for-categorical-data--solutions.html":
        ("../../charts-for-categorical-data.html#quiz", "Back to the book", "Chapter 14 · Take the quiz &amp; aim for 100%"),
    "charts-for-numerical-data.html":
        ("../../charts-for-numerical-data.html#notebook", "Back to the book", "Chapter 15 · Charts for Numerical Data"),
    "charts-for-numerical-data--solutions.html":
        ("../../charts-for-numerical-data.html#quiz", "Back to the book", "Chapter 15 · Take the quiz &amp; aim for 100%"),
    "multivariate-and-specialized-visuals.html":
        ("../../multivariate-and-specialized-visuals.html#notebook", "Back to the book", "Chapter 16 · Multivariate &amp; Specialized Visuals"),
    "multivariate-and-specialized-visuals--solutions.html":
        ("../../multivariate-and-specialized-visuals.html#quiz", "Back to the book", "Chapter 16 · Take the quiz &amp; aim for 100%"),
    "choosing-the-right-visualization.html":
        ("../../choosing-the-right-visualization.html#notebook", "Back to the book", "Chapter 17 · Choosing the Right Visualization"),
    "choosing-the-right-visualization--solutions.html":
        ("../../choosing-the-right-visualization.html#quiz", "Back to the book", "Chapter 17 · Take the quiz &amp; aim for 100%"),
    "the-data-cleaning-mindset.html":
        ("../../the-data-cleaning-mindset.html#notebook", "Back to the book", "Chapter 18 · The Data-Cleaning Mindset"),
    "the-data-cleaning-mindset--solutions.html":
        ("../../the-data-cleaning-mindset.html#quiz", "Back to the book", "Chapter 18 · Take the quiz &amp; aim for 100%"),
    "finding-and-removing-duplicates-and-inconsistencies.html":
        ("../../finding-and-removing-duplicates-and-inconsistencies.html#notebook", "Back to the book", "Chapter 19 · Finding & Removing Duplicates and Inconsistencies"),
    "finding-and-removing-duplicates-and-inconsistencies--solutions.html":
        ("../../finding-and-removing-duplicates-and-inconsistencies.html#quiz", "Back to the book", "Chapter 19 · Take the quiz &amp; aim for 100%"),
    "handling-missing-data.html":
        ("../../handling-missing-data.html#notebook", "Back to the book", "Chapter 20 · Handling Missing Data"),
    "handling-missing-data--solutions.html":
        ("../../handling-missing-data.html#quiz", "Back to the book", "Chapter 20 · Take the quiz &amp; aim for 100%"),
    "detecting-and-treating-outliers.html":
        ("../../detecting-and-treating-outliers.html#notebook", "Back to the book", "Chapter 21 · Detecting & Treating Outliers"),
    "detecting-and-treating-outliers--solutions.html":
        ("../../detecting-and-treating-outliers.html#quiz", "Back to the book", "Chapter 21 · Take the quiz &amp; aim for 100%"),
    "transformations.html":
        ("../../transformations.html#notebook", "Back to the book", "Chapter 22 · Transformations"),
    "transformations--solutions.html":
        ("../../transformations.html#quiz", "Back to the book", "Chapter 22 · Take the quiz &amp; aim for 100%"),
    "combining-and-reshaping-data.html":
        ("../../combining-and-reshaping-data.html#notebook", "Back to the book", "Chapter 23 · Combining & Reshaping Data"),
    "combining-and-reshaping-data--solutions.html":
        ("../../combining-and-reshaping-data.html#quiz", "Back to the book", "Chapter 23 · Take the quiz &amp; aim for 100%"),
    "feature-engineering.html":
        ("../../feature-engineering.html#notebook", "Back to the book", "Chapter 24 · Feature Engineering"),
    "feature-engineering--solutions.html":
        ("../../feature-engineering.html#quiz", "Back to the book", "Chapter 24 · Take the quiz &amp; aim for 100%"),
    "exploratory-data-analysis-eda.html":
        ("../../exploratory-data-analysis-eda.html#notebook", "Back to the book", "Chapter 25 · Exploratory Data Analysis"),
    "exploratory-data-analysis-eda--solutions.html":
        ("../../exploratory-data-analysis-eda.html#quiz", "Back to the book", "Chapter 25 · Take the quiz &amp; aim for 100%"),
    "review-and-how-to-read-these-case-studies.html":
        ("../../review-and-how-to-read-these-case-studies.html#notebook", "Back to the book", "Chapter 26 · Review &amp; Case-Study Roadmap"),
    "review-and-how-to-read-these-case-studies--solutions.html":
        ("../../review-and-how-to-read-these-case-studies.html#quiz", "Back to the book", "Chapter 26 · Take the quiz &amp; aim for 100%"),
    "case-study-spotify-track-features.html":
        ("../../case-study-spotify-track-features.html#notebook", "Back to the book", "Chapter 27 · Case Study: Spotify Track Features"),
    "case-study-spotify-track-features--solutions.html":
        ("../../case-study-spotify-track-features.html#quiz", "Back to the book", "Chapter 27 · Take the quiz &amp; aim for 100%"),
    "case-study-ames-housing-prices.html":
        ("../../case-study-ames-housing-prices.html#notebook", "Back to the book", "Chapter 28 · Case Study: Ames Housing Prices"),
    "case-study-ames-housing-prices--solutions.html":
        ("../../case-study-ames-housing-prices.html#quiz", "Back to the book", "Chapter 28 · Take the quiz &amp; aim for 100%"),
    "case-study-palmer-penguins.html":
        ("../../case-study-palmer-penguins.html#notebook", "Back to the book", "Chapter 29 · Case Study: Palmer Penguins"),
    "case-study-palmer-penguins--solutions.html":
        ("../../case-study-palmer-penguins.html#quiz", "Back to the book", "Chapter 29 · Take the quiz &amp; aim for 100%"),
    "probability-fundamentals.html":
        ("../../probability-fundamentals.html#notebook", "Back to the book", "Chapter 30 · Probability Fundamentals"),
    "probability-fundamentals--solutions.html":
        ("../../probability-fundamentals.html#quiz", "Back to the book", "Chapter 30 · Take the quiz &amp; aim for 100%"),
    "rules-of-probability.html":
        ("../../rules-of-probability.html#notebook", "Back to the book", "Chapter 31 · Rules of Probability"),
    "rules-of-probability--solutions.html":
        ("../../rules-of-probability.html#quiz", "Back to the book", "Chapter 31 · Take the quiz &amp; aim for 100%"),
    "counting-and-combinatorics.html":
        ("../../counting-and-combinatorics.html#notebook", "Back to the book", "Chapter 32 · Counting &amp; Combinatorics"),
    "counting-and-combinatorics--solutions.html":
        ("../../counting-and-combinatorics.html#quiz", "Back to the book", "Chapter 32 · Take the quiz &amp; aim for 100%"),
    "conditional-probability-and-independence.html":
        ("../../conditional-probability-and-independence.html#notebook", "Back to the book", "Chapter 33 · Conditional Probability &amp; Independence"),
    "conditional-probability-and-independence--solutions.html":
        ("../../conditional-probability-and-independence.html#quiz", "Back to the book", "Chapter 33 · Take the quiz &amp; aim for 100%"),
    "bayes-theorem.html":
        ("../../bayes-theorem.html#notebook", "Back to the book", "Chapter 34 · Bayes' Theorem &amp; the Law of Total Probability"),
    "bayes-theorem--solutions.html":
        ("../../bayes-theorem.html#quiz", "Back to the book", "Chapter 34 · Take the quiz &amp; aim for 100%"),
    "random-variables-and-expectation.html":
        ("../../random-variables-and-expectation.html#notebook", "Back to the book", "Chapter 35 · Random Variables &amp; Expectation"),
    "random-variables-and-expectation--solutions.html":
        ("../../random-variables-and-expectation.html#quiz", "Back to the book", "Chapter 35 · Take the quiz &amp; aim for 100%"),
    "probability-by-simulation.html":
        ("../../probability-by-simulation.html#notebook", "Back to the book", "Chapter 36 · Probability by Simulation (Monte Carlo)"),
    "probability-by-simulation--solutions.html":
        ("../../probability-by-simulation.html#quiz", "Back to the book", "Chapter 36 · Take the quiz &amp; aim for 100%"),
    "discrete-distributions.html":
        ("../../discrete-distributions.html#notebook", "Back to the book", "Chapter 37 · Discrete Distributions"),
    "discrete-distributions--solutions.html":
        ("../../discrete-distributions.html#quiz", "Back to the book", "Chapter 37 · Take the quiz &amp; aim for 100%"),
    "continuous-distributions.html":
        ("../../continuous-distributions.html#notebook", "Back to the book", "Chapter 38 · Continuous Distributions"),
    "continuous-distributions--solutions.html":
        ("../../continuous-distributions.html#quiz", "Back to the book", "Chapter 38 · Take the quiz &amp; aim for 100%"),
    "the-normal-distribution-in-depth.html":
        ("../../the-normal-distribution-in-depth.html#notebook", "Back to the book", "Chapter 39 · The Normal Distribution in Depth"),
    "the-normal-distribution-in-depth--solutions.html":
        ("../../the-normal-distribution-in-depth.html#quiz", "Back to the book", "Chapter 39 · Take the quiz &amp; aim for 100%"),
    "sampling-distributions-and-the-central-limit-theorem.html":
        ("../../sampling-distributions-and-the-central-limit-theorem.html#notebook", "Back to the book", "Chapter 40 · Sampling Distributions &amp; the CLT"),
    "sampling-distributions-and-the-central-limit-theorem--solutions.html":
        ("../../sampling-distributions-and-the-central-limit-theorem.html#quiz", "Back to the book", "Chapter 40 · Take the quiz &amp; aim for 100%"),
    "distributions-for-inference.html":
        ("../../distributions-for-inference.html#notebook", "Back to the book", "Chapter 41 · Distributions for Inference"),
    "distributions-for-inference--solutions.html":
        ("../../distributions-for-inference.html#quiz", "Back to the book", "Chapter 41 · Take the quiz &amp; aim for 100%"),
    "joint-marginal-and-conditional-densities.html":
        ("../../joint-marginal-and-conditional-densities.html#notebook", "Back to the book", "Chapter 42 · Joint, Marginal &amp; Conditional Densities"),
    "joint-marginal-and-conditional-densities--solutions.html":
        ("../../joint-marginal-and-conditional-densities.html#quiz", "Back to the book", "Chapter 42 · Take the quiz &amp; aim for 100%"),
    "transformations-of-random-variables.html":
        ("../../transformations-of-random-variables.html#notebook", "Back to the book", "Chapter 43 · Transformations of Random Variables"),
    "transformations-of-random-variables--solutions.html":
        ("../../transformations-of-random-variables.html#quiz", "Back to the book", "Chapter 43 · Take the quiz &amp; aim for 100%"),
    "conditional-expectation-and-the-tower-property.html":
        ("../../conditional-expectation-and-the-tower-property.html#notebook", "Back to the book", "Chapter 44 · Conditional Expectation &amp; the Tower Property"),
    "conditional-expectation-and-the-tower-property--solutions.html":
        ("../../conditional-expectation-and-the-tower-property.html#quiz", "Back to the book", "Chapter 44 · Take the quiz &amp; aim for 100%"),
    "moments-mgfs-and-inequalities.html":
        ("../../moments-mgfs-and-inequalities.html#notebook", "Back to the book", "Chapter 45 · Moments, MGFs &amp; Inequalities"),
    "moments-mgfs-and-inequalities--solutions.html":
        ("../../moments-mgfs-and-inequalities.html#quiz", "Back to the book", "Chapter 45 · Take the quiz &amp; aim for 100%"),
    "estimation-theory.html":
        ("../../estimation-theory.html#notebook", "Back to the book", "Chapter 46 · Estimation Theory"),
    "estimation-theory--solutions.html":
        ("../../estimation-theory.html#quiz", "Back to the book", "Chapter 46 · Take the quiz &amp; aim for 100%"),
    "the-probability-distribution-framework.html":
        ("../../the-probability-distribution-framework.html#notebook", "Back to the book", "Chapter 47 · The Probability Distribution Framework"),
    "case-study-e-commerce-conversions-bernoulli.html":
        ("../../case-study-e-commerce-conversions-bernoulli.html#notebook", "Back to the book", "Chapter 48 · E-commerce Conversions (Bernoulli)"),
    "case-study-manufacturing-defects-binomial.html":
        ("../../case-study-manufacturing-defects-binomial.html#notebook", "Back to the book", "Chapter 49 · Manufacturing Defects (Binomial)"),
    "case-study-server-traffic-spikes-poisson.html":
        ("../../case-study-server-traffic-spikes-poisson.html#notebook", "Back to the book", "Chapter 50 · Server Traffic Spikes (Poisson)"),
    "case-study-sales-calls-to-first-win-geometric.html":
        ("../../case-study-sales-calls-to-first-win-geometric.html#notebook", "Back to the book", "Chapter 51 · Sales Calls to First Win (Geometric)"),
    "case-study-wildlife-capture-recapture-hypergeometric.html":
        ("../../case-study-wildlife-capture-recapture-hypergeometric.html#notebook", "Back to the book", "Chapter 52 · Capture-Recapture (Hypergeometric)"),
    "case-study-software-reliability-testing-negative-binomial.html":
        ("../../case-study-software-reliability-testing-negative-binomial.html#notebook", "Back to the book", "Chapter 53 · Software Reliability (Negative Binomial)"),
    "case-study-standardized-exam-scores-normal.html":
        ("../../case-study-standardized-exam-scores-normal.html#notebook", "Back to the book", "Chapter 54 · Exam Scores (Normal)"),
    "case-study-hardware-lifespans-exponential.html":
        ("../../case-study-hardware-lifespans-exponential.html#notebook", "Back to the book", "Chapter 55 · Hardware Lifespans (Exponential)"),
    "case-study-regional-rainfall-gamma.html":
        ("../../case-study-regional-rainfall-gamma.html#notebook", "Back to the book", "Chapter 56 · Regional Rainfall (Gamma)"),
    "case-study-freight-weights-and-the-clt-central-limit-theorem.html":
        ("../../case-study-freight-weights-and-the-clt-central-limit-theorem.html#notebook", "Back to the book", "Chapter 57 · Freight Weights & the CLT"),
    "case-study-clinical-trial-efficacy-student-s-t.html":
        ("../../case-study-clinical-trial-efficacy-student-s-t.html#notebook", "Back to the book", "Chapter 58 · Clinical Trial Efficacy (Student's t)"),
    "case-study-survey-demographics-chi-square.html":
        ("../../case-study-survey-demographics-chi-square.html#notebook", "Back to the book", "Chapter 59 · Survey Demographics (Chi-Square)"),
    "case-study-crop-yield-by-fertilizer-f-anova.html":
        ("../../case-study-crop-yield-by-fertilizer-f-anova.html#notebook", "Back to the book", "Chapter 60 · Crop Yield by Fertilizer (F / ANOVA)"),
    "why-we-sample.html":
        ("../../why-we-sample.html#notebook", "Back to the book", "Chapter 61 · Why We Sample"),
    "why-we-sample--solutions.html":
        ("../../why-we-sample.html#challenges", "Back to the book", "Chapter 61 · Why We Sample"),
    "probability-sampling-methods.html":
        ("../../probability-sampling-methods.html#notebook", "Back to the book", "Chapter 62 · Probability Sampling Methods"),
    "probability-sampling-methods--solutions.html":
        ("../../probability-sampling-methods.html#challenges", "Back to the book", "Chapter 62 · Probability Sampling Methods"),
    "non-probability-sampling-methods.html":
        ("../../non-probability-sampling-methods.html#notebook", "Back to the book", "Chapter 63 · Non-Probability Sampling Methods"),
    "non-probability-sampling-methods--solutions.html":
        ("../../non-probability-sampling-methods.html#challenges", "Back to the book", "Chapter 63 · Non-Probability Sampling Methods"),
    "determining-sample-size.html":
        ("../../determining-sample-size.html#notebook", "Back to the book", "Chapter 64 · Determining Sample Size"),
    "determining-sample-size--solutions.html":
        ("../../determining-sample-size.html#challenges", "Back to the book", "Chapter 64 · Determining Sample Size"),
    "study-design-and-data-quality.html":
        ("../../study-design-and-data-quality.html#notebook", "Back to the book", "Chapter 65 · Study Design & Data Quality"),
    "study-design-and-data-quality--solutions.html":
        ("../../study-design-and-data-quality.html#challenges", "Back to the book", "Chapter 65 · Study Design & Data Quality"),
    "bias-in-data-collection.html":
        ("../../bias-in-data-collection.html#notebook", "Back to the book", "Chapter 66 · Bias in Data Collection"),
    "bias-in-data-collection--solutions.html":
        ("../../bias-in-data-collection.html#challenges", "Back to the book", "Chapter 66 · Bias in Data Collection"),
    "point-vs-interval-estimation.html":
        ("../../point-vs-interval-estimation.html#notebook", "Back to the book", "Chapter 69 · Point vs. Interval Estimation"),
    "point-vs-interval-estimation--solutions.html":
        ("../../point-vs-interval-estimation.html#challenges", "Back to the book", "Chapter 69 · Point vs. Interval Estimation"),
    "confidence-intervals-for-a-mean.html":
        ("../../confidence-intervals-for-a-mean.html#notebook", "Back to the book", "Chapter 70 · Confidence Intervals for a Mean"),
    "confidence-intervals-for-a-mean--solutions.html":
        ("../../confidence-intervals-for-a-mean.html#challenges", "Back to the book", "Chapter 70 · Confidence Intervals for a Mean"),
    "confidence-intervals-for-proportions-and-differences.html":
        ("../../confidence-intervals-for-proportions-and-differences.html#notebook", "Back to the book", "Chapter 71 · Confidence Intervals for Proportions & Differences"),
    "confidence-intervals-for-proportions-and-differences--solutions.html":
        ("../../confidence-intervals-for-proportions-and-differences.html#challenges", "Back to the book", "Chapter 71 · Confidence Intervals for Proportions & Differences"),
    "margin-of-error.html":
        ("../../margin-of-error.html#notebook", "Back to the book", "Chapter 72 · Margin of Error"),
    "margin-of-error--solutions.html":
        ("../../margin-of-error.html#challenges", "Back to the book", "Chapter 72 · Margin of Error"),
    "resampling-and-simulation.html":
        ("../../resampling-and-simulation.html#notebook", "Back to the book", "Chapter 73 · Resampling & Simulation"),
    "resampling-and-simulation--solutions.html":
        ("../../resampling-and-simulation.html#challenges", "Back to the book", "Chapter 73 · Resampling & Simulation"),
    "the-logic-of-hypothesis-testing.html":
        ("../../the-logic-of-hypothesis-testing.html#notebook", "Back to the book", "Chapter 74 · The Logic of Hypothesis Testing"),
    "the-logic-of-hypothesis-testing--solutions.html":
        ("../../the-logic-of-hypothesis-testing.html#challenges", "Back to the book", "Chapter 74 · The Logic of Hypothesis Testing"),
    "significance-p-values-and-errors.html":
        ("../../significance-p-values-and-errors.html#notebook", "Back to the book", "Chapter 75 · Significance, p-values &amp; Errors"),
    "significance-p-values-and-errors--solutions.html":
        ("../../significance-p-values-and-errors.html#challenges", "Back to the book", "Chapter 75 · Significance, p-values &amp; Errors"),
    "z-tests.html":
        ("../../z-tests.html#notebook", "Back to the book", "Chapter 76 · z-Tests"),
    "z-tests--solutions.html":
        ("../../z-tests.html#challenges", "Back to the book", "Chapter 76 · z-Tests"),
    "t-tests.html":
        ("../../t-tests.html#notebook", "Back to the book", "Chapter 77 · t-Tests"),
    "t-tests--solutions.html":
        ("../../t-tests.html#challenges", "Back to the book", "Chapter 77 · t-Tests"),
    "anova.html":
        ("../../anova.html#notebook", "Back to the book", "Chapter 78 · ANOVA"),
    "anova--solutions.html":
        ("../../anova.html#challenges", "Back to the book", "Chapter 78 · ANOVA"),
    "chi-square-tests.html":
        ("../../chi-square-tests.html#notebook", "Back to the book", "Chapter 79 · Chi-Square Tests"),
    "chi-square-tests--solutions.html":
        ("../../chi-square-tests.html#challenges", "Back to the book", "Chapter 79 · Chi-Square Tests"),
    "nonparametric-tests.html":
        ("../../nonparametric-tests.html#notebook", "Back to the book", "Chapter 80 · Nonparametric Tests"),
    "nonparametric-tests--solutions.html":
        ("../../nonparametric-tests.html#challenges", "Back to the book", "Chapter 80 · Nonparametric Tests"),
    "choosing-the-right-test.html":
        ("../../choosing-the-right-test.html#notebook", "Back to the book", "Chapter 81 · Choosing the Right Test"),
    "choosing-the-right-test--solutions.html":
        ("../../choosing-the-right-test.html#challenges", "Back to the book", "Chapter 81 · Choosing the Right Test"),
    "a-b-testing-and-online-experiments.html":
        ("../../a-b-testing-and-online-experiments.html#notebook", "Back to the book", "Chapter 82 · A/B Testing &amp; Online Experiments"),
    "a-b-testing-and-online-experiments--solutions.html":
        ("../../a-b-testing-and-online-experiments.html#challenges", "Back to the book", "Chapter 82 · A/B Testing &amp; Online Experiments"),
    "review-and-choosing-the-right-test.html":
        ("../../review-and-choosing-the-right-test.html#notebook", "Back to the book", "Chapter 83 · Review &amp; Choosing the Right Test"),
    "case-study-a-web-a-b-test.html":
        ("../../case-study-a-web-a-b-test.html#notebook", "Back to the book", "Chapter 84 · Case Study: A Web A/B Test"),
    "case-study-comparing-marketing-channels.html":
        ("../../case-study-comparing-marketing-channels.html#notebook", "Back to the book", "Chapter 85 · Case Study: Comparing Marketing Channels"),
    "case-study-a-clinical-trial.html":
        ("../../case-study-a-clinical-trial.html#notebook", "Back to the book", "Chapter 86 · Case Study: A Clinical Trial"),
    "case-study-a-customer-satisfaction-survey.html":
        ("../../case-study-a-customer-satisfaction-survey.html#notebook", "Back to the book", "Chapter 87 · Case Study: A Customer Satisfaction Survey"),
    "case-study-manufacturing-quality.html":
        ("../../case-study-manufacturing-quality.html#notebook", "Back to the book", "Chapter 88 · Case Study: Manufacturing Quality"),
    "covariance.html":
        ("../../covariance.html#notebook", "Back to the book", "Chapter 89 · Covariance"),
    "covariance--solutions.html":
        ("../../covariance.html#challenges", "Back to the book", "Chapter 89 · Covariance"),
    "correlation-coefficients.html":
        ("../../correlation-coefficients.html#notebook", "Back to the book", "Chapter 90 · Correlation Coefficients"),
    "correlation-coefficients--solutions.html":
        ("../../correlation-coefficients.html#challenges", "Back to the book", "Chapter 90 · Correlation Coefficients"),
    "correlation-vs-causation.html":
        ("../../correlation-vs-causation.html#notebook", "Back to the book", "Chapter 91 · Correlation vs. Causation"),
    "correlation-vs-causation--solutions.html":
        ("../../correlation-vs-causation.html#challenges", "Back to the book", "Chapter 91 · Correlation vs. Causation"),
    "simple-linear-regression.html":
        ("../../simple-linear-regression.html#notebook", "Back to the book", "Chapter 92 · Simple Linear Regression"),
    "simple-linear-regression--solutions.html":
        ("../../simple-linear-regression.html#challenges", "Back to the book", "Chapter 92 · Simple Linear Regression"),
    "the-ols-framework.html":
        ("../../the-ols-framework.html#notebook", "Back to the book", "Chapter 93 · The OLS Framework"),
    "the-ols-framework--solutions.html":
        ("../../the-ols-framework.html#challenges", "Back to the book", "Chapter 93 · The OLS Framework"),
    "multiple-linear-regression.html":
        ("../../multiple-linear-regression.html#notebook", "Back to the book", "Chapter 94 · Multiple Linear Regression"),
    "multiple-linear-regression--solutions.html":
        ("../../multiple-linear-regression.html#challenges", "Back to the book", "Chapter 94 · Multiple Linear Regression"),
    "regression-assumptions-and-diagnostics.html":
        ("../../regression-assumptions-and-diagnostics.html#notebook", "Back to the book", "Chapter 95 · Regression Assumptions & Diagnostics"),
    "regression-assumptions-and-diagnostics--solutions.html":
        ("../../regression-assumptions-and-diagnostics.html#challenges", "Back to the book", "Chapter 95 · Regression Assumptions & Diagnostics"),
    "logistic-regression.html":
        ("../../logistic-regression.html#notebook", "Back to the book", "Chapter 96 · Logistic Regression"),
    "logistic-regression--solutions.html":
        ("../../logistic-regression.html#challenges", "Back to the book", "Chapter 96 · Logistic Regression"),
    "regularization-and-flexible-models.html":
        ("../../regularization-and-flexible-models.html#notebook", "Back to the book", "Chapter 97 · Regularization & Flexible Models"),
    "regularization-and-flexible-models--solutions.html":
        ("../../regularization-and-flexible-models.html#challenges", "Back to the book", "Chapter 97 · Regularization & Flexible Models"),
    "generalized-linear-models.html":
        ("../../generalized-linear-models.html#notebook", "Back to the book", "Chapter 98 · Generalized Linear Models"),
    "generalized-linear-models--solutions.html":
        ("../../generalized-linear-models.html#challenges", "Back to the book", "Chapter 98 · Generalized Linear Models"),
    "econometrics-and-panel-data.html":
        ("../../econometrics-and-panel-data.html#notebook", "Back to the book", "Chapter 99 · Econometrics & Panel Data"),
    "econometrics-and-panel-data--solutions.html":
        ("../../econometrics-and-panel-data.html#challenges", "Back to the book", "Chapter 99 · Econometrics & Panel Data"),
    "case-study-predicting-ames-house-prices.html":
        ("../../case-study-predicting-ames-house-prices.html#notebook", "Back to the book", "Chapter 100 · Case Study: Predicting Ames House Prices"),
    "case-study-predicting-ames-house-prices--take-it-further.html":
        ("../../case-study-predicting-ames-house-prices.html#challenges", "Back to the book", "Chapter 100 · Take It Further"),
    "case-study-logistic-regression-in-action.html":
        ("../../case-study-logistic-regression-in-action.html#notebook", "Back to the book", "Chapter 101 · Case Study: Logistic Regression in Action"),
    "case-study-logistic-regression-in-action--take-it-further.html":
        ("../../case-study-logistic-regression-in-action.html#challenges", "Back to the book", "Chapter 101 · Take It Further"),
    "case-study-forecasting-daily-bike-share-demand.html":
        ("../../case-study-forecasting-daily-bike-share-demand.html#notebook", "Back to the book", "Chapter 102 · Case Study: Forecasting Daily Bike-Share Demand"),
    "case-study-forecasting-daily-bike-share-demand--take-it-further.html":
        ("../../case-study-forecasting-daily-bike-share-demand.html#challenges", "Back to the book", "Chapter 102 · Take It Further"),
    "case-study-predicting-medical-charges.html":
        ("../../case-study-predicting-medical-charges.html#notebook", "Back to the book", "Chapter 103 · Case Study: Predicting Medical Charges"),
    "case-study-predicting-medical-charges--take-it-further.html":
        ("../../case-study-predicting-medical-charges.html#challenges", "Back to the book", "Chapter 103 · Take It Further"),
    "bayesian-inference-in-practice.html":
        ("../../bayesian-inference-in-practice.html#notebook", "Back to the book", "Chapter 142 · Bayesian Inference in Practice"),
    "bayesian-inference-in-practice--solutions.html":
        ("../../bayesian-inference-in-practice.html#challenges", "Back to the book", "Chapter 142 · Challenge solutions"),
    "causal-inference.html":
        ("../../causal-inference.html#notebook", "Back to the book", "Chapter 143 · Causal Inference"),
    "causal-inference--solutions.html":
        ("../../causal-inference.html#challenges", "Back to the book", "Chapter 143 · Challenge solutions"),
    "survival-analysis.html":
        ("../../survival-analysis.html#notebook", "Back to the book", "Chapter 144 · Survival Analysis"),
    "survival-analysis--solutions.html":
        ("../../survival-analysis.html#challenges", "Back to the book", "Chapter 144 · Challenge solutions"),
}

def card(href, kicker, title):
    # Matches the book's chapter-nav card look (inlined, since nbconvert HTML has no book CSS).
    return (
      '<a class="book-backlink" href="' + href + '" '
      'style="display:flex;align-items:center;gap:12px;max-width:760px;margin:18px auto;'
      'text-decoration:none;border:1px solid #e6e9f2;border-radius:13px;padding:15px 20px;'
      'background:#ffffff;box-shadow:0 6px 18px rgba(20,30,80,0.06);'
      "font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif\">"
      '<span style="font-size:22px;color:#0891b2;line-height:1">&#8592;</span>'
      '<span>'
      '<span style="display:block;font-size:11px;font-weight:700;letter-spacing:0.08em;'
      'text-transform:uppercase;color:#8b94b3">' + kicker + '</span>'
      '<span style="font-weight:700;color:#1a2138;font-size:15px">' + title + '</span>'
      '</span></a>'
    )

# Override nbconvert's centered tables so they left-align like Colab.
TABLE_ALIGN_CSS = (
    '<style id="book-table-align">'
    '.jp-RenderedHTMLCommon table{margin-left:0 !important;margin-right:auto !important;}'
    '</style>'
)

def inject(path, href, kicker, title):
    html = open(path, encoding="utf-8").read()
    if 'class="book-backlink"' in html:
        return "already had link"
    # left-align tables (inject the style once, before </head>)
    if 'id="book-table-align"' not in html:
        html = html.replace("</head>", TABLE_ALIGN_CSS + "\n</head>", 1)
    c = card(href, kicker, title)
    # top: right after the opening <body ...> tag
    i = html.find("<body")
    if i != -1:
        j = html.find(">", i) + 1
        html = html[:j] + "\n" + c + html[j:]
    # bottom: right before </body>
    html = html.replace("</body>", c + "\n</body>", 1)
    open(path, "w", encoding="utf-8").write(html)
    return "injected"

def main():
    if not os.path.isdir(HTML_DIR):
        print("No HTML dir yet:", HTML_DIR); return
    for fname, (href, kicker, title) in MAP.items():
        path = os.path.join(HTML_DIR, fname)
        if os.path.exists(path):
            print(f"{fname}: {inject(path, href, kicker, title)}")
        else:
            print(f"{fname}: (not rendered yet, skipped)")

if __name__ == "__main__":
    main()
