# Retail-Sales-Analytics
Retail Sales Data Engineering & Analytics Solution
Project Overview

This project presents an end-to-end Retail Sales Data Engineering and Analytics Solution developed to transform raw retail transaction data into meaningful business insights. The solution covers data ingestion, cleaning, standardization, transformation, validation, secure handling of customer information, SQL-based analysis, and interactive Power BI dashboards.

The primary objective of the project is to create a reliable and analytics-ready dataset that supports business reporting, KPI monitoring, and data-driven decision-making.

Solution Architecture

The solution follows a layered architecture consisting of five major components:

1. Source Layer

Raw retail data is collected from multiple Excel datasets containing product details and transaction records. These files serve as the input source for the data engineering pipeline.

2. Processing Layer

Python and Pandas are used to process the raw data. This layer performs data cleaning, standardization, transformation, PII masking, and validation to improve data quality and consistency.

3. Storage Layer

The processed data is stored as CSV files and in a SQLite database. This provides centralized storage and enables efficient querying and analysis.

4. Analytics Layer

SQL queries are used to calculate key business metrics such as revenue, transactions, customer counts, category performance, and regional performance.

5. Visualization Layer

Power BI dashboards are developed to present business insights through interactive visualizations and KPI reports.

Data Flow

The project follows the following workflow:

Raw Excel Files
↓
Data Ingestion
↓
Data Cleaning
↓
Data Standardization
↓
Data Transformation
↓
PII Masking
↓
Data Validation
↓
CSV & SQLite Storage
↓
SQL Analysis
↓
Power BI Dashboards
↓
Business Insights

Data Processing Workflow
Data Cleaning
Identified missing values and handled missing product prices.
Reviewed duplicate transactions and data quality issues.
Improved dataset completeness and reliability.
Data Standardization
Standardized product names.
Standardized category values.
Standardized city names and payment methods.
Data Transformation
Generated Revenue metric.
Created Year, Month, and Quarter attributes.
Prepared the dataset for KPI calculations and reporting.
PII Masking
Masked customer email addresses.
Masked customer phone numbers.
Protected sensitive customer information.
Data Validation
Verified price, quantity, and discount values.
Performed integrity checks on transaction records.
Ensured dataset accuracy before storage.
Analytics Performed

The processed dataset was analyzed using SQL to generate business insights including:

Total Revenue
Total Transactions
Unique Customers
Average Order Value
Revenue by Category
Revenue by City
Product Performance Analysis
Regional Performance Analysis
Dashboard Modules
Retail Sales Performance Dashboard

Provides an overview of key business KPIs including revenue, transactions, customers, and category performance.

Revenue Analysis Dashboard

Analyzes monthly revenue trends, quarterly performance, payment methods, and purchase locations.

Product Performance Dashboard

Identifies top-performing products, revenue contribution by product, and quantity sold across categories.

Regional Insights Dashboard

Analyzes city-wise revenue, transaction distribution, average revenue per transaction, and online vs offline sales performance.

Technologies Used
Python
Pandas
NumPy
SQLite
SQL
Power BI
Microsoft Excel
Business Outcome

The project successfully transformed raw retail transaction data into a clean, validated, and analytics-ready dataset. Through SQL analysis and Power BI dashboards, the solution enables stakeholders to monitor business performance, identify trends, evaluate product contributions, analyze regional sales, and make informed business decisions.
