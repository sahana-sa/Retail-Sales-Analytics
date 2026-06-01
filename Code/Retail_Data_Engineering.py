#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# In[13]:


import os

print("Current Working Directory:")
print(os.getcwd())

print("\nFiles and Folders:")
print(os.listdir())

print(os.listdir(".."))



print(os.listdir("../data"))


# DATA INGESTION

# In[15]:


#Load Data
file_path = r"../data/USECASE - Data Engineering.xlsx"

excel_file = pd.ExcelFile(file_path)

print(excel_file.sheet_names)


# In[17]:


products = pd.read_excel(
    file_path,
    sheet_name="product_details"
)

retail1 = pd.read_excel(
    file_path,
    sheet_name="retail_data1"
)

retail2 = pd.read_excel(
    file_path,
    sheet_name="retail_data2"
)

print(products.shape)
print(retail1.shape)
print(retail2.shape)


# In[19]:


#Combine Retail Data
retail = pd.concat(
    [retail1, retail2],
    ignore_index=True
)

print(retail.shape)
retail.head()


# DATA CLEANING

# In[21]:


# Check missing values
print("\nMissing Values:")
print(retail.isnull().sum())


# In[23]:


#Check full dupliacte rows
print("\nFull Duplicate Rows:")
print(retail.duplicated().sum())


# In[25]:


#Check Categories
print("\nUnique Categories:")
print(retail["category"].unique())


# In[27]:


#Standardize Category Values
category_map = {
    "electronics":"Electronics",
    "ELEC":"Electronics",

    "furniture":"Furniture",
    "FURN":"Furniture",

    "home appliances":"Home Appliances",
    "HOME":"Home Appliances",

    "clothing":"Clothing",
    "CLOTH":"Clothing"
}

retail["category"] = retail["category"].replace(category_map)

print("\nCategories After Cleaning:")
print(retail["category"].unique())


# In[29]:


#Check Product Names
print("\nUnique Product Names:")
print(retail["product_name"].unique())


# In[31]:


#Standardize Product Names
retail["product_name"] = (
    retail["product_name"]
    .str.title()
)

print("\nProduct Names After Cleaning:")
print(retail["product_name"].unique())


# In[33]:


#Check Date Formats
print("\nUnique Date Formats:")
print(retail["transaction_date"].head(20))


# In[35]:


#Fix Date Formats
retail["transaction_date"] = pd.to_datetime(
    retail["transaction_date"],
    errors="coerce"
)

print("\nInvalid Dates:")
print(retail["transaction_date"].isnull().sum())


# In[37]:


#Check Product Master Sheet
products = pd.read_excel(file_path,sheet_name="product_details")
print("\nProduct Master Sheet:")
print(products.head())
print(products.columns)
print(products.shape)


# In[39]:


# Revenue Calculation
retail["revenue"] = (
    retail["price"]
    * retail["quantity"]
    * (1 - retail["discount"])
)

print("\nRevenue Sample:")
print(
    retail[ 
        ["price","quantity","discount","revenue"]
    ].head()
)


# In[41]:


#Create Time Features
retail["year"] = retail["transaction_date"].dt.year
retail["month"] = retail["transaction_date"].dt.month
retail["quarter"] = retail["transaction_date"].dt.quarter

print("\nTime Features:")
print(
    retail[
        ["transaction_date","year","month","quarter"]
    ].head()
)


# In[43]:


# PII Masking

retail["email"] = retail["email"].apply(
    lambda x: x[:2] + "***@" + x.split("@")[1]
)

retail["phone"] = retail["phone"].astype(str).apply(
    lambda x: "******" + x[-4:]
)

print("\nPII Masking Completed")


# In[45]:


#Save Dataset
import os
os.makedirs("output", exist_ok=True)

retail.to_csv(
    "output/cleaned_data.csv",
    index=False
)

print("Dataset saved successfully!")


# DATA VALIDATION
# 

# In[48]:


df = pd.read_csv("output/cleaned_data.csv")


# In[50]:


print("Invalid Prices:")
print((df["price"] <= 0).sum())


# In[52]:


print("Invalid Quantities:")
print((df["quantity"] <= 0).sum())


# In[54]:


# Show invalid quantity records

invalid_qty = df[df["quantity"] <= 0]

print("\nInvalid Quantity Records:")
print(invalid_qty.head(10))


# In[56]:


print("Invalid Discounts:")
print(
    ((df["discount"] < 0) |
     (df["discount"] > 1)).sum()
)


# In[58]:


print("Duplicate Transaction IDs:")
print(
    df.duplicated(
        subset=["transaction_id"]
    ).sum()
)


# In[60]:


# Show duplicate transaction records
duplicate_txn = df[
    df.duplicated(
        subset=["transaction_id"],
        keep=False
    )
]

print("\nDuplicate Transaction Records:")
print(
    duplicate_txn[
        ["transaction_id",
         "customer_id",
         "product_name",
         "quantity",
         "revenue"]
    ].head(20)
)


# In[62]:


df.to_csv(
    "output/transformed_data.csv",
    index=False
)

print("Dataset saved successfully!")


# In[64]:


from sqlalchemy import create_engine

engine = create_engine("sqlite:///retail.db")

retail.to_sql(
    "retail_sales",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully!")


# In[66]:


import sqlite3
import pandas as pd

conn = sqlite3.connect("retail.db")

queries = {
    "Total Revenue": """
        SELECT SUM(revenue) AS total_revenue
        FROM retail_sales
    """,

    "Revenue by Category": """
        SELECT category,
               SUM(revenue) AS revenue
        FROM retail_sales
        GROUP BY category
    """,

    "Revenue by City": """
        SELECT city,
               SUM(revenue) AS revenue
        FROM retail_sales
        GROUP BY city
    """,

    "Top 10 Products": """
        SELECT product_name,
               SUM(revenue) AS revenue
        FROM retail_sales
        GROUP BY product_name
        ORDER BY revenue DESC
        LIMIT 10
    """,

    "Monthly Revenue": """
        SELECT month,
               SUM(revenue) AS revenue
        FROM retail_sales
        GROUP BY month
        ORDER BY month
    """
}

for title, query in queries.items():
    print("\n" + "=" * 50)
    print(title)
    print(pd.read_sql_query(query, conn))

conn.close()


# EDA
# 

# In[69]:


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

sns.barplot(
    data=retail,
    x="category",
    y="revenue",
    estimator=sum
)

plt.title("Revenue by Category")
plt.show()


# In[70]:


monthly = retail.groupby("month")["revenue"].sum()

plt.figure(figsize=(8,5))

monthly.plot(marker="o")

plt.title("Monthly Revenue Trend")
plt.show()


# In[71]:


city_revenue = retail.groupby("city")["revenue"].sum()

city_revenue.sort_values(
    ascending=False
).plot(
    kind="bar",
    figsize=(10,5)
)

plt.title("Revenue by City")
plt.show()


# In[72]:


top_products = (
    retail.groupby("product_name")["revenue"]
          .sum()
          .sort_values(ascending=False)
          .head(10)
)

top_products.plot(
    kind="bar",
    figsize=(10,5)
)

plt.title("Top 10 Products")
plt.show()


# In[ ]:




