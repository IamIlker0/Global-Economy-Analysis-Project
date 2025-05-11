# Global Economy Project

## Project Overview
This project analyzes the National Accounts Main Aggregates Database from the United Nations, containing economic indicators for 200+ countries from 1970 onwards. The dataset has 10,513 rows and 26 features covering GDP, manufacturing, agriculture, trade, and government expenditure.

## Data Source
[United Nations Statistics Division's National Accounts Main Aggregates Database](https://www.kaggle.com/datasets/prasad22/global-economy-indicators)

## Project Workflow

### 1. Excel Phase
- Initial data cleaning and formatting
- Basic exploratory analysis
- Pivot table creation for preliminary insights
- Data validation and structure refinement

### 2. SQL Phase
- Comprehensive missing value identification
- Correlation analysis between economic indicators
- Data filtering and transformation
- Query-based analysis for specific economic patterns

### 3. Python Phase
- Advanced analytics and statistical analysis
- Feature engineering and selection
- Machine learning model development
- Missing value treatment strategies:
  - Country-specific mean imputation for low missing rates
  - Time-series interpolation for inventory changes
  - GDP-based estimation for remaining gaps

### 4. Tableau Phase
- Interactive visualization development
- Multi-dimensional economic indicator dashboards
- Time-series analysis of economic trends
- Comparative country performance visualization

### 5. Streamlit Phase
- Development of interactive web application
- Integration of machine learning predictions
- User-friendly interface for data exploration
- Dynamic filtering and visualization options

**Live Demo:** [Global Economy Analysis Dashboard](https://global-economy-analysis-project-jmrhdd8ancqlvqnjjkwv2z.streamlit.app)
The dashboard provides interactive visualizations of global economic data, allowing users to explore trade flows, GDP relationships, and sectoral analyses across different countries and time periods. The deployed application is hosted on Streamlit Cloud and integrates data visualization with our machine learning predictions.

## Key Findings

### Correlation Analysis with GDP
- Perfect correlations (r = 1.0) with GNI and Total Value Added
- Very strong positive correlations (r > 0.95) with service sectors
- Strong positive correlations with capital formation metrics (r = 0.87-0.95)

### Machine Learning Models
- Evaluated multiple regression techniques including:
  - Polynomial Regression
  - Decision Tree Regression
  - Random Forest Regression
  - Gradient Boosting Regression
  - Support Vector Regression

- Optimized Random Forest model achieved exceptional performance (R² = 0.9887)
- Implemented comprehensive regularization to prevent overfitting
- Identified government expenditure as the strongest GDP predictor

## Repository Structure
```
global-economy-project/
├── data/
│   ├── raw/                # Original dataset
│   └── processed/          # Cleaned and transformed data
├── notebooks/
│   ├── 01_excel_analysis/  # Excel documentation and exports
│   ├── 02_sql_queries/     # SQL scripts and queries
│   ├── 03_python_analysis/ # Jupyter notebooks for analysis
│   └── 04_ml_models/       # Machine learning model development
├── models/
│   └── random_forest_gdp_predictor.joblib  # Saved model
├── tableau/
│   └── global_economy_dashboard.twbx       # Tableau workbook
├── streamlit/
│   ├── app.py              # Streamlit application code
│   └── requirements.txt    # Dependencies for the app
├── README.md               # This file
└── requirements.txt        # Project dependencies
```

## Conclusions and Insights
- Service sectors demonstrate the strongest correlation with GDP growth
- Government expenditure has significant predictive power for economic output
- Regularized machine learning models can accurately predict GDP based on sectoral indicators
- The relationship between inventory changes and GDP follows complex patterns that require specialized imputation techniques
- Transportation, communication, and wholesale/retail sectors show strong influence on economic output

## Future Work
- Incorporate additional datasets for enhanced predictive power
- Develop country-specific models to account for economic structural differences
- Implement time-series forecasting for future GDP projections
- Expand analysis to include more granular sector-specific indicators

## Technologies Used
- Excel for initial data processing
- SQL for data querying and transformation
- Python (Pandas, Scikit-learn, NumPy, Matplotlib, Seaborn) for analysis and modeling
- Tableau for interactive visualizations
- Streamlit for web application development
