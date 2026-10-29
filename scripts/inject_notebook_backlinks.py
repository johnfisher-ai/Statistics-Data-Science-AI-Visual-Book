#!/usr/bin/env python3
"""Give each rendered notebook page its book card, links and head tags.

Run AFTER `nbconvert`. It changes only the View-Notebook HTML, never the .ipynb files, and is
wired into both scripts/build_notebook_html.sh and the GitHub Actions deploy workflow so it
survives every re-render. Each run rewrites what it added before, so a page always carries the
current design, and running it twice changes nothing the second time. On every page it sets:

  - the tab title, description, canonical address and link-preview tags, from the chapter's
    title and number in toc.html and the notebook's hero cell
  - the site icon, and styles that left-align tables, darken nbconvert's cell prompts so they
    can be read, and underline links in the notebook's text, as the chapters do
  - a card at the top with the way back to the chapter and buttons to open the notebook in Colab,
    download it and view it on GitHub, and the way back again at the bottom
  - an h1 for a page that has none: the hero cell's title, drawn as before. A heading that then
    skips a level (an h3 straight after the h1) moves up one, keeping its size, and the blank
    corner cell of a pandas table header becomes a plain cell, so screen readers get a sound outline
  - darker shades for the colors that read below 4.5:1 on the page: the code highlighting's
    comments, numbers, operators and errors, and the faint footer line many notebooks end with
  - on a phone, hero titles at 28 px and long words wrapped, so no text cell scrolls sideways

The notebooks themselves are left alone, so nothing changes for a reader in Colab, which has its
own highlighting and themes.

Add a chapter's notebooks to MAP as they ship.
"""
import html as htmllib, json, os, re, unicodedata

HTML_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chapters", "notebooks", "html")

# notebook-html filename -> (relative href to the chapter section, kicker, title)
MAP = {
    "what-is-machine-learning.html":
        ("../../what-is-machine-learning.html#notebook", "Back to the book", "Chapter 108 · What Is Machine Learning?"),
    "what-is-machine-learning--solutions.html":
        ("../../what-is-machine-learning.html#quiz", "Back to the book", "Chapter 108 · Take the quiz &amp; aim for 100%"),
    "the-machine-learning-workflow.html":
        ("../../the-machine-learning-workflow.html#notebook", "Back to the book", "Chapter 109 · The Machine Learning Workflow"),
    "the-machine-learning-workflow--solutions.html":
        ("../../the-machine-learning-workflow.html#quiz", "Back to the book", "Chapter 109 · Take the quiz &amp; aim for 100%"),
    "distance-metrics.html":
        ("../../distance-metrics.html#notebook", "Back to the book", "Chapter 110 · Distance Metrics"),
    "distance-metrics--solutions.html":
        ("../../distance-metrics.html#quiz", "Back to the book", "Chapter 110 · Take the quiz &amp; aim for 100%"),
    "core-classification-and-regression-algorithms.html":
        ("../../core-classification-and-regression-algorithms.html#notebook", "Back to the book", "Chapter 111 · Core Classification &amp; Regression Algorithms"),
    "core-classification-and-regression-algorithms--solutions.html":
        ("../../core-classification-and-regression-algorithms.html#quiz", "Back to the book", "Chapter 111 · Take the quiz &amp; aim for 100%"),
    "ensemble-methods.html":
        ("../../ensemble-methods.html#notebook", "Back to the book", "Chapter 112 · Ensemble Methods"),
    "ensemble-methods--solutions.html":
        ("../../ensemble-methods.html#quiz", "Back to the book", "Chapter 112 · Take the quiz &amp; aim for 100%"),
    "feature-selection.html":
        ("../../feature-selection.html#notebook", "Back to the book", "Chapter 113 · Feature Selection"),
    "feature-selection--solutions.html":
        ("../../feature-selection.html#quiz", "Back to the book", "Chapter 113 · Take the quiz &amp; aim for 100%"),
    "optimization-and-gradient-descent.html":
        ("../../optimization-and-gradient-descent.html#notebook", "Back to the book", "Chapter 114 · Optimization &amp; Gradient Descent"),
    "optimization-and-gradient-descent--solutions.html":
        ("../../optimization-and-gradient-descent.html#quiz", "Back to the book", "Chapter 114 · Take the quiz &amp; aim for 100%"),
    "model-evaluation.html":
        ("../../model-evaluation.html#notebook", "Back to the book", "Chapter 115 · Model Evaluation"),
    "model-evaluation--solutions.html":
        ("../../model-evaluation.html#quiz", "Back to the book", "Chapter 115 · Take the quiz &amp; aim for 100%"),
    "model-pitfalls.html":
        ("../../model-pitfalls.html#notebook", "Back to the book", "Chapter 116 · Model Pitfalls"),
    "model-pitfalls--solutions.html":
        ("../../model-pitfalls.html#quiz", "Back to the book", "Chapter 116 · Take the quiz &amp; aim for 100%"),
    "model-interpretability-and-explainability.html":
        ("../../model-interpretability-and-explainability.html#notebook", "Back to the book", "Chapter 117 · Model Interpretability &amp; Explainability"),
    "model-interpretability-and-explainability--solutions.html":
        ("../../model-interpretability-and-explainability.html#quiz", "Back to the book", "Chapter 117 · Take the quiz &amp; aim for 100%"),
    "clustering.html":
        ("../../clustering.html#notebook", "Back to the book", "Chapter 118 · Clustering"),
    "clustering--solutions.html":
        ("../../clustering.html#quiz", "Back to the book", "Chapter 118 · Take the quiz &amp; aim for 100%"),
    "dimensionality-reduction.html":
        ("../../dimensionality-reduction.html#notebook", "Back to the book", "Chapter 119 · Dimensionality Reduction"),
    "dimensionality-reduction--solutions.html":
        ("../../dimensionality-reduction.html#quiz", "Back to the book", "Chapter 119 · Take the quiz &amp; aim for 100%"),
    "association-rule-mining.html":
        ("../../association-rule-mining.html#notebook", "Back to the book", "Chapter 120 · Association Rule Mining"),
    "association-rule-mining--solutions.html":
        ("../../association-rule-mining.html#quiz", "Back to the book", "Chapter 120 · Take the quiz &amp; aim for 100%"),
    "anomaly-detection.html":
        ("../../anomaly-detection.html#notebook", "Back to the book", "Chapter 121 · Anomaly Detection"),
    "anomaly-detection--solutions.html":
        ("../../anomaly-detection.html#quiz", "Back to the book", "Chapter 121 · Take the quiz &amp; aim for 100%"),
    "reinforcement-learning-primer.html":
        ("../../reinforcement-learning-primer.html#notebook", "Back to the book", "Chapter 122 · Reinforcement Learning Primer"),
    "reinforcement-learning-primer--solutions.html":
        ("../../reinforcement-learning-primer.html#quiz", "Back to the book", "Chapter 122 · Take the quiz &amp; aim for 100%"),
    "deep-rl-and-applications.html":
        ("../../deep-rl-and-applications.html#notebook", "Back to the book", "Chapter 123 · Deep RL &amp; Applications"),
    "deep-rl-and-applications--solutions.html":
        ("../../deep-rl-and-applications.html#quiz", "Back to the book", "Chapter 123 · Take the quiz &amp; aim for 100%"),
    "case-study-an-end-to-end-ml-project.html":
        ("../../case-study-an-end-to-end-ml-project.html#notebook", "Back to the book", "Chapter 124 · An End-to-End ML Project"),
    "case-study-an-end-to-end-ml-project--take-it-further.html":
        ("../../case-study-an-end-to-end-ml-project.html#challenges", "Back to the book", "Chapter 124 · Take it further"),
    "case-study-fraud-detection.html":
        ("../../case-study-fraud-detection.html#notebook", "Back to the book", "Chapter 125 · Fraud Detection"),
    "case-study-fraud-detection--take-it-further.html":
        ("../../case-study-fraud-detection.html#challenges", "Back to the book", "Chapter 125 · Take it further"),
    "case-study-predictive-maintenance.html":
        ("../../case-study-predictive-maintenance.html#notebook", "Back to the book", "Chapter 126 · Predictive Maintenance"),
    "case-study-predictive-maintenance--take-it-further.html":
        ("../../case-study-predictive-maintenance.html#challenges", "Back to the book", "Chapter 126 · Take it further"),
    "case-study-customer-segmentation-and-targeting.html":
        ("../../case-study-customer-segmentation-and-targeting.html#notebook", "Back to the book", "Chapter 127 · Customer Segmentation &amp; Targeting"),
    "case-study-customer-segmentation-and-targeting--take-it-further.html":
        ("../../case-study-customer-segmentation-and-targeting.html#challenges", "Back to the book", "Chapter 127 · Take it further"),
    "case-study-loan-default-risk.html":
        ("../../case-study-loan-default-risk.html#notebook", "Back to the book", "Chapter 128 · Loan Default Risk"),
    "case-study-loan-default-risk--take-it-further.html":
        ("../../case-study-loan-default-risk.html#challenges", "Back to the book", "Chapter 128 · Take it further"),
    "case-study-from-model-to-decision.html":
        ("../../case-study-from-model-to-decision.html#notebook", "Back to the book", "Chapter 129 · From Model to Decision"),
    "case-study-from-model-to-decision--take-it-further.html":
        ("../../case-study-from-model-to-decision.html#challenges", "Back to the book", "Chapter 129 · Take it further"),
    "case-study-operationalizing-the-model-mlops.html":
        ("../../case-study-operationalizing-the-model-mlops.html#notebook", "Back to the book", "Chapter 130 · Operationalizing the Model"),
    "case-study-operationalizing-the-model-mlops--take-it-further.html":
        ("../../case-study-operationalizing-the-model-mlops.html#challenges", "Back to the book", "Chapter 130 · Take it further"),
    "components-of-a-time-series.html":
        ("../../components-of-a-time-series.html#notebook", "Back to the book", "Chapter 132 · Components of a Time Series"),
    "components-of-a-time-series--solutions.html":
        ("../../components-of-a-time-series.html#challenges", "Back to the book", "Chapter 132 · Challenge solutions"),
    "forecasting-models.html":
        ("../../forecasting-models.html#notebook", "Back to the book", "Chapter 133 · Forecasting Models"),
    "forecasting-models--solutions.html":
        ("../../forecasting-models.html#challenges", "Back to the book", "Chapter 133 · Challenge solutions"),
    "volatility-and-advanced-models.html":
        ("../../volatility-and-advanced-models.html#notebook", "Back to the book", "Chapter 134 · Volatility & Advanced Models"),
    "volatility-and-advanced-models--solutions.html":
        ("../../volatility-and-advanced-models.html#challenges", "Back to the book", "Chapter 134 · Challenge solutions"),
    "forecast-accuracy.html":
        ("../../forecast-accuracy.html#notebook", "Back to the book", "Chapter 135 · Forecast Accuracy"),
    "forecast-accuracy--solutions.html":
        ("../../forecast-accuracy.html#challenges", "Back to the book", "Chapter 135 · Challenge solutions"),
    "case-study-forecasting-retail-sales.html":
        ("../../case-study-forecasting-retail-sales.html#notebook", "Back to the book", "Chapter 136 · Forecasting Retail Sales"),
    "case-study-forecasting-retail-sales--take-it-further.html":
        ("../../case-study-forecasting-retail-sales.html#challenges", "Back to the book", "Chapter 136 · Take it further"),
    "case-study-financial-volatility-and-risk.html":
        ("../../case-study-financial-volatility-and-risk.html#notebook", "Back to the book", "Chapter 137 · Financial Volatility & Risk"),
    "case-study-financial-volatility-and-risk--take-it-further.html":
        ("../../case-study-financial-volatility-and-risk.html#challenges", "Back to the book", "Chapter 137 · Take it further"),
    "case-study-energy-demand-forecasting.html":
        ("../../case-study-energy-demand-forecasting.html#notebook", "Back to the book", "Chapter 138 · Energy Demand Forecasting"),
    "case-study-energy-demand-forecasting--take-it-further.html":
        ("../../case-study-energy-demand-forecasting.html#challenges", "Back to the book", "Chapter 138 · Take it further"),
    "case-study-from-forecast-to-decision.html":
        ("../../case-study-from-forecast-to-decision.html#notebook", "Back to the book", "Chapter 139 · From Forecast to Decision"),
    "case-study-from-forecast-to-decision--take-it-further.html":
        ("../../case-study-from-forecast-to-decision.html#challenges", "Back to the book", "Chapter 139 · Take it further"),
    "case-study-operationalizing-a-forecast.html":
        ("../../case-study-operationalizing-a-forecast.html#notebook", "Back to the book", "Chapter 140 · Operationalizing a Forecast"),
    "case-study-operationalizing-a-forecast--take-it-further.html":
        ("../../case-study-operationalizing-a-forecast.html#challenges", "Back to the book", "Chapter 140 · Take it further"),
    "case-study-designing-and-analyzing-a-survey.html":
        ("../../case-study-designing-and-analyzing-a-survey.html#notebook", "Back to the book", "Chapter 70 · Designing and Analyzing a Survey"),
    "case-study-designing-and-analyzing-a-survey--take-it-further.html":
        ("../../case-study-designing-and-analyzing-a-survey.html#challenges", "Back to the book", "Chapter 70 · Take it further"),
    "case-study-difference-in-differences.html":
        ("../../case-study-difference-in-differences.html#notebook", "Back to the book", "Chapter 107 · Difference-in-Differences"),
    "case-study-difference-in-differences--take-it-further.html":
        ("../../case-study-difference-in-differences.html#challenges", "Back to the book", "Chapter 107 · Take it further"),
    "case-study-a-paired-pre-post-study.html":
        ("../../case-study-a-paired-pre-post-study.html#notebook", "Back to the book", "Chapter 91 · A Paired Pre/Post Study"),
    "case-study-a-paired-pre-post-study--take-it-further.html":
        ("../../case-study-a-paired-pre-post-study.html#challenges", "Back to the book", "Chapter 91 · Take it further"),
    "case-study-customer-lifetime-value.html":
        ("../../case-study-customer-lifetime-value.html#notebook", "Back to the book", "Chapter 131 · Customer Lifetime Value"),
    "case-study-customer-lifetime-value--take-it-further.html":
        ("../../case-study-customer-lifetime-value.html#challenges", "Back to the book", "Chapter 131 · Take it further"),
    "case-study-forecasting-with-drivers.html":
        ("../../case-study-forecasting-with-drivers.html#notebook", "Back to the book", "Chapter 141 · Forecasting with Drivers"),
    "case-study-forecasting-with-drivers--take-it-further.html":
        ("../../case-study-forecasting-with-drivers.html#challenges", "Back to the book", "Chapter 141 · Take it further"),
    "case-study-multi-file-and-datetime-eda.html":
        ("../../case-study-multi-file-and-datetime-eda.html#notebook", "Back to the book", "Chapter 30 · Multi-File, Multi-Date EDA"),
    "case-study-multi-file-and-datetime-eda--take-it-further.html":
        ("../../case-study-multi-file-and-datetime-eda.html#challenges", "Back to the book", "Chapter 30 · Take it further"),
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
        ("../../population-vs-sample-parameter-vs-statistic.html#notebook", "Back to the book", "Chapter 6 · Population vs. Sample &amp; Parameter vs. Statistic"),
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
        ("../../probability-fundamentals.html#notebook", "Back to the book", "Chapter 31 · Probability Fundamentals"),
    "probability-fundamentals--solutions.html":
        ("../../probability-fundamentals.html#quiz", "Back to the book", "Chapter 31 · Take the quiz &amp; aim for 100%"),
    "rules-of-probability.html":
        ("../../rules-of-probability.html#notebook", "Back to the book", "Chapter 32 · Rules of Probability"),
    "rules-of-probability--solutions.html":
        ("../../rules-of-probability.html#quiz", "Back to the book", "Chapter 32 · Take the quiz &amp; aim for 100%"),
    "counting-and-combinatorics.html":
        ("../../counting-and-combinatorics.html#notebook", "Back to the book", "Chapter 33 · Counting &amp; Combinatorics"),
    "counting-and-combinatorics--solutions.html":
        ("../../counting-and-combinatorics.html#quiz", "Back to the book", "Chapter 33 · Take the quiz &amp; aim for 100%"),
    "conditional-probability-and-independence.html":
        ("../../conditional-probability-and-independence.html#notebook", "Back to the book", "Chapter 34 · Conditional Probability &amp; Independence"),
    "conditional-probability-and-independence--solutions.html":
        ("../../conditional-probability-and-independence.html#quiz", "Back to the book", "Chapter 34 · Take the quiz &amp; aim for 100%"),
    "bayes-theorem.html":
        ("../../bayes-theorem.html#notebook", "Back to the book", "Chapter 35 · Bayes' Theorem &amp; the Law of Total Probability"),
    "bayes-theorem--solutions.html":
        ("../../bayes-theorem.html#quiz", "Back to the book", "Chapter 35 · Take the quiz &amp; aim for 100%"),
    "random-variables-and-expectation.html":
        ("../../random-variables-and-expectation.html#notebook", "Back to the book", "Chapter 36 · Random Variables &amp; Expectation"),
    "random-variables-and-expectation--solutions.html":
        ("../../random-variables-and-expectation.html#quiz", "Back to the book", "Chapter 36 · Take the quiz &amp; aim for 100%"),
    "probability-by-simulation.html":
        ("../../probability-by-simulation.html#notebook", "Back to the book", "Chapter 37 · Probability by Simulation"),
    "probability-by-simulation--solutions.html":
        ("../../probability-by-simulation.html#quiz", "Back to the book", "Chapter 37 · Take the quiz &amp; aim for 100%"),
    "discrete-distributions.html":
        ("../../discrete-distributions.html#notebook", "Back to the book", "Chapter 38 · Discrete Distributions"),
    "discrete-distributions--solutions.html":
        ("../../discrete-distributions.html#quiz", "Back to the book", "Chapter 38 · Take the quiz &amp; aim for 100%"),
    "continuous-distributions.html":
        ("../../continuous-distributions.html#notebook", "Back to the book", "Chapter 39 · Continuous Distributions"),
    "continuous-distributions--solutions.html":
        ("../../continuous-distributions.html#quiz", "Back to the book", "Chapter 39 · Take the quiz &amp; aim for 100%"),
    "the-normal-distribution-in-depth.html":
        ("../../the-normal-distribution-in-depth.html#notebook", "Back to the book", "Chapter 40 · The Normal Distribution in Depth"),
    "the-normal-distribution-in-depth--solutions.html":
        ("../../the-normal-distribution-in-depth.html#quiz", "Back to the book", "Chapter 40 · Take the quiz &amp; aim for 100%"),
    "sampling-distributions-and-the-central-limit-theorem.html":
        ("../../sampling-distributions-and-the-central-limit-theorem.html#notebook", "Back to the book", "Chapter 41 · Sampling Distributions &amp; the CLT"),
    "sampling-distributions-and-the-central-limit-theorem--solutions.html":
        ("../../sampling-distributions-and-the-central-limit-theorem.html#quiz", "Back to the book", "Chapter 41 · Take the quiz &amp; aim for 100%"),
    "distributions-for-inference.html":
        ("../../distributions-for-inference.html#notebook", "Back to the book", "Chapter 42 · Distributions for Inference"),
    "distributions-for-inference--solutions.html":
        ("../../distributions-for-inference.html#quiz", "Back to the book", "Chapter 42 · Take the quiz &amp; aim for 100%"),
    "joint-marginal-and-conditional-densities.html":
        ("../../joint-marginal-and-conditional-densities.html#notebook", "Back to the book", "Chapter 43 · Joint, Marginal &amp; Conditional Densities"),
    "joint-marginal-and-conditional-densities--solutions.html":
        ("../../joint-marginal-and-conditional-densities.html#quiz", "Back to the book", "Chapter 43 · Take the quiz &amp; aim for 100%"),
    "transformations-of-random-variables.html":
        ("../../transformations-of-random-variables.html#notebook", "Back to the book", "Chapter 44 · Transformations of Random Variables"),
    "transformations-of-random-variables--solutions.html":
        ("../../transformations-of-random-variables.html#quiz", "Back to the book", "Chapter 44 · Take the quiz &amp; aim for 100%"),
    "conditional-expectation-and-the-tower-property.html":
        ("../../conditional-expectation-and-the-tower-property.html#notebook", "Back to the book", "Chapter 45 · Conditional Expectation &amp; the Tower Property"),
    "conditional-expectation-and-the-tower-property--solutions.html":
        ("../../conditional-expectation-and-the-tower-property.html#quiz", "Back to the book", "Chapter 45 · Take the quiz &amp; aim for 100%"),
    "moments-mgfs-and-inequalities.html":
        ("../../moments-mgfs-and-inequalities.html#notebook", "Back to the book", "Chapter 46 · Moments, MGFs &amp; Inequalities"),
    "moments-mgfs-and-inequalities--solutions.html":
        ("../../moments-mgfs-and-inequalities.html#quiz", "Back to the book", "Chapter 46 · Take the quiz &amp; aim for 100%"),
    "estimation-theory.html":
        ("../../estimation-theory.html#notebook", "Back to the book", "Chapter 47 · Estimation Theory"),
    "estimation-theory--solutions.html":
        ("../../estimation-theory.html#quiz", "Back to the book", "Chapter 47 · Take the quiz &amp; aim for 100%"),
    "the-probability-distribution-framework.html":
        ("../../the-probability-distribution-framework.html#notebook", "Back to the book", "Chapter 48 · The Probability Distribution Framework"),
    "case-study-e-commerce-conversions-bernoulli.html":
        ("../../case-study-e-commerce-conversions-bernoulli.html#notebook", "Back to the book", "Chapter 49 · E-commerce Conversions (Bernoulli)"),
    "case-study-manufacturing-defects-binomial.html":
        ("../../case-study-manufacturing-defects-binomial.html#notebook", "Back to the book", "Chapter 50 · Manufacturing Defects (Binomial)"),
    "case-study-server-traffic-spikes-poisson.html":
        ("../../case-study-server-traffic-spikes-poisson.html#notebook", "Back to the book", "Chapter 51 · Server Traffic Spikes (Poisson)"),
    "case-study-sales-calls-to-first-win-geometric.html":
        ("../../case-study-sales-calls-to-first-win-geometric.html#notebook", "Back to the book", "Chapter 52 · Sales Calls to First Win (Geometric)"),
    "case-study-wildlife-capture-recapture-hypergeometric.html":
        ("../../case-study-wildlife-capture-recapture-hypergeometric.html#notebook", "Back to the book", "Chapter 53 · Capture-Recapture (Hypergeometric)"),
    "case-study-software-reliability-testing-negative-binomial.html":
        ("../../case-study-software-reliability-testing-negative-binomial.html#notebook", "Back to the book", "Chapter 54 · Software Reliability (Negative Binomial)"),
    "case-study-standardized-exam-scores-normal.html":
        ("../../case-study-standardized-exam-scores-normal.html#notebook", "Back to the book", "Chapter 55 · Exam Scores (Normal)"),
    "case-study-hardware-lifespans-exponential.html":
        ("../../case-study-hardware-lifespans-exponential.html#notebook", "Back to the book", "Chapter 56 · Hardware Lifespans (Exponential)"),
    "case-study-regional-rainfall-gamma.html":
        ("../../case-study-regional-rainfall-gamma.html#notebook", "Back to the book", "Chapter 57 · Regional Rainfall (Gamma)"),
    "case-study-freight-weights-and-the-clt-central-limit-theorem.html":
        ("../../case-study-freight-weights-and-the-clt-central-limit-theorem.html#notebook", "Back to the book", "Chapter 58 · Freight Weights & the CLT"),
    "case-study-clinical-trial-efficacy-student-s-t.html":
        ("../../case-study-clinical-trial-efficacy-student-s-t.html#notebook", "Back to the book", "Chapter 59 · Clinical Trial Efficacy (Student's t)"),
    "case-study-survey-demographics-chi-square.html":
        ("../../case-study-survey-demographics-chi-square.html#notebook", "Back to the book", "Chapter 60 · Survey Demographics (Chi-Square)"),
    "case-study-crop-yield-by-fertilizer-f-anova.html":
        ("../../case-study-crop-yield-by-fertilizer-f-anova.html#notebook", "Back to the book", "Chapter 61 · Crop Yield by Fertilizer (F / ANOVA)"),
    "why-we-sample.html":
        ("../../why-we-sample.html#notebook", "Back to the book", "Chapter 62 · Why We Sample"),
    "why-we-sample--solutions.html":
        ("../../why-we-sample.html#challenges", "Back to the book", "Chapter 62 · Why We Sample"),
    "probability-sampling-methods.html":
        ("../../probability-sampling-methods.html#notebook", "Back to the book", "Chapter 63 · Probability Sampling Methods"),
    "probability-sampling-methods--solutions.html":
        ("../../probability-sampling-methods.html#challenges", "Back to the book", "Chapter 63 · Probability Sampling Methods"),
    "non-probability-sampling-methods.html":
        ("../../non-probability-sampling-methods.html#notebook", "Back to the book", "Chapter 64 · Non-Probability Sampling Methods"),
    "non-probability-sampling-methods--solutions.html":
        ("../../non-probability-sampling-methods.html#challenges", "Back to the book", "Chapter 64 · Non-Probability Sampling Methods"),
    "determining-sample-size.html":
        ("../../determining-sample-size.html#notebook", "Back to the book", "Chapter 65 · Determining Sample Size"),
    "determining-sample-size--solutions.html":
        ("../../determining-sample-size.html#challenges", "Back to the book", "Chapter 65 · Determining Sample Size"),
    "study-design-and-data-quality.html":
        ("../../study-design-and-data-quality.html#notebook", "Back to the book", "Chapter 66 · Study Design & Data Quality"),
    "study-design-and-data-quality--solutions.html":
        ("../../study-design-and-data-quality.html#challenges", "Back to the book", "Chapter 66 · Study Design & Data Quality"),
    "bias-in-data-collection.html":
        ("../../bias-in-data-collection.html#notebook", "Back to the book", "Chapter 67 · Bias in Data Collection"),
    "bias-in-data-collection--solutions.html":
        ("../../bias-in-data-collection.html#challenges", "Back to the book", "Chapter 67 · Bias in Data Collection"),
    "point-vs-interval-estimation.html":
        ("../../point-vs-interval-estimation.html#notebook", "Back to the book", "Chapter 71 · Point vs. Interval Estimation"),
    "point-vs-interval-estimation--solutions.html":
        ("../../point-vs-interval-estimation.html#challenges", "Back to the book", "Chapter 71 · Point vs. Interval Estimation"),
    "confidence-intervals-for-a-mean.html":
        ("../../confidence-intervals-for-a-mean.html#notebook", "Back to the book", "Chapter 72 · Confidence Intervals for a Mean"),
    "confidence-intervals-for-a-mean--solutions.html":
        ("../../confidence-intervals-for-a-mean.html#challenges", "Back to the book", "Chapter 72 · Confidence Intervals for a Mean"),
    "confidence-intervals-for-proportions-and-differences.html":
        ("../../confidence-intervals-for-proportions-and-differences.html#notebook", "Back to the book", "Chapter 73 · Confidence Intervals for Proportions & Differences"),
    "confidence-intervals-for-proportions-and-differences--solutions.html":
        ("../../confidence-intervals-for-proportions-and-differences.html#challenges", "Back to the book", "Chapter 73 · Confidence Intervals for Proportions & Differences"),
    "margin-of-error.html":
        ("../../margin-of-error.html#notebook", "Back to the book", "Chapter 74 · Margin of Error"),
    "margin-of-error--solutions.html":
        ("../../margin-of-error.html#challenges", "Back to the book", "Chapter 74 · Margin of Error"),
    "resampling-and-simulation.html":
        ("../../resampling-and-simulation.html#notebook", "Back to the book", "Chapter 75 · Resampling & Simulation"),
    "resampling-and-simulation--solutions.html":
        ("../../resampling-and-simulation.html#challenges", "Back to the book", "Chapter 75 · Resampling & Simulation"),
    "the-logic-of-hypothesis-testing.html":
        ("../../the-logic-of-hypothesis-testing.html#notebook", "Back to the book", "Chapter 76 · The Logic of Hypothesis Testing"),
    "the-logic-of-hypothesis-testing--solutions.html":
        ("../../the-logic-of-hypothesis-testing.html#challenges", "Back to the book", "Chapter 76 · The Logic of Hypothesis Testing"),
    "significance-p-values-and-errors.html":
        ("../../significance-p-values-and-errors.html#notebook", "Back to the book", "Chapter 77 · Significance, p-values &amp; Errors"),
    "significance-p-values-and-errors--solutions.html":
        ("../../significance-p-values-and-errors.html#challenges", "Back to the book", "Chapter 77 · Significance, p-values &amp; Errors"),
    "z-tests.html":
        ("../../z-tests.html#notebook", "Back to the book", "Chapter 78 · z-Tests"),
    "z-tests--solutions.html":
        ("../../z-tests.html#challenges", "Back to the book", "Chapter 78 · z-Tests"),
    "t-tests.html":
        ("../../t-tests.html#notebook", "Back to the book", "Chapter 79 · t-Tests"),
    "t-tests--solutions.html":
        ("../../t-tests.html#challenges", "Back to the book", "Chapter 79 · t-Tests"),
    "anova.html":
        ("../../anova.html#notebook", "Back to the book", "Chapter 80 · ANOVA"),
    "anova--solutions.html":
        ("../../anova.html#challenges", "Back to the book", "Chapter 80 · ANOVA"),
    "chi-square-tests.html":
        ("../../chi-square-tests.html#notebook", "Back to the book", "Chapter 81 · Chi-Square Tests"),
    "chi-square-tests--solutions.html":
        ("../../chi-square-tests.html#challenges", "Back to the book", "Chapter 81 · Chi-Square Tests"),
    "nonparametric-tests.html":
        ("../../nonparametric-tests.html#notebook", "Back to the book", "Chapter 82 · Nonparametric Tests"),
    "nonparametric-tests--solutions.html":
        ("../../nonparametric-tests.html#challenges", "Back to the book", "Chapter 82 · Nonparametric Tests"),
    "choosing-the-right-test.html":
        ("../../choosing-the-right-test.html#notebook", "Back to the book", "Chapter 83 · Choosing the Right Test"),
    "choosing-the-right-test--solutions.html":
        ("../../choosing-the-right-test.html#challenges", "Back to the book", "Chapter 83 · Choosing the Right Test"),
    "a-b-testing-and-online-experiments.html":
        ("../../a-b-testing-and-online-experiments.html#notebook", "Back to the book", "Chapter 84 · A/B Testing &amp; Online Experiments"),
    "a-b-testing-and-online-experiments--solutions.html":
        ("../../a-b-testing-and-online-experiments.html#challenges", "Back to the book", "Chapter 84 · A/B Testing &amp; Online Experiments"),
    "review-and-choosing-the-right-test.html":
        ("../../review-and-choosing-the-right-test.html#notebook", "Back to the book", "Chapter 85 · Review &amp; Choosing the Right Test"),
    "case-study-a-web-a-b-test.html":
        ("../../case-study-a-web-a-b-test.html#notebook", "Back to the book", "Chapter 86 · Case Study: A Web A/B Test"),
    "case-study-comparing-marketing-channels.html":
        ("../../case-study-comparing-marketing-channels.html#notebook", "Back to the book", "Chapter 87 · Case Study: Comparing Marketing Channels"),
    "case-study-a-clinical-trial.html":
        ("../../case-study-a-clinical-trial.html#notebook", "Back to the book", "Chapter 88 · Case Study: A Clinical Trial"),
    "case-study-a-customer-satisfaction-survey.html":
        ("../../case-study-a-customer-satisfaction-survey.html#notebook", "Back to the book", "Chapter 89 · Case Study: A Customer Satisfaction Survey"),
    "case-study-manufacturing-quality.html":
        ("../../case-study-manufacturing-quality.html#notebook", "Back to the book", "Chapter 90 · Case Study: Manufacturing Quality"),
    "covariance.html":
        ("../../covariance.html#notebook", "Back to the book", "Chapter 92 · Covariance"),
    "covariance--solutions.html":
        ("../../covariance.html#challenges", "Back to the book", "Chapter 92 · Covariance"),
    "correlation-coefficients.html":
        ("../../correlation-coefficients.html#notebook", "Back to the book", "Chapter 93 · Correlation Coefficients"),
    "correlation-coefficients--solutions.html":
        ("../../correlation-coefficients.html#challenges", "Back to the book", "Chapter 93 · Correlation Coefficients"),
    "correlation-vs-causation.html":
        ("../../correlation-vs-causation.html#notebook", "Back to the book", "Chapter 94 · Correlation vs. Causation"),
    "correlation-vs-causation--solutions.html":
        ("../../correlation-vs-causation.html#challenges", "Back to the book", "Chapter 94 · Correlation vs. Causation"),
    "simple-linear-regression.html":
        ("../../simple-linear-regression.html#notebook", "Back to the book", "Chapter 95 · Simple Linear Regression"),
    "simple-linear-regression--solutions.html":
        ("../../simple-linear-regression.html#challenges", "Back to the book", "Chapter 95 · Simple Linear Regression"),
    "the-ols-framework.html":
        ("../../the-ols-framework.html#notebook", "Back to the book", "Chapter 96 · The OLS Framework"),
    "the-ols-framework--solutions.html":
        ("../../the-ols-framework.html#challenges", "Back to the book", "Chapter 96 · The OLS Framework"),
    "multiple-linear-regression.html":
        ("../../multiple-linear-regression.html#notebook", "Back to the book", "Chapter 97 · Multiple Linear Regression"),
    "multiple-linear-regression--solutions.html":
        ("../../multiple-linear-regression.html#challenges", "Back to the book", "Chapter 97 · Multiple Linear Regression"),
    "regression-assumptions-and-diagnostics.html":
        ("../../regression-assumptions-and-diagnostics.html#notebook", "Back to the book", "Chapter 98 · Regression Assumptions & Diagnostics"),
    "regression-assumptions-and-diagnostics--solutions.html":
        ("../../regression-assumptions-and-diagnostics.html#challenges", "Back to the book", "Chapter 98 · Regression Assumptions & Diagnostics"),
    "logistic-regression.html":
        ("../../logistic-regression.html#notebook", "Back to the book", "Chapter 99 · Logistic Regression"),
    "logistic-regression--solutions.html":
        ("../../logistic-regression.html#challenges", "Back to the book", "Chapter 99 · Logistic Regression"),
    "regularization-and-flexible-models.html":
        ("../../regularization-and-flexible-models.html#notebook", "Back to the book", "Chapter 100 · Regularization & Flexible Models"),
    "regularization-and-flexible-models--solutions.html":
        ("../../regularization-and-flexible-models.html#challenges", "Back to the book", "Chapter 100 · Regularization & Flexible Models"),
    "generalized-linear-models.html":
        ("../../generalized-linear-models.html#notebook", "Back to the book", "Chapter 101 · Generalized Linear Models"),
    "generalized-linear-models--solutions.html":
        ("../../generalized-linear-models.html#challenges", "Back to the book", "Chapter 101 · Generalized Linear Models"),
    "econometrics-and-panel-data.html":
        ("../../econometrics-and-panel-data.html#notebook", "Back to the book", "Chapter 102 · Econometrics & Panel Data"),
    "econometrics-and-panel-data--solutions.html":
        ("../../econometrics-and-panel-data.html#challenges", "Back to the book", "Chapter 102 · Econometrics & Panel Data"),
    "case-study-predicting-ames-house-prices.html":
        ("../../case-study-predicting-ames-house-prices.html#notebook", "Back to the book", "Chapter 103 · Case Study: Predicting Ames House Prices"),
    "case-study-predicting-ames-house-prices--take-it-further.html":
        ("../../case-study-predicting-ames-house-prices.html#challenges", "Back to the book", "Chapter 103 · Take It Further"),
    "case-study-logistic-regression-in-action.html":
        ("../../case-study-logistic-regression-in-action.html#notebook", "Back to the book", "Chapter 104 · Case Study: Logistic Regression in Action"),
    "case-study-logistic-regression-in-action--take-it-further.html":
        ("../../case-study-logistic-regression-in-action.html#challenges", "Back to the book", "Chapter 104 · Take It Further"),
    "case-study-forecasting-daily-bike-share-demand.html":
        ("../../case-study-forecasting-daily-bike-share-demand.html#notebook", "Back to the book", "Chapter 105 · Case Study: Forecasting Daily Bike-Share Demand"),
    "case-study-forecasting-daily-bike-share-demand--take-it-further.html":
        ("../../case-study-forecasting-daily-bike-share-demand.html#challenges", "Back to the book", "Chapter 105 · Take It Further"),
    "case-study-predicting-medical-charges.html":
        ("../../case-study-predicting-medical-charges.html#notebook", "Back to the book", "Chapter 106 · Case Study: Predicting Medical Charges"),
    "case-study-predicting-medical-charges--take-it-further.html":
        ("../../case-study-predicting-medical-charges.html#challenges", "Back to the book", "Chapter 106 · Take It Further"),
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
    "structural-equation-modeling-and-mixed-models.html":
        ("../../structural-equation-modeling-and-mixed-models.html#notebook", "Back to the book", "Chapter 145 · Structural Equation Modeling &amp; Mixed Models"),
    "structural-equation-modeling-and-mixed-models--solutions.html":
        ("../../structural-equation-modeling-and-mixed-models.html#challenges", "Back to the book", "Chapter 145 · Challenge solutions"),
    "deep-learning-primer.html":
        ("../../deep-learning-primer.html#notebook", "Back to the book", "Chapter 146 · Deep Learning Primer"),
    "deep-learning-primer--solutions.html":
        ("../../deep-learning-primer.html#challenges", "Back to the book", "Chapter 146 · Challenge solutions"),
    "recommendation-systems.html":
        ("../../recommendation-systems.html#notebook", "Back to the book", "Chapter 147 · Recommendation Systems"),
    "recommendation-systems--solutions.html":
        ("../../recommendation-systems.html#challenges", "Back to the book", "Chapter 147 · Challenge solutions"),
    "nlp-and-large-language-models.html":
        ("../../nlp-and-large-language-models.html#notebook", "Back to the book", "Chapter 148 · NLP &amp; Large Language Models"),
    "nlp-and-large-language-models--solutions.html":
        ("../../nlp-and-large-language-models.html#challenges", "Back to the book", "Chapter 148 · Challenge solutions"),
    "big-data-and-scaling.html":
        ("../../big-data-and-scaling.html#notebook", "Back to the book", "Chapter 149 · Big Data &amp; Scaling"),
    "big-data-and-scaling--solutions.html":
        ("../../big-data-and-scaling.html#challenges", "Back to the book", "Chapter 149 · Challenge solutions"),
    "from-model-to-production-mlops.html":
        ("../../from-model-to-production-mlops.html#notebook", "Back to the book", "Chapter 150 · From Model to Production (MLOps)"),
    "from-model-to-production-mlops--solutions.html":
        ("../../from-model-to-production-mlops.html#challenges", "Back to the book", "Chapter 150 · Challenge solutions"),
    "python-for-data-analysis--1-python-foundations.html":
        ("../../python-for-data-analysis.html#notebooks", "Back to the book", "Chapter 151 · Notebook 1 · Python Foundations"),
    "python-for-data-analysis--2-numpy.html":
        ("../../python-for-data-analysis.html#notebooks", "Back to the book", "Chapter 151 · Notebook 2 · NumPy"),
    "python-for-data-analysis--3-pandas-essentials.html":
        ("../../python-for-data-analysis.html#notebooks", "Back to the book", "Chapter 151 · Notebook 3 · pandas Essentials"),
    "python-for-data-analysis--4-reshaping-and-aggregation.html":
        ("../../python-for-data-analysis.html#notebooks", "Back to the book", "Chapter 151 · Notebook 4 · Reshaping &amp; Aggregating"),
    "python-for-data-analysis--5-visualization.html":
        ("../../python-for-data-analysis.html#notebooks", "Back to the book", "Chapter 151 · Notebook 5 · Visualization"),
    "python-for-data-analysis--solutions.html":
        ("../../python-for-data-analysis.html#challenges", "Back to the book", "Chapter 151 · Challenge solutions"),
    "sql-and-databases--1-foundations.html":
        ("../../sql-and-databases.html#notebooks", "Back to the book", "Chapter 154 · Notebook 1 · SQL Foundations"),
    "sql-and-databases--2-aggregation.html":
        ("../../sql-and-databases.html#notebooks", "Back to the book", "Chapter 154 · Notebook 2 · Aggregation"),
    "sql-and-databases--3-joins.html":
        ("../../sql-and-databases.html#notebooks", "Back to the book", "Chapter 154 · Notebook 3 · Joins"),
    "sql-and-databases--4-window-functions.html":
        ("../../sql-and-databases.html#notebooks", "Back to the book", "Chapter 154 · Notebook 4 · Window Functions"),
    "sql-and-databases--5-subqueries-and-pandas.html":
        ("../../sql-and-databases.html#notebooks", "Back to the book", "Chapter 154 · Notebook 5 · Subqueries &amp; pandas"),
    "sql-and-databases--solutions.html":
        ("../../sql-and-databases.html#challenges", "Back to the book", "Chapter 154 · Challenge solutions"),
    "reproducibility-and-version-control--1-reproducibility.html":
        ("../../reproducibility-and-version-control.html#notebooks", "Back to the book", "Chapter 156 · Notebook 1 · Reproducibility"),
    "reproducibility-and-version-control--2-project-structure.html":
        ("../../reproducibility-and-version-control.html#notebooks", "Back to the book", "Chapter 156 · Notebook 2 · Project Structure"),
    "reproducibility-and-version-control--3-git-basics.html":
        ("../../reproducibility-and-version-control.html#notebooks", "Back to the book", "Chapter 156 · Notebook 3 · Git Basics"),
    "reproducibility-and-version-control--4-branching-and-merging.html":
        ("../../reproducibility-and-version-control.html#notebooks", "Back to the book", "Chapter 156 · Notebook 4 · Branching &amp; Merging"),
    "reproducibility-and-version-control--5-experiment-tracking.html":
        ("../../reproducibility-and-version-control.html#notebooks", "Back to the book", "Chapter 156 · Notebook 5 · Experiment Tracking"),
    "reproducibility-and-version-control--solutions.html":
        ("../../reproducibility-and-version-control.html#challenges", "Back to the book", "Chapter 156 · Challenge solutions"),
    "communicating-insights--A-chart-toolkit.html":
        ("../../communicating-insights-and-storytelling-with-data.html#notebooks", "Back to the book", "Chapter 157 · Toolkit A · Chart Recipes"),
    "communicating-insights--B-table-toolkit.html":
        ("../../communicating-insights-and-storytelling-with-data.html#notebooks", "Back to the book", "Chapter 157 · Toolkit B · Table Recipes"),
    "communicating-insights--1-executive-report.html":
        ("../../communicating-insights-and-storytelling-with-data.html#notebooks", "Back to the book", "Chapter 157 · Report 1 · Executive One-Pager"),
    "communicating-insights--2-ab-test-report.html":
        ("../../communicating-insights-and-storytelling-with-data.html#notebooks", "Back to the book", "Chapter 157 · Report 2 · A/B Test Readout"),
    "communicating-insights--3-analytical-report.html":
        ("../../communicating-insights-and-storytelling-with-data.html#notebooks", "Back to the book", "Chapter 157 · Report 3 · Analytical Report"),
    "communicating-insights--solutions.html":
        ("../../communicating-insights-and-storytelling-with-data.html#challenges", "Back to the book", "Chapter 157 · Challenge solutions"),
    "data-ethics--1-measuring-fairness.html":
        ("../../data-ethics-bias-and-fairness.html#notebooks", "Back to the book", "Chapter 158 · Notebook 1 · Measuring Bias and Fairness"),
    "data-ethics--2-fairness-tradeoff.html":
        ("../../data-ethics-bias-and-fairness.html#notebooks", "Back to the book", "Chapter 158 · Notebook 2 · The Fairness-Accuracy Tradeoff"),
    "data-ethics--solutions.html":
        ("../../data-ethics-bias-and-fairness.html#challenges", "Back to the book", "Chapter 158 · Challenge solutions"),
    "capstone-coffee-fill-weight.html":
        ("../../capstone-coffee-fill-weight.html#notebook", "Back to the book", "Chapter 160 · One-Sample t-Test: Coffee Fill Weight"),
    "capstone-onboarding-productivity.html":
        ("../../capstone-onboarding-productivity.html#notebook", "Back to the book", "Chapter 161 · Two-Sample t-Test: A New Onboarding Program"),
    "capstone-blood-pressure-before-after.html":
        ("../../capstone-blood-pressure-before-after.html#notebook", "Back to the book", "Chapter 162 · Paired t-Test: Blood Pressure Before &amp; After"),
    "capstone-heart-disease-markers.html":
        ("../../capstone-heart-disease-markers.html#notebook", "Back to the book", "Chapter 163 · Multiple Comparisons: Screening Heart-Disease Markers"),
    "capstone-teaching-methods-exam-scores.html":
        ("../../capstone-teaching-methods-exam-scores.html#notebook", "Back to the book", "Chapter 164 · One-Way ANOVA: Three Teaching Methods"),
    "capstone-cognitive-training-over-time.html":
        ("../../capstone-cognitive-training-over-time.html#notebook", "Back to the book", "Chapter 165 · Repeated-Measures ANOVA: Cognitive Training Over Time"),
    "capstone-plant-growth-two-factors.html":
        ("../../capstone-plant-growth-two-factors.html#notebook", "Back to the book", "Chapter 166 · Two-Way ANOVA: Fertilizer and Sunlight"),
    "capstone-commute-mode-by-region.html":
        ("../../capstone-commute-mode-by-region.html#notebook", "Back to the book", "Chapter 167 · Chi-Square Test of Independence: Commute Mode by Region"),
    "capstone-website-visits-by-weekday.html":
        ("../../capstone-website-visits-by-weekday.html#notebook", "Back to the book", "Chapter 168 · Chi-Square Goodness-of-Fit: Weekday Traffic"),
    "capstone-email-signup-rates.html":
        ("../../capstone-email-signup-rates.html#notebook", "Back to the book", "Chapter 169 · Proportion Tests: Email Signup Rates"),
    "capstone-study-hours-and-scores.html":
        ("../../capstone-study-hours-and-scores.html#notebook", "Back to the book", "Chapter 170 · Pearson Correlation: Study Hours and Scores"),
    "capstone-satisfaction-and-loyalty.html":
        ("../../capstone-satisfaction-and-loyalty.html#notebook", "Back to the book", "Chapter 171 · Spearman Correlation: Satisfaction and Loyalty"),
    "capstone-judges-product-rankings.html":
        ("../../capstone-judges-product-rankings.html#notebook", "Back to the book", "Chapter 172 · Kendall's Tau: Two Judges' Rankings"),
    "capstone-pain-relief-two-treatments.html":
        ("../../capstone-pain-relief-two-treatments.html#notebook", "Back to the book", "Chapter 173 · Mann-Whitney U: Comparing Two Pain Treatments"),
    "capstone-service-ratings-before-after.html":
        ("../../capstone-service-ratings-before-after.html#notebook", "Back to the book", "Chapter 174 · Wilcoxon Signed-Rank: Service Ratings Before &amp; After"),
    "capstone-store-ratings-across-locations.html":
        ("../../capstone-store-ratings-across-locations.html#notebook", "Back to the book", "Chapter 175 · Kruskal-Wallis: Ratings Across Four Stores"),
    "capstone-stratified-customer-survey.html":
        ("../../capstone-stratified-customer-survey.html#notebook", "Back to the book", "Chapter 177 · Stratified Survey: A National Customer Study"),
    "capstone-cluster-sampling-schools.html":
        ("../../capstone-cluster-sampling-schools.html#notebook", "Back to the book", "Chapter 178 · Cluster Sampling: Schools and Students"),
    "capstone-web-scraping-job-postings.html":
        ("../../capstone-web-scraping-job-postings.html#notebook", "Back to the book", "Chapter 179 · Web Scraping as a Sampling Frame: Job Postings"),
    "capstone-repairing-an-online-panel.html":
        ("../../capstone-repairing-an-online-panel.html#notebook", "Back to the book", "Chapter 180 · When the Sample Is Not Random: Repairing a Panel"),
    "capstone-designing-an-ab-test.html":
        ("../../capstone-designing-an-ab-test.html#notebook", "Back to the book", "Chapter 181 · Designing an A/B Test Properly"),
    "capstone-designing-a-factorial-experiment.html":
        ("../../capstone-designing-a-factorial-experiment.html#notebook", "Back to the book", "Chapter 182 · Designing a Factorial Experiment"),
    "capstone-propensity-score-matching.html":
        ("../../capstone-propensity-score-matching.html#notebook", "Back to the book", "Chapter 183 · Propensity Scores: Matching and Weighting"),
    "capstone-regression-discontinuity-and-iv.html":
        ("../../capstone-regression-discontinuity-and-iv.html#notebook", "Back to the book", "Chapter 184 · Regression Discontinuity and Instrumental Variables"),
    "capstone-pay-equity-review.html":
        ("../../capstone-pay-equity-review.html#notebook", "Back to the book", "Chapter 186 · Multiple Regression Done Properly: A Pay Equity Review"),
    "capstone-regression-diagnostics-and-remedies.html":
        ("../../capstone-regression-diagnostics-and-remedies.html#notebook", "Back to the book", "Chapter 187 · When the Assumptions Fail: Diagnostics and Remedies"),
    "capstone-clinical-risk-scoring.html":
        ("../../capstone-clinical-risk-scoring.html#notebook", "Back to the book", "Chapter 188 · Logistic Regression for Decisions: Clinical Risk Scoring"),
    "capstone-emergency-department-visits.html":
        ("../../capstone-emergency-department-visits.html#notebook", "Back to the book", "Chapter 189 · Counts and Rates: Emergency Department Visits"),
    "capstone-credit-card-fraud.html":
        ("../../capstone-credit-card-fraud.html#notebook", "Back to the book", "Chapter 191 · Imbalanced Classification: Credit Card Fraud"),
    "capstone-churn-prediction-explainability.html":
        ("../../capstone-churn-prediction-explainability.html#notebook", "Back to the book", "Chapter 192 · Churn Prediction and Explainability"),
    "capstone-gradient-boosting-regression.html":
        ("../../capstone-gradient-boosting-regression.html#notebook", "Back to the book", "Chapter 193 · Gradient Boosting for Tabular Regression"),
    "capstone-pca-survey-battery.html":
        ("../../capstone-pca-survey-battery.html#notebook", "Back to the book", "Chapter 194 · Principal Component Analysis: A Survey Battery"),
    "capstone-clustering-choosing-k.html":
        ("../../capstone-clustering-choosing-k.html#notebook", "Back to the book", "Chapter 195 · Clustering: Choosing k Honestly"),
    "capstone-anomaly-detection-unlabeled.html":
        ("../../capstone-anomaly-detection-unlabeled.html#notebook", "Back to the book", "Chapter 196 · Anomaly Detection Without Labels"),
    "capstone-reinforcement-learning-pricing.html":
        ("../../capstone-reinforcement-learning-pricing.html#notebook", "Back to the book", "Chapter 197 · Reinforcement Learning: Dynamic Pricing"),
    "capstone-hierarchical-forecasting.html":
        ("../../capstone-hierarchical-forecasting.html#notebook", "Back to the book", "Chapter 199 · Hierarchical Forecasting: Store, Region, National"),
    "capstone-intermittent-demand-spare-parts.html":
        ("../../capstone-intermittent-demand-spare-parts.html#notebook", "Back to the book", "Chapter 200 · Intermittent Demand: Spare Parts"),
    "capstone-forecast-backtesting.html":
        ("../../capstone-forecast-backtesting.html#notebook", "Back to the book", "Chapter 201 · Backtesting and Honest Model Selection"),
    "capstone-missing-data-imputation.html":
        ("../../capstone-missing-data-imputation.html#notebook", "Back to the book", "Chapter 202 · Missing Data: What Dropping Rows Costs You"),
    "capstone-survival-analysis-time-to-event.html":
        ("../../capstone-survival-analysis-time-to-event.html#notebook", "Back to the book", "Chapter 203 · Survival Analysis: Time to Event"),
    "capstone-fairness-audit.html":
        ("../../capstone-fairness-audit.html#notebook", "Back to the book", "Chapter 204 · A Fairness Audit"),
    "the-whole-pipeline-reflection-and-next-steps.html":
        ("../../the-whole-pipeline-reflection-and-next-steps.html#notebook", "Back to the book",
         "Chapter 205 · The Whole Pipeline: Reflection and Next Steps"),
}

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/"
REPO = "johnfisher-ai/Statistics-Data-Science-AI-Visual-Book"
BOOK_SHORT = "Statistics, Data Science and AI"
BOOK_FULL = "Statistics, Data Science and AI: A Visual Handbook"

# Everything the script adds sits between these markers or in the two cards, so a later run can
# take it out again and put the current version in.
HEAD_START, HEAD_END = "<!-- book-head -->", "<!-- /book-head -->"

CSS = (
    "<style id=\"book-notebook-css\">"
    # left-align tables like Colab, where nbconvert centers them
    ".jp-RenderedHTMLCommon table{margin-left:0 !important;margin-right:auto !important;}"
    # nbconvert shows the In and Out prompts at half opacity in light blue and orange (about 2:1);
    # these shades of the same hues read at 5:1 or more on the white page and the gray code box
    ":root{--jp-cell-inprompt-font-color:#2766a0;--jp-cell-outprompt-font-color:#a64d32;"
    "--jp-cell-prompt-not-active-opacity:1;}"
    # code highlighting: these four of jupyterlab_pygments' colors read below 4.5:1 on the gray code box
    ":root{--jp-mirror-editor-comment-color:#3a7474;--jp-mirror-editor-number-color:#007e00;"
    "--jp-mirror-editor-operator-color:#a10bff;--jp-mirror-editor-error-color:#db0000;}"
    # the footer line in the last cell, #8b94b3 (3:1) on white, takes the chapters' faint ink
    ".jp-RenderedHTMLCommon [style*=\"color:#8b94b3\"]{color:#666f8e !important;}"
    # a heading moved up a level keeps the size of the level it had
    ".jp-RenderedHTMLCommon .book-was-h3{font-size:var(--jp-content-font-size3);}"
    ".jp-RenderedHTMLCommon .book-was-h4{font-size:var(--jp-content-font-size2);}"
    ".jp-RenderedHTMLCommon .book-was-h5{font-size:var(--jp-content-font-size1);}"
    ".jp-RenderedHTMLCommon .book-was-h6{font-size:var(--jp-content-font-size0);}"
    # links in the notebook's text are underlined, as in the chapters
    ".jp-RenderedHTMLCommon a:link,.jp-RenderedHTMLCommon a:visited{text-decoration:underline;}"
    # the card, in the look of the chapters' previous and next cards
    ".book-nav{max-width:760px;margin:18px auto;"
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}"
    ".book-back{display:flex;align-items:center;gap:12px;text-decoration:none;border:1px solid #e6e9f2;"
    "border-radius:13px;padding:15px 20px;background:#ffffff;box-shadow:0 6px 18px rgba(20,30,80,0.06);}"
    ".book-back:hover{border-color:#7c3aed;}"
    ".book-back-arrow{font-size:22px;color:#0e7490;line-height:1;}"
    ".book-back-kicker{display:block;font-size:11px;font-weight:700;letter-spacing:0.08em;"
    "text-transform:uppercase;color:#666f8e;}"
    ".book-back-title{font-weight:700;color:#1a2138;font-size:15px;}"
    ".book-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px;}"
    ".book-btn{display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:8px;"
    "font-size:14px;font-weight:600;text-decoration:none;color:#1a2138;background:#ffffff;"
    "border:1px solid #cdd3e3;}"
    ".book-btn:hover{background:#f4f6fb;}"
    ".book-btn-colab{background:#f9ab00;border-color:#f9ab00;font-weight:700;}"
    ".book-btn-colab:hover{background:#ffbd2e;}"
    ".book-back:focus-visible,.book-btn:focus-visible{outline:2px solid #0e7490;outline-offset:2px;}"
    # the hero title made a heading is drawn as the div it was: inherited type and no heading margins,
    # with the hero's inline style on top
    ".jp-RenderedHTMLCommon h1.book-hero-title{font:inherit;color:inherit;letter-spacing:inherit;"
    "margin:0;border:0;padding:0;}"
    # on a phone the three buttons sit closer, so the first two share a line, hero titles of up to
    # 40 px come down to 28, and a long word wraps rather than pushing its cell sideways, as does code
    # in a table cell, which would otherwise widen the whole table
    "@media (max-width:480px){.book-actions{gap:8px;}.book-btn{padding:8px 13px;font-size:13px;}"
    "main>.jp-Cell:first-of-type [style*=\"font-weight:900\"]{font-size:28px !important;}"
    ".jp-RenderedMarkdown{overflow-wrap:break-word;}"
    ".jp-RenderedMarkdown td code,.jp-RenderedMarkdown th code{overflow-wrap:anywhere;}}"
    "</style>"
)

# What the first version of this script added, removed before the current version goes in.
OLD_PIECES = [
    '<link rel="icon" href="../../../assets/img/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="../../../assets/img/apple-touch-icon.png">\n',
    '<style id="book-table-align">.jp-RenderedHTMLCommon table{margin-left:0 !important;'
    'margin-right:auto !important;}</style>\n',
]
# the first version's cards: one after <body ...> and a newline, one before a newline and </body>
OLD_TOP = re.compile(r'(<body[^>]*>)\n<a class="book-backlink" .*?</a>', re.S)
OLD_BOTTOM = re.compile(r'<a class="book-backlink" .*?</a>\n(?=</body>)', re.S)
# the current cards: one just before <main>, one just after </main>
NAV_TOP = re.compile(r'<nav class="book-nav" .*?</nav>\n(?=<main>)', re.S)
NAV_BOTTOM = re.compile(r'(?<=</main>)\n<nav class="book-nav" .*?</nav>', re.S)
# the hero cell's title, as nbconvert writes it and as this script makes it a heading
HERO_DIV = re.compile(r'<div (style="[^"]*font-weight:\s*900[^"]*")>(.*?)</div>', re.S)
HERO_H1 = re.compile(r'<h1 class="book-hero-title" (style="[^"]*")>(.*?)</h1>', re.S)
# a heading this script moved up a level, and a pandas header's blank corner cell
MOVED = re.compile(r'<h([1-6]) class="book-was-h([1-6])"([^>]*)>(.*?)</h\1>', re.S)
HEADING = re.compile(r'<h([1-6])((?:\s[^>]*)?)>(.*?)</h\1>', re.S)
THEAD = re.compile(r"<thead>.*?</thead>", re.S)
BLANK_TD = '<td class="book-blank-th"></td>'
HEAD_BLOCK = re.compile(re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END) + r"\n", re.S)


def manifest():
    """Each chapter's number and title from toc.html, by slug. Numbers come from position."""
    toc = open(os.path.join(BOOK, "toc.html"), encoding="utf-8").read()
    parts = toc[toc.index("const PARTS ="):toc.index("const AVAILABLE")]
    found = re.findall(r'\{(?:n:\s*\d+,\s*)?slug:"([^"]+)",\s*t:"([^"]*)"', parts)
    return {slug: (i + 1, htmllib.unescape(t).replace("★", "").strip()) for i, (slug, t) in enumerate(found)}


def plain(fragment):
    """Visible text of a bit of the hero's HTML, without tags, entities or emoji."""
    text = htmllib.unescape(re.sub(r"<[^>]+>", "", fragment))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "So" and ch not in "\ufe0f\u200d")
    return re.sub(r"\s+", " ", text).strip()


def hero(name):
    """The kicker, title and first line of text in the notebook's hero cell."""
    nb = json.load(open(os.path.join(BOOK, "chapters", "notebooks", name + ".ipynb"), encoding="utf-8"))
    src = "".join(nb["cells"][0]["source"])
    kicker = re.search(r'<div style="[^"]*text-transform:\s*uppercase[^"]*">(.*?)</div>', src, re.S)
    title = re.search(r'<(div|h1) style="([^"]*font-weight:\s*900[^"]*)">(.*?)</\1>', src, re.S)
    lines = [plain(t) for t in re.findall(r"<div[^>]*>(.*?)</div>", src[title.end():], re.S)] if title else []
    lines = [t for t in lines if t and "John Fisher" not in t]
    return (plain(kicker.group(1)) if kicker else "", plain(title.group(3)) if title else "", lines[0] if lines else "")


def describe(name, slug, chapters):
    """The page's tab title, link-preview title and description."""
    n, chapter = chapters[slug]
    kicker, title, line = hero(name)
    where = f"Chapter {n}, {chapter}, of {BOOK_FULL}"
    if name == slug:
        kind, lead = "Notebook", f"The companion notebook for {where}."
    elif name.endswith("--solutions"):
        kind, lead = "Solutions", f"Worked solutions to the practice challenges in {where}."
    elif name.endswith("--take-it-further"):
        kind, lead = "Take It Further", f"A take-it-further notebook that extends {where}."
    else:
        # one of several notebooks for a chapter, named in its hero ("Notebook 3 of 5", "Toolkit")
        kind = kicker.split("·")[-1].strip()
        if kind == "Toolkit":
            lead = f"A toolkit notebook for {where}."
        elif kind.startswith("Report"):
            lead = f"The notebook behind {kind.lower()} in {where}."
        else:
            lead = f"{kind} for {where}."
        chapter = title
    tab = f"Ch {n} · {chapter} · {kind} — {BOOK_SHORT}"
    preview = f"{chapter} · Chapter {n} · {kind}"
    return tab, preview, (lead + " " + line).strip()


def head_block(name, preview, description):
    a = lambda v: htmllib.escape(v, quote=True)
    url = SITE + "chapters/notebooks/html/" + name + ".html"
    image = SITE + "assets/img/social-card-v2.png"
    return "\n".join([
        HEAD_START,
        f'<meta name="description" content="{a(description)}">',
        '<meta name="author" content="John Fisher">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:site_name" content="{a(BOOK_FULL)}">',
        f'<meta property="og:title" content="{a(preview)}">',
        f'<meta property="og:description" content="{a(description)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{image}">',
        '<meta property="og:image:width" content="2400">',
        '<meta property="og:image:height" content="1260">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{a(preview)}">',
        f'<meta name="twitter:description" content="{a(description)}">',
        f'<meta name="twitter:image" content="{image}">',
        '<link rel="icon" href="../../../assets/img/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="../../../assets/img/apple-touch-icon.png">',
        CSS,
        HEAD_END,
    ]) + "\n"


def back_link(href, kicker, title):
    return ('<a class="book-back" href="' + href + '">'
            '<span class="book-back-arrow" aria-hidden="true">&#8592;</span>'
            '<span><span class="book-back-kicker">' + kicker + '</span>'
            '<span class="book-back-title">' + title + '</span></span></a>')


def top_card(name, href, kicker, title):
    ipynb = "blob/main/chapters/notebooks/" + name + ".ipynb"
    return ('<nav class="book-nav" aria-label="Notebook links">' + back_link(href, kicker, title) +
            '<div class="book-actions">'
            '<a class="book-btn book-btn-colab" href="https://colab.research.google.com/github/' + REPO + '/' + ipynb +
            '" target="_blank" rel="noopener"><span aria-hidden="true">&#9654;</span> Open in Colab</a>'
            '<a class="book-btn" href="../' + name + '.ipynb" download>'
            '<span aria-hidden="true">&#11015;</span> Download notebook</a>'
            '<a class="book-btn" href="https://github.com/' + REPO + '/' + ipynb +
            '" target="_blank" rel="noopener">View on GitHub</a>'
            '</div></nav>')


def bottom_card(href, kicker, title):
    return '<nav class="book-nav" aria-label="Back to the book">' + back_link(href, kicker, title) + '</nav>'


def strip(html):
    """The page as nbconvert wrote it: everything this script added, old or current, taken out."""
    html = HEAD_BLOCK.sub("", html)
    for piece in OLD_PIECES:
        html = html.replace(piece, "")
    html = html.replace(BLANK_TD, "<th></th>")
    html = MOVED.sub(r"<h\2\3>\4</h\2>", html)
    html = HERO_H1.sub(r"<div \1>\2</div>", html)
    html = OLD_BOTTOM.sub("", OLD_TOP.sub(r"\1", html))
    return NAV_BOTTOM.sub("", NAV_TOP.sub("", html))


def outline(html):
    """Move up any heading in <main> that skips a level, and turn blank header corners into plain cells."""
    start, end = html.index("<main>"), html.rindex("</main>")
    body, prev, pos, out = html[start:end], 0, 0, []
    for m in HEADING.finditer(body):
        level, attrs = int(m.group(1)), m.group(2)
        if prev and level > prev + 1 and "class=" not in attrs:
            out += [body[pos:m.start()], f'<h{prev + 1} class="book-was-h{level}"{attrs}>{m.group(3)}</h{prev + 1}>']
            pos, level = m.end(), prev + 1
        prev = level
    body = "".join(out) + body[pos:]
    body = THEAD.sub(lambda m: m.group(0).replace("<th></th>", BLANK_TD), body)
    return html[:start] + body + html[end:]


def inject(path, name, href, kicker, title, chapters):
    old = open(path, encoding="utf-8").read()
    html = strip(old)
    slug = re.match(r"\.\./\.\./([^#]+)\.html#", href).group(1)
    tab, preview, description = describe(name, slug, chapters)
    html = re.sub(r"<title>.*?</title>", lambda m: "<title>" + htmllib.escape(tab, quote=False) + "</title>",
                  html, count=1, flags=re.S)
    html = html.replace("</head>", head_block(name, preview, description) + "</head>", 1)
    if not re.search(r"<h1[\s>]", html):
        html = HERO_DIV.sub(r'<h1 class="book-hero-title" \1>\2</h1>', html, count=1)
    html = outline(html)
    html = html.replace("<main>", top_card(name, href, kicker, title) + "\n<main>", 1)
    end = html.rindex("</main>") + len("</main>")
    html = html[:end] + "\n" + bottom_card(href, kicker, title) + html[end:]
    if html == old:
        return "up to date"
    open(path, "w", encoding="utf-8").write(html)
    return "updated"


def main():
    if not os.path.isdir(HTML_DIR):
        print("No HTML dir yet:", HTML_DIR); return
    chapters = manifest()
    for fname, (href, kicker, title) in MAP.items():
        path = os.path.join(HTML_DIR, fname)
        if os.path.exists(path):
            print(f"{fname}: {inject(path, fname[:-5], href, kicker, title, chapters)}")
        else:
            print(f"{fname}: (not rendered yet, skipped)")

if __name__ == "__main__":
    main()
