import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Swetha@546",
    database="prescription_db"
)

cursor = conn.cursor()

# # Read 'prescription' table
# query = "SELECT * FROM prescription"
# df = pd.read_sql(query, conn)
#
# # Show first 5 rows
# print(df.head())
#
# # Read 'drugs' table
# query = "SELECT * FROM drugs"
# drugs_df = pd.read_sql(query, conn)
#
# # Show preview
# print("Drugs Table:")
# print(drugs_df.head())

# Load your prescription data and drugs data
prescription_df = pd.read_csv("prescription.csv")
drugs_df = pd.read_csv("drugs.csv")

#
# Normalize drug names to lowercase and strip spaces (optional but avoids mismatch issues)
prescription_df['drug_name'] = prescription_df['drug_name'].str.strip().str.lower()
drugs_df['Drug Name'] = drugs_df['Drug Name'].str.strip().str.lower()

# Map 'Limited Dosage (mg/day)' to prescription_df
prescription_df['limited_dosage'] = prescription_df['drug_name'].map(
    drugs_df.set_index('Drug Name')['Limited Dosage (mg/day)']
)
# print(prescription_df.head())

####1. PRESCRIBING TREND ANALYSIS - MOST COMMONLY PRESCRIBED DRUGS OVER TIME
# top_drugs = prescription_df['drug_name'].value_counts().nlargest(5)
#
# plt.figure(figsize=(8, 5))
# top_drugs.plot(kind='bar', color='skyblue', edgecolor='black')
# plt.title('Top 5 Most Prescribed Drugs')
# plt.xlabel('Drug Name')
# plt.ylabel('Number of Prescriptions')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

####2. DRUG UTILIZATION AND DOSAGE PATTERN - HOW DIFF DRUGS ARE USED AND DOSAGE PATTERNS
# # Group by drug and calculate average prescribed dosage
# avg_dosage = prescription_df.groupby('drug_name')['total_dose'].mean().reset_index()
# avg_dosage.columns = ['drug_name', 'avg_total_dose']
# # Merge with limited dosage
# utilization_df = pd.merge(avg_dosage, drugs_df, left_on='drug_name', right_on='Drug Name', how='left')
# # Compare avg_total_dose vs. limited dosage
# utilization_df['exceeds_limit'] = utilization_df['avg_total_dose'] > utilization_df['Limited Dosage (mg/day)']
# # Show drugs that exceed recommended dosage
# overused = utilization_df[utilization_df['exceeds_limit'] == True]
# print("Drugs with average total dose exceeding the limit:")
# print(overused[['drug_name', 'avg_total_dose', 'Limited Dosage (mg/day)']])
#
# # Bar chart
# top10 = utilization_df.head(10)
#
# plt.figure(figsize=(10, 6))
# plt.bar(top10['drug_name'], top10['avg_total_dose'], label='Avg Prescribed Dosage', color='orange')
# plt.plot(top10['drug_name'], top10['Limited Dosage (mg/day)'], color='green', marker='o', label='Limited Dosage')
#
# plt.title('Avg Dosage vs Limited Dosage for Top 10 Drugs')
# plt.xlabel('Drug Name')
# plt.ylabel('Dosage (mg/day)')
# plt.xticks(rotation=45)
# plt.legend()
# plt.tight_layout()
# plt.show()

#### 3. ANAMALY DETECTION -
## Filter anomalous prescriptions
# anomalies_df = prescription_df[
#     (prescription_df['limited_dosage'].notnull()) &
#     (prescription_df['total_dose'] > prescription_df['limited_dosage'])
# ]
# # Count anomalies per drug
# anomaly_counts = anomalies_df['drug_name'].value_counts().head(10)
# # BAR CHART
# plt.figure(figsize=(10, 6))
# anomaly_counts.plot(kind='bar', color='salmon')
# plt.title('Top Drugs with Overdosage Prescriptions')
# plt.xlabel('Drug Name')
# plt.ylabel('Number of Anomalies')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

#### 4. GEOGRAPHIC ANALYSIS
# Count prescriptions per city
# city_counts = prescription_df['city'].value_counts().head(10)
#
# # BAR CHART
# plt.figure(figsize=(10, 6))
# city_counts.plot(kind='bar', color='skyblue')
# plt.title('Top 10 Cities by Prescription Volume')
# plt.xlabel('City')
# plt.ylabel('Number of Prescriptions')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()



#### 5. DEMOGRAPHIC ANALYSIS
# city vs drug name






