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
    "ch104_what_is_ml.html":
        ("../../ch104.html#notebook", "Back to the book", "Chapter 104 · What Is Machine Learning?"),
    "ch104_challenges_solutions.html":
        ("../../ch104.html#quiz", "Back to the book", "Chapter 104 · Take the quiz &amp; aim for 100%"),
    "ch105_ml_workflow.html":
        ("../../ch105.html#notebook", "Back to the book", "Chapter 105 · The Machine Learning Workflow"),
    "ch105_challenges_solutions.html":
        ("../../ch105.html#quiz", "Back to the book", "Chapter 105 · Take the quiz &amp; aim for 100%"),
    "ch106_distance_metrics.html":
        ("../../ch106.html#notebook", "Back to the book", "Chapter 106 · Distance Metrics"),
    "ch106_challenges_solutions.html":
        ("../../ch106.html#quiz", "Back to the book", "Chapter 106 · Take the quiz &amp; aim for 100%"),
    "ch107_core_algorithms.html":
        ("../../ch107.html#notebook", "Back to the book", "Chapter 107 · Core Classification &amp; Regression Algorithms"),
    "ch107_challenges_solutions.html":
        ("../../ch107.html#quiz", "Back to the book", "Chapter 107 · Take the quiz &amp; aim for 100%"),
    "ch108_ensemble_methods.html":
        ("../../ch108.html#notebook", "Back to the book", "Chapter 108 · Ensemble Methods"),
    "ch108_challenges_solutions.html":
        ("../../ch108.html#quiz", "Back to the book", "Chapter 108 · Take the quiz &amp; aim for 100%"),
    "ch109_feature_selection.html":
        ("../../ch109.html#notebook", "Back to the book", "Chapter 109 · Feature Selection"),
    "ch109_challenges_solutions.html":
        ("../../ch109.html#quiz", "Back to the book", "Chapter 109 · Take the quiz &amp; aim for 100%"),
    "ch110_optimization_gradient_descent.html":
        ("../../ch110.html#notebook", "Back to the book", "Chapter 110 · Optimization &amp; Gradient Descent"),
    "ch110_challenges_solutions.html":
        ("../../ch110.html#quiz", "Back to the book", "Chapter 110 · Take the quiz &amp; aim for 100%"),
    "ch111_model_evaluation.html":
        ("../../ch111.html#notebook", "Back to the book", "Chapter 111 · Model Evaluation"),
    "ch111_challenges_solutions.html":
        ("../../ch111.html#quiz", "Back to the book", "Chapter 111 · Take the quiz &amp; aim for 100%"),
    "ch112_model_pitfalls.html":
        ("../../ch112.html#notebook", "Back to the book", "Chapter 112 · Model Pitfalls"),
    "ch112_challenges_solutions.html":
        ("../../ch112.html#quiz", "Back to the book", "Chapter 112 · Take the quiz &amp; aim for 100%"),
    "ch113_interpretability.html":
        ("../../ch113.html#notebook", "Back to the book", "Chapter 113 · Model Interpretability &amp; Explainability"),
    "ch113_challenges_solutions.html":
        ("../../ch113.html#quiz", "Back to the book", "Chapter 113 · Take the quiz &amp; aim for 100%"),
    "ch114_clustering.html":
        ("../../ch114.html#notebook", "Back to the book", "Chapter 114 · Clustering"),
    "ch114_challenges_solutions.html":
        ("../../ch114.html#quiz", "Back to the book", "Chapter 114 · Take the quiz &amp; aim for 100%"),
    "ch115_dimensionality_reduction.html":
        ("../../ch115.html#notebook", "Back to the book", "Chapter 115 · Dimensionality Reduction"),
    "ch115_challenges_solutions.html":
        ("../../ch115.html#quiz", "Back to the book", "Chapter 115 · Take the quiz &amp; aim for 100%"),
    "ch116_association_rules.html":
        ("../../ch116.html#notebook", "Back to the book", "Chapter 116 · Association Rule Mining"),
    "ch116_challenges_solutions.html":
        ("../../ch116.html#quiz", "Back to the book", "Chapter 116 · Take the quiz &amp; aim for 100%"),
    "ch117_anomaly_detection.html":
        ("../../ch117.html#notebook", "Back to the book", "Chapter 117 · Anomaly Detection"),
    "ch117_challenges_solutions.html":
        ("../../ch117.html#quiz", "Back to the book", "Chapter 117 · Take the quiz &amp; aim for 100%"),
    "ch118_reinforcement_learning.html":
        ("../../ch118.html#notebook", "Back to the book", "Chapter 118 · Reinforcement Learning Primer"),
    "ch118_challenges_solutions.html":
        ("../../ch118.html#quiz", "Back to the book", "Chapter 118 · Take the quiz &amp; aim for 100%"),
    "ch119_deep_rl.html":
        ("../../ch119.html#notebook", "Back to the book", "Chapter 119 · Deep RL &amp; Applications"),
    "ch119_challenges_solutions.html":
        ("../../ch119.html#quiz", "Back to the book", "Chapter 119 · Take the quiz &amp; aim for 100%"),
    "ch120_ml_project.html":
        ("../../ch120.html#notebook", "Back to the book", "Chapter 120 · An End-to-End ML Project"),
    "ch120_take_it_further.html":
        ("../../ch120.html#challenges", "Back to the book", "Chapter 120 · Take it further"),
    "ch121_fraud_detection.html":
        ("../../ch121.html#notebook", "Back to the book", "Chapter 121 · Fraud Detection"),
    "ch121_take_it_further.html":
        ("../../ch121.html#challenges", "Back to the book", "Chapter 121 · Take it further"),
    "ch122_predictive_maintenance.html":
        ("../../ch122.html#notebook", "Back to the book", "Chapter 122 · Predictive Maintenance"),
    "ch122_take_it_further.html":
        ("../../ch122.html#challenges", "Back to the book", "Chapter 122 · Take it further"),
    "ch123_segmentation_targeting.html":
        ("../../ch123.html#notebook", "Back to the book", "Chapter 123 · Customer Segmentation &amp; Targeting"),
    "ch123_take_it_further.html":
        ("../../ch123.html#challenges", "Back to the book", "Chapter 123 · Take it further"),
    "ch124_loan_default.html":
        ("../../ch124.html#notebook", "Back to the book", "Chapter 124 · Loan Default Risk"),
    "ch124_take_it_further.html":
        ("../../ch124.html#challenges", "Back to the book", "Chapter 124 · Take it further"),
    "ch125_model_to_decision.html":
        ("../../ch125.html#notebook", "Back to the book", "Chapter 125 · From Model to Decision"),
    "ch125_take_it_further.html":
        ("../../ch125.html#challenges", "Back to the book", "Chapter 125 · Take it further"),
    "ch126_operationalizing.html":
        ("../../ch126.html#notebook", "Back to the book", "Chapter 126 · Operationalizing the Model"),
    "ch126_take_it_further.html":
        ("../../ch126.html#challenges", "Back to the book", "Chapter 126 · Take it further"),
    "ch127_time_series_components.html":
        ("../../ch127.html#notebook", "Back to the book", "Chapter 127 · Components of a Time Series"),
    "ch127_challenges_solutions.html":
        ("../../ch127.html#challenges", "Back to the book", "Chapter 127 · Challenge solutions"),
    "ch128_forecasting_models.html":
        ("../../ch128.html#notebook", "Back to the book", "Chapter 128 · Forecasting Models"),
    "ch128_challenges_solutions.html":
        ("../../ch128.html#challenges", "Back to the book", "Chapter 128 · Challenge solutions"),
    "ch129_volatility_advanced.html":
        ("../../ch129.html#notebook", "Back to the book", "Chapter 129 · Volatility & Advanced Models"),
    "ch129_challenges_solutions.html":
        ("../../ch129.html#challenges", "Back to the book", "Chapter 129 · Challenge solutions"),
    "ch130_forecast_accuracy.html":
        ("../../ch130.html#notebook", "Back to the book", "Chapter 130 · Forecast Accuracy"),
    "ch130_challenges_solutions.html":
        ("../../ch130.html#challenges", "Back to the book", "Chapter 130 · Challenge solutions"),
    "ch131_forecasting_retail_sales.html":
        ("../../ch131.html#notebook", "Back to the book", "Chapter 131 · Forecasting Retail Sales"),
    "ch131_take_it_further.html":
        ("../../ch131.html#challenges", "Back to the book", "Chapter 131 · Take it further"),
    "ch132_volatility_risk.html":
        ("../../ch132.html#notebook", "Back to the book", "Chapter 132 · Financial Volatility & Risk"),
    "ch132_take_it_further.html":
        ("../../ch132.html#challenges", "Back to the book", "Chapter 132 · Take it further"),
    "ch133_energy_demand.html":
        ("../../ch133.html#notebook", "Back to the book", "Chapter 133 · Energy Demand Forecasting"),
    "ch133_take_it_further.html":
        ("../../ch133.html#challenges", "Back to the book", "Chapter 133 · Take it further"),
    "ch134_forecast_to_decision.html":
        ("../../ch134.html#notebook", "Back to the book", "Chapter 134 · From Forecast to Decision"),
    "ch134_take_it_further.html":
        ("../../ch134.html#challenges", "Back to the book", "Chapter 134 · Take it further"),
    "ch135_operationalizing_forecast.html":
        ("../../ch135.html#notebook", "Back to the book", "Chapter 135 · Operationalizing a Forecast"),
    "ch135_take_it_further.html":
        ("../../ch135.html#challenges", "Back to the book", "Chapter 135 · Take it further"),
    "ch136_survey_capstone.html":
        ("../../ch136.html#notebook", "Back to the book", "Chapter 136 · Designing and Analyzing a Survey"),
    "ch136_take_it_further.html":
        ("../../ch136.html#challenges", "Back to the book", "Chapter 136 · Take it further"),
    "ch137_diff_in_diff.html":
        ("../../ch137.html#notebook", "Back to the book", "Chapter 137 · Difference-in-Differences"),
    "ch137_take_it_further.html":
        ("../../ch137.html#challenges", "Back to the book", "Chapter 137 · Take it further"),
    "ch138_paired_prepost.html":
        ("../../ch138.html#notebook", "Back to the book", "Chapter 138 · A Paired Pre/Post Study"),
    "ch138_take_it_further.html":
        ("../../ch138.html#challenges", "Back to the book", "Chapter 138 · Take it further"),
    "ch01_what_is_statistics.html":
        ("../../ch01.html#notebook", "Back to the book", "Chapter 1 · What Is Statistics?"),
    "ch01_challenges_solutions.html":
        ("../../ch01.html#quiz", "Back to the book", "Chapter 1 · Take the quiz &amp; aim for 100%"),
    "ch02_stats_ds_ai.html":
        ("../../ch02.html#notebook", "Back to the book", "Chapter 2 · Statistics, Data Science &amp; AI"),
    "ch02_challenges_solutions.html":
        ("../../ch02.html#quiz", "Back to the book", "Chapter 2 · Take the quiz &amp; aim for 100%"),
    "ch03_data_science_lifecycle.html":
        ("../../ch03.html#notebook", "Back to the book", "Chapter 3 · The Data Science Lifecycle"),
    "ch03_challenges_solutions.html":
        ("../../ch03.html#quiz", "Back to the book", "Chapter 3 · Take the quiz &amp; aim for 100%"),
    "ch04_types_of_data.html":
        ("../../ch04.html#notebook", "Back to the book", "Chapter 4 · Types of Data &amp; Variables"),
    "ch04_challenges_solutions.html":
        ("../../ch04.html#quiz", "Back to the book", "Chapter 4 · Take the quiz &amp; aim for 100%"),
    "ch05_levels_of_measurement.html":
        ("../../ch05.html#notebook", "Back to the book", "Chapter 5 · Levels of Measurement"),
    "ch05_challenges_solutions.html":
        ("../../ch05.html#quiz", "Back to the book", "Chapter 5 · Take the quiz &amp; aim for 100%"),
    "ch06_population_vs_sample.html":
        ("../../ch06.html#notebook", "Back to the book", "Chapter 6 · Population vs. Sample"),
    "ch06_challenges_solutions.html":
        ("../../ch06.html#quiz", "Back to the book", "Chapter 6 · Take the quiz &amp; aim for 100%"),
    "ch07_math_refresher.html":
        ("../../ch07.html#notebook", "Back to the book", "Chapter 7 · Math Refresher for Statistics"),
    "ch07_challenges_solutions.html":
        ("../../ch07.html#quiz", "Back to the book", "Chapter 7 · Take the quiz &amp; aim for 100%"),
    "ch08_central_tendency.html":
        ("../../ch08.html#notebook", "Back to the book", "Chapter 8 · Measures of Central Tendency"),
    "ch08_challenges_solutions.html":
        ("../../ch08.html#quiz", "Back to the book", "Chapter 8 · Take the quiz &amp; aim for 100%"),
    "ch09_dispersion.html":
        ("../../ch09.html#notebook", "Back to the book", "Chapter 9 · Measures of Dispersion"),
    "ch09_challenges_solutions.html":
        ("../../ch09.html#quiz", "Back to the book", "Chapter 9 · Take the quiz &amp; aim for 100%"),
    "ch10_position.html":
        ("../../ch10.html#notebook", "Back to the book", "Chapter 10 · Measures of Position"),
    "ch10_challenges_solutions.html":
        ("../../ch10.html#quiz", "Back to the book", "Chapter 10 · Take the quiz &amp; aim for 100%"),
    "ch11_shape.html":
        ("../../ch11.html#notebook", "Back to the book", "Chapter 11 · Shape of a Distribution"),
    "ch11_challenges_solutions.html":
        ("../../ch11.html#quiz", "Back to the book", "Chapter 11 · Take the quiz &amp; aim for 100%"),
    "ch12_standardization.html":
        ("../../ch12.html#notebook", "Back to the book", "Chapter 12 · Standardization & z-scores"),
    "ch12_challenges_solutions.html":
        ("../../ch12.html#quiz", "Back to the book", "Chapter 12 · Take the quiz &amp; aim for 100%"),
    "ch13_frequency.html":
        ("../../ch13.html#notebook", "Back to the book", "Chapter 13 · Frequency Distributions"),
    "ch13_challenges_solutions.html":
        ("../../ch13.html#quiz", "Back to the book", "Chapter 13 · Take the quiz &amp; aim for 100%"),
    "ch14_categorical_charts.html":
        ("../../ch14.html#notebook", "Back to the book", "Chapter 14 · Charts for Categorical Data"),
    "ch14_challenges_solutions.html":
        ("../../ch14.html#quiz", "Back to the book", "Chapter 14 · Take the quiz &amp; aim for 100%"),
    "ch15_numerical_charts.html":
        ("../../ch15.html#notebook", "Back to the book", "Chapter 15 · Charts for Numerical Data"),
    "ch15_challenges_solutions.html":
        ("../../ch15.html#quiz", "Back to the book", "Chapter 15 · Take the quiz &amp; aim for 100%"),
    "ch16_multivariate.html":
        ("../../ch16.html#notebook", "Back to the book", "Chapter 16 · Multivariate &amp; Specialized Visuals"),
    "ch16_challenges_solutions.html":
        ("../../ch16.html#quiz", "Back to the book", "Chapter 16 · Take the quiz &amp; aim for 100%"),
    "ch17_choosing_viz.html":
        ("../../ch17.html#notebook", "Back to the book", "Chapter 17 · Choosing the Right Visualization"),
    "ch17_challenges_solutions.html":
        ("../../ch17.html#quiz", "Back to the book", "Chapter 17 · Take the quiz &amp; aim for 100%"),
    "ch18_data_cleaning_mindset.html":
        ("../../ch18.html#notebook", "Back to the book", "Chapter 18 · The Data-Cleaning Mindset"),
    "ch18_challenges_solutions.html":
        ("../../ch18.html#quiz", "Back to the book", "Chapter 18 · Take the quiz &amp; aim for 100%"),
    "ch19_duplicates_inconsistencies.html":
        ("../../ch19.html#notebook", "Back to the book", "Chapter 19 · Finding & Removing Duplicates and Inconsistencies"),
    "ch19_challenges_solutions.html":
        ("../../ch19.html#quiz", "Back to the book", "Chapter 19 · Take the quiz &amp; aim for 100%"),
    "ch20_missing_data.html":
        ("../../ch20.html#notebook", "Back to the book", "Chapter 20 · Handling Missing Data"),
    "ch20_challenges_solutions.html":
        ("../../ch20.html#quiz", "Back to the book", "Chapter 20 · Take the quiz &amp; aim for 100%"),
    "ch21_outliers.html":
        ("../../ch21.html#notebook", "Back to the book", "Chapter 21 · Detecting & Treating Outliers"),
    "ch21_challenges_solutions.html":
        ("../../ch21.html#quiz", "Back to the book", "Chapter 21 · Take the quiz &amp; aim for 100%"),
    "ch22_transformations.html":
        ("../../ch22.html#notebook", "Back to the book", "Chapter 22 · Transformations"),
    "ch22_challenges_solutions.html":
        ("../../ch22.html#quiz", "Back to the book", "Chapter 22 · Take the quiz &amp; aim for 100%"),
    "ch23_combining_reshaping.html":
        ("../../ch23.html#notebook", "Back to the book", "Chapter 23 · Combining & Reshaping Data"),
    "ch23_challenges_solutions.html":
        ("../../ch23.html#quiz", "Back to the book", "Chapter 23 · Take the quiz &amp; aim for 100%"),
    "ch24_feature_engineering.html":
        ("../../ch24.html#notebook", "Back to the book", "Chapter 24 · Feature Engineering"),
    "ch24_challenges_solutions.html":
        ("../../ch24.html#quiz", "Back to the book", "Chapter 24 · Take the quiz &amp; aim for 100%"),
    "ch25_eda.html":
        ("../../ch25.html#notebook", "Back to the book", "Chapter 25 · Exploratory Data Analysis"),
    "ch25_challenges_solutions.html":
        ("../../ch25.html#quiz", "Back to the book", "Chapter 25 · Take the quiz &amp; aim for 100%"),
    "ch26_meet_the_data.html":
        ("../../ch26.html#notebook", "Back to the book", "Chapter 26 · Review &amp; Case-Study Roadmap"),
    "ch26_challenges_solutions.html":
        ("../../ch26.html#quiz", "Back to the book", "Chapter 26 · Take the quiz &amp; aim for 100%"),
    "ch27_spotify_case.html":
        ("../../ch27.html#notebook", "Back to the book", "Chapter 27 · Case Study: Spotify Track Features"),
    "ch27_challenges_solutions.html":
        ("../../ch27.html#quiz", "Back to the book", "Chapter 27 · Take the quiz &amp; aim for 100%"),
    "ch28_ames_case.html":
        ("../../ch28.html#notebook", "Back to the book", "Chapter 28 · Case Study: Ames Housing Prices"),
    "ch28_challenges_solutions.html":
        ("../../ch28.html#quiz", "Back to the book", "Chapter 28 · Take the quiz &amp; aim for 100%"),
    "ch29_penguins_case.html":
        ("../../ch29.html#notebook", "Back to the book", "Chapter 29 · Case Study: Palmer Penguins"),
    "ch29_challenges_solutions.html":
        ("../../ch29.html#quiz", "Back to the book", "Chapter 29 · Take the quiz &amp; aim for 100%"),
    "ch30_probability.html":
        ("../../ch30.html#notebook", "Back to the book", "Chapter 30 · Probability Fundamentals"),
    "ch30_challenges_solutions.html":
        ("../../ch30.html#quiz", "Back to the book", "Chapter 30 · Take the quiz &amp; aim for 100%"),
    "ch31_rules.html":
        ("../../ch31.html#notebook", "Back to the book", "Chapter 31 · Rules of Probability"),
    "ch31_challenges_solutions.html":
        ("../../ch31.html#quiz", "Back to the book", "Chapter 31 · Take the quiz &amp; aim for 100%"),
    "ch32_counting.html":
        ("../../ch32.html#notebook", "Back to the book", "Chapter 32 · Counting &amp; Combinatorics"),
    "ch32_challenges_solutions.html":
        ("../../ch32.html#quiz", "Back to the book", "Chapter 32 · Take the quiz &amp; aim for 100%"),
    "ch33_conditional.html":
        ("../../ch33.html#notebook", "Back to the book", "Chapter 33 · Conditional Probability &amp; Independence"),
    "ch33_challenges_solutions.html":
        ("../../ch33.html#quiz", "Back to the book", "Chapter 33 · Take the quiz &amp; aim for 100%"),
    "ch34_bayes.html":
        ("../../ch34.html#notebook", "Back to the book", "Chapter 34 · Bayes' Theorem &amp; the Law of Total Probability"),
    "ch34_challenges_solutions.html":
        ("../../ch34.html#quiz", "Back to the book", "Chapter 34 · Take the quiz &amp; aim for 100%"),
    "ch35_random_variables.html":
        ("../../ch35.html#notebook", "Back to the book", "Chapter 35 · Random Variables &amp; Expectation"),
    "ch35_challenges_solutions.html":
        ("../../ch35.html#quiz", "Back to the book", "Chapter 35 · Take the quiz &amp; aim for 100%"),
    "ch36_simulation.html":
        ("../../ch36.html#notebook", "Back to the book", "Chapter 36 · Probability by Simulation (Monte Carlo)"),
    "ch36_challenges_solutions.html":
        ("../../ch36.html#quiz", "Back to the book", "Chapter 36 · Take the quiz &amp; aim for 100%"),
    "ch37_discrete_distributions.html":
        ("../../ch37.html#notebook", "Back to the book", "Chapter 37 · Discrete Distributions"),
    "ch37_challenges_solutions.html":
        ("../../ch37.html#quiz", "Back to the book", "Chapter 37 · Take the quiz &amp; aim for 100%"),
    "ch38_continuous_distributions.html":
        ("../../ch38.html#notebook", "Back to the book", "Chapter 38 · Continuous Distributions"),
    "ch38_challenges_solutions.html":
        ("../../ch38.html#quiz", "Back to the book", "Chapter 38 · Take the quiz &amp; aim for 100%"),
    "ch39_normal_in_depth.html":
        ("../../ch39.html#notebook", "Back to the book", "Chapter 39 · The Normal Distribution in Depth"),
    "ch39_challenges_solutions.html":
        ("../../ch39.html#quiz", "Back to the book", "Chapter 39 · Take the quiz &amp; aim for 100%"),
    "ch40_sampling_clt.html":
        ("../../ch40.html#notebook", "Back to the book", "Chapter 40 · Sampling Distributions &amp; the CLT"),
    "ch40_challenges_solutions.html":
        ("../../ch40.html#quiz", "Back to the book", "Chapter 40 · Take the quiz &amp; aim for 100%"),
    "ch41_inference_distributions.html":
        ("../../ch41.html#notebook", "Back to the book", "Chapter 41 · Distributions for Inference"),
    "ch41_challenges_solutions.html":
        ("../../ch41.html#quiz", "Back to the book", "Chapter 41 · Take the quiz &amp; aim for 100%"),
    "ch42_joint_densities.html":
        ("../../ch42.html#notebook", "Back to the book", "Chapter 42 · Joint, Marginal &amp; Conditional Densities"),
    "ch42_challenges_solutions.html":
        ("../../ch42.html#quiz", "Back to the book", "Chapter 42 · Take the quiz &amp; aim for 100%"),
    "ch43_transformations.html":
        ("../../ch43.html#notebook", "Back to the book", "Chapter 43 · Transformations of Random Variables"),
    "ch43_challenges_solutions.html":
        ("../../ch43.html#quiz", "Back to the book", "Chapter 43 · Take the quiz &amp; aim for 100%"),
    "ch44_conditional_expectation.html":
        ("../../ch44.html#notebook", "Back to the book", "Chapter 44 · Conditional Expectation &amp; the Tower Property"),
    "ch44_challenges_solutions.html":
        ("../../ch44.html#quiz", "Back to the book", "Chapter 44 · Take the quiz &amp; aim for 100%"),
    "ch45_moments_mgfs.html":
        ("../../ch45.html#notebook", "Back to the book", "Chapter 45 · Moments, MGFs &amp; Inequalities"),
    "ch45_challenges_solutions.html":
        ("../../ch45.html#quiz", "Back to the book", "Chapter 45 · Take the quiz &amp; aim for 100%"),
    "ch46_estimation_theory.html":
        ("../../ch46.html#notebook", "Back to the book", "Chapter 46 · Estimation Theory"),
    "ch46_challenges_solutions.html":
        ("../../ch46.html#quiz", "Back to the book", "Chapter 46 · Take the quiz &amp; aim for 100%"),
    "ch47_distribution_framework.html":
        ("../../ch47.html#notebook", "Back to the book", "Chapter 47 · The Probability Distribution Framework"),
    "ch48_ecommerce_bernoulli.html":
        ("../../ch48.html#notebook", "Back to the book", "Chapter 48 · E-commerce Conversions (Bernoulli)"),
    "ch49_manufacturing_binomial.html":
        ("../../ch49.html#notebook", "Back to the book", "Chapter 49 · Manufacturing Defects (Binomial)"),
    "ch50_server_poisson.html":
        ("../../ch50.html#notebook", "Back to the book", "Chapter 50 · Server Traffic Spikes (Poisson)"),
    "ch51_telemarketing_geometric.html":
        ("../../ch51.html#notebook", "Back to the book", "Chapter 51 · Sales Calls to First Win (Geometric)"),
    "ch52_wildlife_hypergeometric.html":
        ("../../ch52.html#notebook", "Back to the book", "Chapter 52 · Capture-Recapture (Hypergeometric)"),
    "ch53_software_negbinomial.html":
        ("../../ch53.html#notebook", "Back to the book", "Chapter 53 · Software Reliability (Negative Binomial)"),
    "ch54_exam_normal.html":
        ("../../ch54.html#notebook", "Back to the book", "Chapter 54 · Exam Scores (Normal)"),
    "ch55_hardware_exponential.html":
        ("../../ch55.html#notebook", "Back to the book", "Chapter 55 · Hardware Lifespans (Exponential)"),
    "ch56_rainfall_gamma.html":
        ("../../ch56.html#notebook", "Back to the book", "Chapter 56 · Regional Rainfall (Gamma)"),
    "ch57_freight_clt.html":
        ("../../ch57.html#notebook", "Back to the book", "Chapter 57 · Freight Weights & the CLT"),
    "ch58_clinical_t.html":
        ("../../ch58.html#notebook", "Back to the book", "Chapter 58 · Clinical Trial Efficacy (Student's t)"),
    "ch59_survey_chisquare.html":
        ("../../ch59.html#notebook", "Back to the book", "Chapter 59 · Survey Demographics (Chi-Square)"),
    "ch60_crop_anova.html":
        ("../../ch60.html#notebook", "Back to the book", "Chapter 60 · Crop Yield by Fertilizer (F / ANOVA)"),
    "ch61_why_sample.html":
        ("../../ch61.html#notebook", "Back to the book", "Chapter 61 · Why We Sample"),
    "ch61_challenges_solutions.html":
        ("../../ch61.html#challenges", "Back to the book", "Chapter 61 · Why We Sample"),
    "ch62_probability_sampling.html":
        ("../../ch62.html#notebook", "Back to the book", "Chapter 62 · Probability Sampling Methods"),
    "ch62_challenges_solutions.html":
        ("../../ch62.html#challenges", "Back to the book", "Chapter 62 · Probability Sampling Methods"),
    "ch63_nonprobability_sampling.html":
        ("../../ch63.html#notebook", "Back to the book", "Chapter 63 · Non-Probability Sampling Methods"),
    "ch63_challenges_solutions.html":
        ("../../ch63.html#challenges", "Back to the book", "Chapter 63 · Non-Probability Sampling Methods"),
    "ch64_sample_size.html":
        ("../../ch64.html#notebook", "Back to the book", "Chapter 64 · Determining Sample Size"),
    "ch64_challenges_solutions.html":
        ("../../ch64.html#challenges", "Back to the book", "Chapter 64 · Determining Sample Size"),
    "ch65_study_design.html":
        ("../../ch65.html#notebook", "Back to the book", "Chapter 65 · Study Design & Data Quality"),
    "ch65_challenges_solutions.html":
        ("../../ch65.html#challenges", "Back to the book", "Chapter 65 · Study Design & Data Quality"),
    "ch66_bias_collection.html":
        ("../../ch66.html#notebook", "Back to the book", "Chapter 66 · Bias in Data Collection"),
    "ch66_challenges_solutions.html":
        ("../../ch66.html#challenges", "Back to the book", "Chapter 66 · Bias in Data Collection"),
    "ch69_point_interval.html":
        ("../../ch69.html#notebook", "Back to the book", "Chapter 69 · Point vs. Interval Estimation"),
    "ch69_challenges_solutions.html":
        ("../../ch69.html#challenges", "Back to the book", "Chapter 69 · Point vs. Interval Estimation"),
    "ch70_ci_mean.html":
        ("../../ch70.html#notebook", "Back to the book", "Chapter 70 · Confidence Intervals for a Mean"),
    "ch70_challenges_solutions.html":
        ("../../ch70.html#challenges", "Back to the book", "Chapter 70 · Confidence Intervals for a Mean"),
    "ch71_ci_proportions.html":
        ("../../ch71.html#notebook", "Back to the book", "Chapter 71 · Confidence Intervals for Proportions & Differences"),
    "ch71_challenges_solutions.html":
        ("../../ch71.html#challenges", "Back to the book", "Chapter 71 · Confidence Intervals for Proportions & Differences"),
    "ch72_margin_of_error.html":
        ("../../ch72.html#notebook", "Back to the book", "Chapter 72 · Margin of Error"),
    "ch72_challenges_solutions.html":
        ("../../ch72.html#challenges", "Back to the book", "Chapter 72 · Margin of Error"),
    "ch73_resampling.html":
        ("../../ch73.html#notebook", "Back to the book", "Chapter 73 · Resampling & Simulation"),
    "ch73_challenges_solutions.html":
        ("../../ch73.html#challenges", "Back to the book", "Chapter 73 · Resampling & Simulation"),
    "ch74_logic_testing.html":
        ("../../ch74.html#notebook", "Back to the book", "Chapter 74 · The Logic of Hypothesis Testing"),
    "ch74_challenges_solutions.html":
        ("../../ch74.html#challenges", "Back to the book", "Chapter 74 · The Logic of Hypothesis Testing"),
    "ch75_significance_errors.html":
        ("../../ch75.html#notebook", "Back to the book", "Chapter 75 · Significance, p-values &amp; Errors"),
    "ch75_challenges_solutions.html":
        ("../../ch75.html#challenges", "Back to the book", "Chapter 75 · Significance, p-values &amp; Errors"),
    "ch76_z_tests.html":
        ("../../ch76.html#notebook", "Back to the book", "Chapter 76 · z-Tests"),
    "ch76_challenges_solutions.html":
        ("../../ch76.html#challenges", "Back to the book", "Chapter 76 · z-Tests"),
    "ch77_t_tests.html":
        ("../../ch77.html#notebook", "Back to the book", "Chapter 77 · t-Tests"),
    "ch77_challenges_solutions.html":
        ("../../ch77.html#challenges", "Back to the book", "Chapter 77 · t-Tests"),
    "ch78_anova.html":
        ("../../ch78.html#notebook", "Back to the book", "Chapter 78 · ANOVA"),
    "ch78_challenges_solutions.html":
        ("../../ch78.html#challenges", "Back to the book", "Chapter 78 · ANOVA"),
    "ch79_chi_square.html":
        ("../../ch79.html#notebook", "Back to the book", "Chapter 79 · Chi-Square Tests"),
    "ch79_challenges_solutions.html":
        ("../../ch79.html#challenges", "Back to the book", "Chapter 79 · Chi-Square Tests"),
    "ch80_nonparametric.html":
        ("../../ch80.html#notebook", "Back to the book", "Chapter 80 · Nonparametric Tests"),
    "ch80_challenges_solutions.html":
        ("../../ch80.html#challenges", "Back to the book", "Chapter 80 · Nonparametric Tests"),
    "ch81_choosing_test.html":
        ("../../ch81.html#notebook", "Back to the book", "Chapter 81 · Choosing the Right Test"),
    "ch81_challenges_solutions.html":
        ("../../ch81.html#challenges", "Back to the book", "Chapter 81 · Choosing the Right Test"),
    "ch82_ab_testing.html":
        ("../../ch82.html#notebook", "Back to the book", "Chapter 82 · A/B Testing &amp; Online Experiments"),
    "ch82_challenges_solutions.html":
        ("../../ch82.html#challenges", "Back to the book", "Chapter 82 · A/B Testing &amp; Online Experiments"),
    "ch83_review_choosing.html":
        ("../../ch83.html#notebook", "Back to the book", "Chapter 83 · Review &amp; Choosing the Right Test"),
    "ch84_web_abtest.html":
        ("../../ch84.html#notebook", "Back to the book", "Chapter 84 · Case Study: A Web A/B Test"),
    "ch85_marketing_channels.html":
        ("../../ch85.html#notebook", "Back to the book", "Chapter 85 · Case Study: Comparing Marketing Channels"),
    "ch86_clinical_trial.html":
        ("../../ch86.html#notebook", "Back to the book", "Chapter 86 · Case Study: A Clinical Trial"),
    "ch87_satisfaction_survey.html":
        ("../../ch87.html#notebook", "Back to the book", "Chapter 87 · Case Study: A Customer Satisfaction Survey"),
    "ch88_manufacturing_quality.html":
        ("../../ch88.html#notebook", "Back to the book", "Chapter 88 · Case Study: Manufacturing Quality"),
    "ch89_covariance.html":
        ("../../ch89.html#notebook", "Back to the book", "Chapter 89 · Covariance"),
    "ch89_challenges_solutions.html":
        ("../../ch89.html#challenges", "Back to the book", "Chapter 89 · Covariance"),
    "ch90_correlation.html":
        ("../../ch90.html#notebook", "Back to the book", "Chapter 90 · Correlation Coefficients"),
    "ch90_challenges_solutions.html":
        ("../../ch90.html#challenges", "Back to the book", "Chapter 90 · Correlation Coefficients"),
    "ch91_causation.html":
        ("../../ch91.html#notebook", "Back to the book", "Chapter 91 · Correlation vs. Causation"),
    "ch91_challenges_solutions.html":
        ("../../ch91.html#challenges", "Back to the book", "Chapter 91 · Correlation vs. Causation"),
    "ch92_simple_regression.html":
        ("../../ch92.html#notebook", "Back to the book", "Chapter 92 · Simple Linear Regression"),
    "ch92_challenges_solutions.html":
        ("../../ch92.html#challenges", "Back to the book", "Chapter 92 · Simple Linear Regression"),
    "ch93_ols_framework.html":
        ("../../ch93.html#notebook", "Back to the book", "Chapter 93 · The OLS Framework"),
    "ch93_challenges_solutions.html":
        ("../../ch93.html#challenges", "Back to the book", "Chapter 93 · The OLS Framework"),
    "ch94_multiple_regression.html":
        ("../../ch94.html#notebook", "Back to the book", "Chapter 94 · Multiple Linear Regression"),
    "ch94_challenges_solutions.html":
        ("../../ch94.html#challenges", "Back to the book", "Chapter 94 · Multiple Linear Regression"),
    "ch95_diagnostics.html":
        ("../../ch95.html#notebook", "Back to the book", "Chapter 95 · Regression Assumptions & Diagnostics"),
    "ch95_challenges_solutions.html":
        ("../../ch95.html#challenges", "Back to the book", "Chapter 95 · Regression Assumptions & Diagnostics"),
    "ch96_logistic_regression.html":
        ("../../ch96.html#notebook", "Back to the book", "Chapter 96 · Logistic Regression"),
    "ch96_challenges_solutions.html":
        ("../../ch96.html#challenges", "Back to the book", "Chapter 96 · Logistic Regression"),
    "ch97_regularization.html":
        ("../../ch97.html#notebook", "Back to the book", "Chapter 97 · Regularization & Flexible Models"),
    "ch97_challenges_solutions.html":
        ("../../ch97.html#challenges", "Back to the book", "Chapter 97 · Regularization & Flexible Models"),
    "ch98_glm.html":
        ("../../ch98.html#notebook", "Back to the book", "Chapter 98 · Generalized Linear Models"),
    "ch98_challenges_solutions.html":
        ("../../ch98.html#challenges", "Back to the book", "Chapter 98 · Generalized Linear Models"),
    "ch99_econometrics.html":
        ("../../ch99.html#notebook", "Back to the book", "Chapter 99 · Econometrics & Panel Data"),
    "ch99_challenges_solutions.html":
        ("../../ch99.html#challenges", "Back to the book", "Chapter 99 · Econometrics & Panel Data"),
    "ch100_ames_case_study.html":
        ("../../ch100.html#notebook", "Back to the book", "Chapter 100 · Case Study: Predicting Ames House Prices"),
    "ch100_take_it_further.html":
        ("../../ch100.html#challenges", "Back to the book", "Chapter 100 · Take It Further"),
    "ch101_churn_case_study.html":
        ("../../ch101.html#notebook", "Back to the book", "Chapter 101 · Case Study: Logistic Regression in Action"),
    "ch101_take_it_further.html":
        ("../../ch101.html#challenges", "Back to the book", "Chapter 101 · Take It Further"),
    "ch102_bikeshare_case_study.html":
        ("../../ch102.html#notebook", "Back to the book", "Chapter 102 · Case Study: Forecasting Daily Bike-Share Demand"),
    "ch102_take_it_further.html":
        ("../../ch102.html#challenges", "Back to the book", "Chapter 102 · Take It Further"),
    "ch103_medical_charges_case_study.html":
        ("../../ch103.html#notebook", "Back to the book", "Chapter 103 · Case Study: Predicting Medical Charges"),
    "ch103_take_it_further.html":
        ("../../ch103.html#challenges", "Back to the book", "Chapter 103 · Take It Further"),
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
