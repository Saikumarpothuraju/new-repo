import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# Step 1: Create In-Memory SQLite Database
# ==================================================
conn = sqlite3.connect(":memory:")

# ==================================================
# Step 2: Create Employees Table
# ==================================================
conn.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    salary REAL
)
""")

# ==================================================
# Step 3: Insert Sample Rows
# ==================================================
conn.executemany(
    "INSERT INTO employees (name, age, salary) VALUES (?, ?, ?)", [
        ("Alice", 25, 50000),
        ("Bob", 30, 60000),
        ("Charlie", 28, 55000),
        ("David", 35, 70000),
        ("Eva", 29, 48000)
    ]
)
conn.commit()

# ==================================================
# Step 4: Read SQL Table into Pandas DataFrame
# ==================================================
df_sql = pd.read_sql("SELECT * FROM employees", conn)
print("=== Employees Data from SQLite ===")
print(df_sql)

# ==================================================
# Step 5: Filtering with Pandas
# ==================================================
print("\n=== Employees with Salary > 55,000 ===")
high_salary = df_sql[df_sql['salary'] > 55000]
print(high_salary)

print("\n=== Employees aged below 30 ===")
young_employees = df_sql[df_sql['age'] < 30]
print(young_employees)

# ==================================================
# Step 6: Write DataFrame back into SQLite
# ==================================================
high_salary.to_sql("high_salary_employees", conn, index=False, if_exists="replace")

df_high_salary = pd.read_sql("SELECT * FROM high_salary_employees", conn)
print("\n=== High Salary Employees Table from SQLite ===")
print(df_high_salary)

# ==================================================
# Step 7: Visualization with Matplotlib
# ==================================================
print("\n=== Salary Distribution (Bar Chart) ===")
plt.figure(figsize=(8,5))
plt.bar(df_sql['name'], df_sql['salary'], color='skyblue')
plt.title("Employee Salary Distribution")
plt.xlabel("Employee")
plt.ylabel("Salary")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
