# Portfolio-Optimization
Generate an optimized portfolio from the current S&P 500 companies. To optimize a portfolio we want to maximize returns while minimizing the risk with respect to the amount of money we allocate on each asset in our portfolio. We want to think about index, sector, industry, and industry anti-correlation and covariance. Our portfolio will be measured in respect to the efficient frontier.

## 
Project Setup
------------

### Project Virtual Environment  (conda)

#### conda

   

To start up:

    conda env create --file environment.yml    
    conda activate port-opt-py37
    
To tear down:

    conda deactivate


## The Data Science Method


1.   [Problem Identification](https://medium.com/@aiden.dataminer/the-data-science-method-problem-identification-6ffcda1e5152)

2.   [**Data Wrangling**](https://medium.com/@aiden.dataminer/the-data-science-method-dsm-data-collection-organization-and-definitions-d19b6ff141c4) 
  * Data Collection - Collected data from wikipedia and yahoo finance price dataset. The wikipedia showed us the currect S&P 500 companies and then used their ticker symbols to query yahoo finance adj. close prices.
      - Load the S&P 500 tickers from wikipedia page
      - Get S&P 500 Index (^GSPC) as a Bench Mark
      - Use S&P Symbols to Get Adj Close from Yahoo Finance
  * Data Organization - Done using cookiecutter template
  * Data Definition 
  * Data Cleaning - The S&P 500 data from yahoo finance price is clean and ready for analysis use. So we will use this dataset to setup the protfolio optimizer with proof of concept then use a different data source later if issues arise with historic data.
 
3.   [Exploratory Data Analysis](https://medium.com/@aiden.dataminer/the-data-science-method-dsm-exploratory-data-analysis-bc84d4d8d3f9)
 * Build data profile tables and plots
        - Outliers & Anomalies
 * Explore data relationships
 * Identification and creation of features

4.   [Pre-processing and Training Data Development](https://medium.com/@aiden.dataminer/the-data-science-method-dsm-pre-processing-and-training-data-development-fd2d75182967)
  * Create dummy or indicator features for categorical variables
  * Standardize the magnitude of numeric features
  * Split into testing and training datasets
  * Apply scaler to the testing set
5.   [Modeling](https://medium.com/@aiden.dataminer/the-data-science-method-dsm-modeling-56b4233cad1b)
  * Create dummy or indicator features for categorical variable
  * Fit Models with Training Data Set
  * Review Model Outcomes — Iterate over additional models as needed.
  * Identify the Final Model

6.   [Documentation](https://medium.com/@aiden.dataminer/the-data-science-method-dsm-documentation-c92c28bd45e6)

  * Review the Results
  * Present and share your findings - storytelling
  * Finalize Code 
  * Finalize Documentation



## 
Project Organization
------------

    ├── LICENSE
    TODO:├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    TODO: ├── setup.py           <- makes project conda installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
    

