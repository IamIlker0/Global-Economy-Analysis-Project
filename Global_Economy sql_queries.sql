
/*
EXCHANGE RATE CHANGE ANALYSIS:

This query calculates year-over-year percentage changes in IMF-based exchange rates for each country.

Notable observations:
- Exchange rate fluctuations reflect currency valuation changes against the USD
- Large positive values indicate significant currency depreciation
- Large negative values indicate significant currency appreciation
- Volatility may be caused by:
  * Economic policy changes (monetary policy shifts)
  * Political instability or regime changes
  * Economic crises (inflation, recession)
  * External shocks (commodity price changes, global financial events)
  * Currency reforms or redenomination

The calculated percentage changes provide a normalized metric for comparing currency stability across countries with different monetary scales.

Note: Some extreme values may represent currency reforms rather than market-driven changes.
*/

WITH ExchangeRateChanges AS (
  SELECT 
    Country,
    Year,
    [IMF based exchange rate],
    LAG([IMF based exchange rate]) OVER (PARTITION BY Country ORDER BY Year) AS PreviousRate
  FROM Global_Economy_Indicators
)
SELECT 
  Country,
  Year,
  [IMF based exchange rate],
  PreviousRate,
  CAST(
    CASE 
      WHEN PreviousRate IS NULL OR PreviousRate = 0 THEN NULL
      ELSE ([IMF based exchange rate] - PreviousRate) / PreviousRate * 100 
    END AS DECIMAL(18,4)
  ) AS ExchangeRateChangePercent
FROM ExchangeRateChanges
ORDER BY Country, Year;

--------------------------------------
/*
CORRELATION ANALYSIS WITH GDP:

This query calculates the Pearson correlation coefficient between GDP and various economic indicators:
- Correlation ranges from -1 to 1, with values close to 1 indicating strong positive correlation
- Results are sorted by correlation strength to identify the most influential factors
- These correlations help identify key predictors for GDP modeling in Python
- The analysis considers only complete pairs of observations (where both GDP and the factor are not NULL)

This statistical analysis informs feature selection for our machine learning models.
*/
SELECT 
  'Manufacturing' AS Economic_Factor,
  COUNT(*) AS DataPoints,
  CAST(
    (COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Manufacturing (ISIC D)]) - SUM([Gross Domestic Product (GDP)]) * SUM([Manufacturing (ISIC D)])) / 
    (SQRT(COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Gross Domestic Product (GDP)]) - SUM([Gross Domestic Product (GDP)]) * SUM([Gross Domestic Product (GDP)])) * 
     SQRT(COUNT(*) * SUM([Manufacturing (ISIC D)] * [Manufacturing (ISIC D)]) - SUM([Manufacturing (ISIC D)]) * SUM([Manufacturing (ISIC D)])))
  AS DECIMAL(18,4)) AS Correlation_With_GDP
FROM Global_Economy_Indicators
WHERE [Gross Domestic Product (GDP)] IS NOT NULL AND [Manufacturing (ISIC D)] IS NOT NULL

UNION ALL

SELECT 
  'Agriculture' AS Economic_Factor,
  COUNT(*) AS DataPoints,
  CAST(
    (COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Agriculture, hunting, forestry, fishing (ISIC A-B)]) - SUM([Gross Domestic Product (GDP)]) * SUM([Agriculture, hunting, forestry, fishing (ISIC A-B)])) / 
    (SQRT(COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Gross Domestic Product (GDP)]) - SUM([Gross Domestic Product (GDP)]) * SUM([Gross Domestic Product (GDP)])) * 
     SQRT(COUNT(*) * SUM([Agriculture, hunting, forestry, fishing (ISIC A-B)] * [Agriculture, hunting, forestry, fishing (ISIC A-B)]) - SUM([Agriculture, hunting, forestry, fishing (ISIC A-B)]) * SUM([Agriculture, hunting, forestry, fishing (ISIC A-B)])))
  AS DECIMAL(18,4)) AS Correlation_With_GDP
FROM Global_Economy_Indicators
WHERE [Gross Domestic Product (GDP)] IS NOT NULL AND [Agriculture, hunting, forestry, fishing (ISIC A-B)] IS NOT NULL

UNION ALL

SELECT 
  'Exports' AS Economic_Factor,
  COUNT(*) AS DataPoints,
  CAST(
    (COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Exports of goods and services]) - SUM([Gross Domestic Product (GDP)]) * SUM([Exports of goods and services])) / 
    (SQRT(COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Gross Domestic Product (GDP)]) - SUM([Gross Domestic Product (GDP)]) * SUM([Gross Domestic Product (GDP)])) * 
     SQRT(COUNT(*) * SUM([Exports of goods and services] * [Exports of goods and services]) - SUM([Exports of goods and services]) * SUM([Exports of goods and services])))
  AS DECIMAL(18,4)) AS Correlation_With_GDP
FROM Global_Economy_Indicators
WHERE [Gross Domestic Product (GDP)] IS NOT NULL AND [Exports of goods and services] IS NOT NULL

UNION ALL

SELECT 
  'Government Expenditure' AS Economic_Factor,
  COUNT(*) AS DataPoints,
  CAST(
    (COUNT(*) * SUM([Gross Domestic Product (GDP)] * [General government final consumption expenditure]) - SUM([Gross Domestic Product (GDP)]) * SUM([General government final consumption expenditure])) / 
    (SQRT(COUNT(*) * SUM([Gross Domestic Product (GDP)] * [Gross Domestic Product (GDP)]) - SUM([Gross Domestic Product (GDP)]) * SUM([Gross Domestic Product (GDP)])) * 
     SQRT(COUNT(*) * SUM([General government final consumption expenditure] * [General government final consumption expenditure]) - SUM([General government final consumption expenditure]) * SUM([General government final consumption expenditure])))
  AS DECIMAL(18,4)) AS Correlation_With_GDP
FROM Global_Economy_Indicators
WHERE [Gross Domestic Product (GDP)] IS NOT NULL AND [General government final consumption expenditure] IS NOT NULL

-- Add other economic factors as needed

ORDER BY Correlation_With_GDP DESC;

--------------------------------------

-- Calculate sum of missing values in each column
SELECT 
  COUNT(*) AS TotalRows,
  SUM(CASE WHEN [AMA exchange rate] IS NULL THEN 1 ELSE 0 END) AS Missing_AMA_Exchange_Rate,
  SUM(CASE WHEN [IMF based exchange rate] IS NULL THEN 1 ELSE 0 END) AS Missing_IMF_Exchange_Rate,
  SUM(CASE WHEN [Population] IS NULL THEN 1 ELSE 0 END) AS Missing_Population,
  SUM(CASE WHEN [Currency] IS NULL THEN 1 ELSE 0 END) AS Missing_Currency,
  SUM(CASE WHEN [Per capita GNI] IS NULL THEN 1 ELSE 0 END) AS Missing_Per_Capita_GNI,
  SUM(CASE WHEN [Agriculture, hunting, forestry, fishing (ISIC A-B)] IS NULL THEN 1 ELSE 0 END) AS Missing_Agriculture,
  SUM(CASE WHEN [Changes in inventories] IS NULL THEN 1 ELSE 0 END) AS Missing_Inventories,
  SUM(CASE WHEN [Construction (ISIC F)] IS NULL THEN 1 ELSE 0 END) AS Missing_Construction,
  SUM(CASE WHEN [Exports of goods and services] IS NULL THEN 1 ELSE 0 END) AS Missing_Exports,
  SUM(CASE WHEN [Final consumption expenditure] IS NULL THEN 1 ELSE 0 END) AS Missing_Final_Consumption,
  SUM(CASE WHEN [General government final consumption expenditure] IS NULL THEN 1 ELSE 0 END) AS Missing_Gov_Consumption,
  SUM(CASE WHEN [Gross capital formation] IS NULL THEN 1 ELSE 0 END) AS Missing_Capital_Formation,
  SUM(CASE WHEN [Gross fixed capital formation (including Acquisitions less dispo] IS NULL THEN 1 ELSE 0 END) AS Missing_Fixed_Capital_Formation,
  SUM(CASE WHEN [Household consumption expenditure (including Non-profit institut] IS NULL THEN 1 ELSE 0 END) AS Missing_Household_Consumption,
  SUM(CASE WHEN [Imports of goods and services] IS NULL THEN 1 ELSE 0 END) AS Missing_Imports,
  SUM(CASE WHEN [Manufacturing (ISIC D)] IS NULL THEN 1 ELSE 0 END) AS Missing_Manufacturing,
  SUM(CASE WHEN [Mining, Manufacturing, Utilities (ISIC C-E)] IS NULL THEN 1 ELSE 0 END) AS Missing_Mining_Manufacturing,
  SUM(CASE WHEN [Other Activities (ISIC J-P)] IS NULL THEN 1 ELSE 0 END) AS Missing_Other_Activities,
  SUM(CASE WHEN [Total Value Added] IS NULL THEN 1 ELSE 0 END) AS Missing_Value_Added,
  SUM(CASE WHEN [Transport, storage and communication (ISIC I)] IS NULL THEN 1 ELSE 0 END) AS Missing_Transport,
  SUM(CASE WHEN [Wholesale, retail trade, restaurants and hotels (ISIC G-H)] IS NULL THEN 1 ELSE 0 END) AS Missing_Wholesale_Retail,
  SUM(CASE WHEN [Gross National Income(GNI) in USD] IS NULL THEN 1 ELSE 0 END) AS Missing_GNI,
  SUM(CASE WHEN [Gross Domestic Product (GDP)] IS NULL THEN 1 ELSE 0 END) AS Missing_GDP
FROM Global_Economy_Indicators;

-- Calculate percentage of missing values in each column
SELECT 
  COUNT(*) AS TotalRows,
  CAST(SUM(CASE WHEN [AMA exchange rate] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS AMA_Exchange_Rate_Missing_Pct,
  CAST(SUM(CASE WHEN [IMF based exchange rate] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS IMF_Exchange_Rate_Missing_Pct,
  CAST(SUM(CASE WHEN [Population] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Population_Missing_Pct,
  CAST(SUM(CASE WHEN [Currency] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Currency_Missing_Pct,
  CAST(SUM(CASE WHEN [Per capita GNI] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Per_Capita_GNI_Missing_Pct,
  CAST(SUM(CASE WHEN [Agriculture, hunting, forestry, fishing (ISIC A-B)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Agriculture_Missing_Pct,
  CAST(SUM(CASE WHEN [Changes in inventories] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Inventories_Missing_Pct,
  CAST(SUM(CASE WHEN [Construction (ISIC F)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Construction_Missing_Pct,
  CAST(SUM(CASE WHEN [Exports of goods and services] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Exports_Missing_Pct,
  CAST(SUM(CASE WHEN [Final consumption expenditure] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Final_Consumption_Missing_Pct,
  CAST(SUM(CASE WHEN [General government final consumption expenditure] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Gov_Consumption_Missing_Pct,
  CAST(SUM(CASE WHEN [Gross capital formation] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Capital_Formation_Missing_Pct,
  CAST(SUM(CASE WHEN [Gross fixed capital formation (including Acquisitions less dispo] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Fixed_Capital_Formation_Missing_Pct,
  CAST(SUM(CASE WHEN [Household consumption expenditure (including Non-profit institut] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Household_Consumption_Missing_Pct,
  CAST(SUM(CASE WHEN [Imports of goods and services] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Imports_Missing_Pct,
  CAST(SUM(CASE WHEN [Manufacturing (ISIC D)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Manufacturing_Missing_Pct,
  CAST(SUM(CASE WHEN [Mining, Manufacturing, Utilities (ISIC C-E)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Mining_Manufacturing_Missing_Pct,
  CAST(SUM(CASE WHEN [Other Activities (ISIC J-P)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Other_Activities_Missing_Pct,
  CAST(SUM(CASE WHEN [Total Value Added] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Value_Added_Missing_Pct,
  CAST(SUM(CASE WHEN [Transport, storage and communication (ISIC I)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Transport_Missing_Pct,
  CAST(SUM(CASE WHEN [Wholesale, retail trade, restaurants and hotels (ISIC G-H)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS Wholesale_Retail_Missing_Pct,
  CAST(SUM(CASE WHEN [Gross National Income(GNI) in USD] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS GNI_Missing_Pct,
  CAST(SUM(CASE WHEN [Gross Domestic Product (GDP)] IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 AS GDP_Missing_Pct
FROM Global_Economy_Indicators;

/*
NOTE ON MISSING DATA HANDLING:

Missing data analysis revealed low percentages of missing values in most columns:
- Most economic indicators: < 1% missing
- Inventories: 17.5% missing

Decided to handle missing values in Python rather than SQL due to:
1. Access to more sophisticated imputation techniques in Python
2. Ability to leverage time series structure for better imputation
3. Flexibility to try multiple methods and evaluate their impact on model performance

The dataset will be exported with NULL values intact for proper preprocessing in Python.
*/

--------------------------------------

-- Check for completely duplicate rows

/*
DUPLICATE DATA CHECK:

Performed a check for duplicate rows based on Country-Year combinations:
- No duplicate records were found in the dataset
- Each Country-Year combination appears exactly once
- This confirms the data integrity from a uniqueness perspective

This validation ensures that our time series analysis will have one data point per country per year.
*/

SELECT 
    Country,
    Year,
    COUNT(*) AS DuplicateCount
FROM Global_Economy_Indicators
GROUP BY Country, Year
HAVING COUNT(*) > 1
ORDER BY DuplicateCount DESC;

---------------------------------------
/*
SQL Phase Completion Note
-------------------------
The SQL phase of our analysis is now complete. We've explored the Global Economy Indicators dataset, assessed data quality, identified missing values, and examined basic relationships between variables.

Due to the comprehensive nature of this dataset (25+ columns spanning multiple economic indicators across countries and years), we'll transition to Python for the remaining analysis. The subsequent steps including:
- Data cleaning and imputation of missing values
- Feature engineering
- Exploratory data analysis with visualizations
- Machine learning model development
- Time series analysis

Python's rich ecosystem of data science libraries will provide greater flexibility for handling the complexity of this economic dataset compared to SQL.

The primary findings from our SQL analysis include:
- Most columns have very low missing data rates (<2%)
- Only the "Changes in inventories" column has a moderate missing rate (17.5%)
- There appears to be a strong correlation between GDP and various economic sectors
- Exchange rate data showed some inconsistencies that will require careful handling in Python

This completes the SQL portion of our analysis workflow.
*/