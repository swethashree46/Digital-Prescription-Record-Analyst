# import mysql.connector
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import warnings
# warnings.filterwarnings("ignore")
#
# # MySQL connection
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Swetha@546",
#     database="prescription_db"
# )
#
# cursor = conn.cursor()
#
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
#
# # Load your prescription data and drugs data
# prescription_df = pd.read_csv("prescription.csv")
# drugs_df = pd.read_csv("drugs.csv")
#
#
# # Normalize drug names to lowercase and strip spaces (optional but avoids mismatch issues)
# prescription_df['drug_name'] = prescription_df['drug_name'].str.strip().str.lower()
# drugs_df['Drug Name'] = drugs_df['Drug Name'].str.strip().str.lower()
#
# # Map 'Limited Dosage (mg/day)' to prescription_df
# prescription_df['limited_dosage'] = prescription_df['drug_name'].map(
#     drugs_df.set_index('Drug Name')['Limited Dosage (mg/day)']
# )
# print(prescription_df.head())
#
# ####1. PRESCRIBING TREND ANALYSIS - MOST COMMONLY PRESCRIBED DRUGS OVER TIME
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
#
# ###2. DRUG UTILIZATION AND DOSAGE PATTERN - HOW DIFF DRUGS ARE USED AND DOSAGE PATTERNS
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
#
# ### 3. ANAMALY DETECTION -
# # Filter anomalous prescriptions
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
#
# ## 4. GEOGRAPHIC ANALYSIS
# # Count prescriptions per city
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
#
#
#
# #### 5. DEMOGRAPHIC ANALYSIS
# # Create pivot table of city vs drug
# city_drug_matrix = prescription_df.pivot_table(
#     index='city',
#     columns='drug_name',
#     aggfunc='size',
#     fill_value=0
# )
#
# # Get top 10 cities and top 10 drugs by prescription count
# top_cities = city_drug_matrix.sum(axis=1).nlargest(10).index
# top_drugs = city_drug_matrix.sum(axis=0).nlargest(10).index
# filtered_matrix = city_drug_matrix.loc[top_cities, top_drugs]
#
# # HEATMAP
# plt.figure(figsize=(12, 8))
# sns.heatmap(filtered_matrix, annot=True, fmt='d', cmap='Reds')
# plt.title('Top Drugs Prescribed Across Top Cities')
# plt.xlabel('Drug Name')
# plt.ylabel('City')
# plt.tight_layout()
# plt.show()



# import mysql.connector
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import logging
# import warnings
# warnings.filterwarnings("ignore")
# import os
#
# # ------------------------Custom Exception
# class DataNotFoundError(Exception):
#     """Raised when required CSV data file is missing."""
#     pass
#
# # ------------------------Set up logging
# logging.basicConfig(
#     filename='prescription_analysis.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
#
# def connect_mysql():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Swetha@546",
#             database="prescription_db"
#         )
#         logging.info("MySQL connection successful!")
#         return conn
#     except mysql.connector.Error as err:
#         logging.error(f"MySQL connection failed: {err}")
#         raise
#
# def load_data_from_mysql(conn):
#     try:
#         df = pd.read_sql("SELECT * FROM prescription", conn)
#         drugs_df = pd.read_sql("SELECT * FROM drugs", conn)
#         logging.info("Data loaded from MySQL")
#         return df, drugs_df
#     except Exception as e:
#         logging.error(f"Error loading data from MySQL: {e}")
#         raise
#
# def load_csv(file_name):
#     if not os.path.exists(file_name):
#         logging.warning(f"{file_name} not found!")
#         raise DataNotFoundError(f"Required file '{file_name}' is missing.")
#     try:
#         df = pd.read_csv(file_name)
#         logging.info(f"{file_name} loaded successfully")
#         return df
#     except Exception as e:
#         logging.error(f"Error reading {file_name}: {e}")
#         raise
#
# def analysis_menu():
#         print("\nHey you!! Select the analysis you want to perform:")
#         print("1. Prescribing Trend Analysis - Top 5 most Prescribed drugs")
#         print("2. Drug Utilization and Dosage Pattern - Average dosage VS Limited dosage")
#         print("3. Anomaly Detection - Overdose")
#         print("4. Geographic Analysis - How prescription volumes vary by location ")
#         print("5. Demographic Analysis - Heatmap showing top prescribed drugs across top cities.")
#         print("6. Time-Based Prescription Trend - Monthly Prescription")
#         print("7. Diagnosis-Based Drug Mapping  - Diagnosis-Wise Drug Trends")
#         print("8. Exit - That's all I gonna leave")
#
# def perform_analysis(option, prescription_df, drugs_df):
#     try:
#         prescription_df['drug_name'] = prescription_df['drug_name'].str.strip().str.lower()
#         drugs_df['Drug Name'] = drugs_df['Drug Name'].str.strip().str.lower()
#
#         # Map limited dosage
#         prescription_df['limited_dosage'] = prescription_df['drug_name'].map(
#             drugs_df.set_index('Drug Name')['Limited Dosage (mg/day)']
#         )
#
#         if option == '1':
#             top_drugs = prescription_df['drug_name'].value_counts().nlargest(5)
#             top_drugs.plot(kind='bar', color='skyblue', edgecolor='black')
#             plt.title('Top 5 Most Prescribed Drugs')
#             plt.xlabel('Drug Name')
#             plt.ylabel('Number of Prescriptions')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '2':
#             avg_dosage = prescription_df.groupby('drug_name')['total_dose'].mean().reset_index()
#             avg_dosage.columns = ['drug_name', 'avg_total_dose']
#             utilization_df = pd.merge(avg_dosage, drugs_df, left_on='drug_name', right_on='Drug Name', how='left')
#             utilization_df['exceeds_limit'] = utilization_df['avg_total_dose'] > utilization_df['Limited Dosage (mg/day)']
#             overused = utilization_df[utilization_df['exceeds_limit'] == True]
#             print("Drugs with average total dose exceeding the limit:")
#             print(overused[['drug_name', 'avg_total_dose', 'Limited Dosage (mg/day)']])
#             top10 = utilization_df.head(10)
#             plt.bar(top10['drug_name'], top10['avg_total_dose'], label='Avg Prescribed Dosage', color='orange')
#             plt.plot(top10['drug_name'], top10['Limited Dosage (mg/day)'], color='green', marker='o', label='Limited Dosage')
#             plt.title('Avg Dosage vs Limited Dosage for Top 10 Drugs')
#             plt.xlabel('Drug Name')
#             plt.ylabel('Dosage (mg/day)')
#             plt.xticks(rotation=45)
#             plt.legend()
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '3':
#             anomalies_df = prescription_df[
#                 (prescription_df['limited_dosage'].notnull()) &
#                 (prescription_df['total_dose'] > prescription_df['limited_dosage'])
#             ]
#             anomaly_counts = anomalies_df['drug_name'].value_counts().head(10)
#             anomaly_counts.plot(kind='bar', color='salmon')
#             plt.title('Top Drugs with Overdosage Prescriptions')
#             plt.xlabel('Drug Name')
#             plt.ylabel('Number of Anomalies')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '4':
#             city_counts = prescription_df['city'].value_counts().head(10)
#             city_counts.plot(kind='bar', color='skyblue')
#             plt.title('Top 10 Cities by Prescription Volume')
#             plt.xlabel('City')
#             plt.ylabel('Number of Prescriptions')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '5':
#             city_drug_matrix = prescription_df.pivot_table(index='city', columns='drug_name', aggfunc='size', fill_value=0)
#             top_cities = city_drug_matrix.sum(axis=1).nlargest(10).index
#             top_drugs = city_drug_matrix.sum(axis=0).nlargest(10).index
#             filtered_matrix = city_drug_matrix.loc[top_cities, top_drugs]
#             plt.figure(figsize=(12, 8))
#             sns.heatmap(filtered_matrix, annot=True, fmt='d', cmap='Reds')
#             plt.title('Top Drugs Prescribed Across Top Cities')
#             plt.xlabel('Drug Name')
#             plt.ylabel('City')
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '6':
#             prescription_df['date'] = pd.to_datetime(prescription_df['date'])
#             monthly_trend = prescription_df.groupby(prescription_df['date'].dt.to_period('M')).size()
#             monthly_trend.plot(kind='line', marker='o', color='purple')
#             plt.title('Monthly Prescription Trend')
#             plt.xlabel("Month")
#             plt.ylabel("No. of Prescriptions")
#             plt.grid(True)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '7':
#             diagnosis_matrix = prescription_df.pivot_table(index='diagnosis', columns='drug_name', aggfunc='size', fill_value=0)
#             plt.figure(figsize=(14, 8))
#             sns.heatmap(diagnosis_matrix, cmap='YlGnBu')
#             plt.title('Drugs Prescribed for Each Diagnosis')
#             plt.xlabel('Drug Name')
#             plt.ylabel('Diagnosis')
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '8':
#             print("Bye!! Exiting analysis.")
#             return False
#
#         else:
#             print("Oh no!!Invalid option. Choose a number between 1 to 8.")
#
#         return True
#
#     except Exception as e:
#         logging.error(f"Error during analysis: {e}")
#         print("Something went wrong during analysis. Check logs for details.")
#         return True
#
# def main():
#     conn = None
#     try:
#         conn = connect_mysql()
#         sql_df, sql_drugs_df = load_data_from_mysql(conn)
#         print(sql_df.head())
#         prescription_df = load_csv("prescription.csv")
#         drugs_df = load_csv("drugs.csv")
#         if prescription_df is None or drugs_df is None:
#             return
#         while True:
#             analysis_menu()
#             user_input = input("Enter option (1-8): ").strip()
#             if not perform_analysis(user_input, prescription_df.copy(), drugs_df.copy()):
#                 break
#     except DataNotFoundError as dne:
#         print(dne)
#         logging.error(dne)
#     except Exception as e:
#         logging.error(f"Critical error: {e}")
#         print("A critical error occurred. Check logs for details.")
#     finally:
#         if conn:
#             conn.close()
#             logging.info("Connection closed.")
#
# if __name__ == "__main__":
#     main()
#
# import mysql.connector
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import logging
# import warnings
# warnings.filterwarnings("ignore")
#
# # Set up logging
# logging.basicConfig(
#     filename='prescription_analysis.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
#
# def connect_mysql():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Swetha@546",
#             database="prescription_db"
#         )
#         logging.info("MySQL connection successful!")
#         return conn
#     except mysql.connector.Error as err:
#         logging.error(f"MySQL connection failed: {err}")
#         raise
#
# def analysis_menu():
#     print("\nHey you!! Select the analysis you want to perform:")
#     print("1. Top 5 Most Prescribed Drugs")
#     print("2. Avg Dosage vs Limited Dosage (Top 10 Drugs)")
#     print("3. Anomaly Detection (Overdose)")
#     print("4. Geographic Analysis - Top Cities by Volume")
#     print("5. Demographic Analysis - Heatmap")
#     print("6. Diagnosis-Based Drug Mapping")
#     print("7. Exit")
#
# def perform_analysis(option, conn):
#     try:
#         cursor = conn.cursor()
#
#         if option == '1':
#             query = """SELECT drug_name, COUNT(*) AS count
#                        FROM prescription
#                        GROUP BY drug_name
#                        ORDER BY count DESC
#                        LIMIT 5;"""
#             df = pd.read_sql(query, conn)
#             df.plot(kind='bar', x='drug_name', y='count', color='skyblue', edgecolor='black')
#             plt.title("Top 5 Most Prescribed Drugs")
#             plt.xlabel("Drug Name")
#             plt.ylabel("No. of Prescriptions")
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '2':
#             query = """
#                 SELECT p.drug_name,
#                        ROUND(AVG(p.total_dose), 2) AS avg_dose,
#                        d.`Limited Dosage (mg/day)` AS limited_dosage
#                 FROM prescription p
#                 JOIN drugs d ON LOWER(TRIM(p.drug_name)) = LOWER(TRIM(d.`Drug Name`))
#                 GROUP BY p.drug_name
#                 ORDER BY avg_dose DESC
#                 LIMIT 10;
#             """
#             df = pd.read_sql(query, conn)
#             plt.bar(df['drug_name'], df['avg_dose'], label='Avg Prescribed Dosage', color='orange')
#             plt.plot(df['drug_name'], df['limited_dosage'], color='green', marker='o', label='Limited Dosage')
#             plt.title('Avg Dosage vs Limited Dosage for Top 10 Drugs')
#             plt.xlabel('Drug Name')
#             plt.ylabel('Dosage (mg/day)')
#             plt.xticks(rotation=45)
#             plt.legend()
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '3':
#             query = """
#                 SELECT p.drug_name, COUNT(*) AS overdose_count
#                 FROM prescription p
#                 JOIN drugs d ON LOWER(TRIM(p.drug_name)) = LOWER(TRIM(d.`Drug Name`))
#                 WHERE p.total_dose > d.`Limited Dosage (mg/day)`
#                 GROUP BY p.drug_name
#                 ORDER BY overdose_count DESC
#                 LIMIT 10;
#             """
#             df = pd.read_sql(query, conn)
#             df.plot(kind='bar', x='drug_name', y='overdose_count', color='salmon')
#             plt.title("Top Drugs with Overdosage Prescriptions")
#             plt.xlabel("Drug Name")
#             plt.ylabel("No. of Anomalies")
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '4':
#             query = """
#                 SELECT city, COUNT(*) AS count
#                 FROM prescription
#                 GROUP BY city
#                 ORDER BY count DESC
#                 LIMIT 10;
#             """
#             df = pd.read_sql(query, conn)
#             df.plot(kind='bar', x='city', y='count', color='skyblue')
#             plt.title("Top 10 Cities by Prescription Volume")
#             plt.xlabel("City")
#             plt.ylabel("Number of Prescriptions")
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '5':
#             query = """
#                 SELECT city, drug_name, COUNT(*) AS count
#                 FROM prescription
#                 GROUP BY city, drug_name;
#             """
#             df = pd.read_sql(query, conn)
#             pivot = df.pivot_table(index='city', columns='drug_name', values='count', fill_value=0)
#             top_cities = pivot.sum(axis=1).nlargest(10).index
#             top_drugs = pivot.sum(axis=0).nlargest(10).index
#             heatmap_data = pivot.loc[top_cities, top_drugs]
#             plt.figure(figsize=(12, 8))
#             sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Reds')
#             plt.title("Top Drugs Prescribed Across Top Cities")
#             plt.xlabel("Drug Name")
#             plt.ylabel("City")
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '6':
#             query = """
#                 SELECT diagnosis, drug_name, COUNT(*) AS count
#                 FROM prescription
#                 GROUP BY diagnosis, drug_name;
#             """
#             df = pd.read_sql(query, conn)
#             pivot = df.pivot_table(index='diagnosis', columns='drug_name', values='count', fill_value=0)
#             plt.figure(figsize=(14, 8))
#             sns.heatmap(pivot, cmap='YlGnBu')
#             plt.title("Drugs Prescribed for Each Diagnosis")
#             plt.xlabel("Drug Name")
#             plt.ylabel("Diagnosis")
#             plt.tight_layout()
#             plt.show()
#
#         elif option == '7':
#             print("Bye!! Exiting analysis.")
#             return False
#
#         else:
#             print("Invalid option. Please choose a number between 1 and 7.")
#
#         return True
#
#     except Exception as e:
#         logging.error(f"Error during analysis: {e}")
#         print("Something went wrong during analysis. Check logs for details.")
#         return True
#
# def main():
#     conn = None
#     try:
#         conn = connect_mysql()
#         while True:
#             analysis_menu()
#             user_input = input("Enter option (1-7): ").strip()
#             if not perform_analysis(user_input, conn):
#                 break
#     except Exception as e:
#         logging.error(f"Critical error: {e}")
#         print("A critical error occurred. Check logs for details.")
#     finally:
#         if conn:
#             conn.close()
#             logging.info("Connection closed.")
#
# if __name__ == "__main__":
#     main()

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import warnings
warnings.filterwarnings("ignore")

# ------------------------ Custom Exception
class DataNotFoundError(Exception):
    """Raised when required CSV data file is missing."""
    pass

# ------------------------ Logging Setup
logging.basicConfig(
    filename='prescription_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------------ MySQL Connection
def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Swetha@546",
            database="prescription_db"
        )
        logging.info("MySQL connection successful.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"MySQL connection failed: {err}")
        raise

# ------------------------ Menu
def analysis_menu():
    print("\nSelect an analysis to perform:")
    print("1. Prescribing Trend Analysis - Top 5 Most Prescribed Drugs")
    print("2. Drug Utilization and Dosage Pattern - Avg Dosage vs Limited Dosage")
    print("3. Anomaly Detection - Overdose")
    print("4. Geographic Analysis - Prescription Volumes by City")

    print("5. Diagnosis-Based Drug Mapping - Drug vs Diagnosis")
    print("6. Exit")

# ------------------------ Analysis Logic
def perform_analysis(option, conn):
    try:
        if option == '1':
            query = """
                SELECT drug_name, COUNT(*) AS prescription_count
                FROM prescription
                GROUP BY drug_name
                ORDER BY prescription_count DESC
                LIMIT 5;
            """
            df = pd.read_sql(query, conn)
            df['drug_name'] = df['drug_name'].str.title()
            df.plot(kind='bar', x='drug_name', y='prescription_count', color='skyblue', edgecolor='black')
            plt.title('Top 5 Most Prescribed Drugs')
            plt.xlabel('Drug Name')
            plt.ylabel('Number of Prescriptions')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif option == '2':
            query = """
                SELECT p.drug_name,
                AVG(p.total_dose) AS avg_total_dose,
                d.`Limited Dosage (mg/day)` AS limited_dosage
                FROM prescription p
                JOIN drugs d
                ON LOWER(TRIM(p.drug_name)) = LOWER(TRIM(d.`Drug Name`))
                WHERE d.`Limited Dosage (mg/day)` IS NOT NULL
                GROUP BY p.drug_name, d.`Limited Dosage (mg/day)`
                HAVING avg_total_dose IS NOT NULL
                ORDER BY avg_total_dose DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, conn)
            df['exceeds_limit'] = df['avg_total_dose'] > df['limited_dosage']
            print("Drugs exceeding limited dosage:")
            print(df[df['exceeds_limit']][['drug_name', 'avg_total_dose', 'limited_dosage']])
            plt.bar(df['drug_name'], df['avg_total_dose'], label='Avg Dosage', color='orange')
            plt.plot(df['drug_name'], df['limited_dosage'], color='green', marker='o', label='Limited Dosage')
            plt.title('Avg Dosage vs Limited Dosage')
            plt.xlabel('Drug Name')
            plt.ylabel('Dosage (mg/day)')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

        elif option == '3':
            query = """
                SELECT p.drug_name, COUNT(*) AS overdose_count
                FROM prescription p
                JOIN drugs d ON LOWER(TRIM(p.drug_name)) = LOWER(TRIM(d.`Drug Name`))
                WHERE p.total_dose > d.`Limited Dosage (mg/day)`
                GROUP BY p.drug_name
                ORDER BY overdose_count DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, conn)
            df.plot(kind='bar', x='drug_name', y='overdose_count', color='salmon')
            plt.title('Top 10 Drugs with Overdosage')
            plt.xlabel('Drug Name')
            plt.ylabel('No. of Overdose Cases')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif option == '4':
            query = """
                SELECT city, COUNT(*) AS count
                FROM prescription
                GROUP BY city
                ORDER BY count DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, conn)
            df.plot(kind='bar', x='city', y='count', color='skyblue')
            plt.title('Top 10 Cities by Prescription Volume')
            plt.xlabel('City')
            plt.ylabel('Number of Prescriptions')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()


        elif option == '5':
            query = """
                SELECT diagnosis, drug_name, COUNT(*) AS count
                FROM prescription
                GROUP BY diagnosis, drug_name;
            """
            df = pd.read_sql(query, conn)
            pivot = df.pivot_table(index='diagnosis', columns='drug_name', values='count', fill_value=0)
            plt.figure(figsize=(14, 8))
            sns.heatmap(pivot, cmap='YlGnBu')
            plt.title('Diagnosis vs Drug Mapping')
            plt.xlabel('Drug Name')
            plt.ylabel('Diagnosis')
            plt.tight_layout()
            plt.show()

        elif option == '6':
            print("Bye! Exiting analysis.")
            return False

        else:
            print(" Invalid option. Please select from 1 to 6.")
        return True

    except Exception as e:
        logging.error(f"Error in analysis {option}: {e}")
        print(" Error occurred during analysis. Check logs.")
        return True

def main():
    conn = None
    try:
        conn = connect_mysql()
        while True:
            analysis_menu()
            user_input = input("Enter option (1–6): ").strip()
            if not perform_analysis(user_input, conn):
                break
    except DataNotFoundError as dne:
        print(dne)
        logging.error(dne)
    except Exception as e:
        logging.error(f"Critical error: {e}")
        print("A critical error occurred. Check logs for details.")
    finally:
        if conn:
            conn.close()
            logging.info("MySQL connection closed.")

if __name__ == "__main__":
    main()

