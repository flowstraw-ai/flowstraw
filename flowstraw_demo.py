import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys

# ------------------------------
# CONFIG
# ------------------------------
DB_PATH = "flowstraw.db"
DATA_DIR = Path("data")
CUSTOMERS_CSV = DATA_DIR / "customers.csv"
PRODUCTS_CSV = DATA_DIR / "products.csv"
SALES_CSV = DATA_DIR / "sales.csv"
BIG_SALES_CSV = DATA_DIR / "sales_big.csv"  # for large demo


# ------------------------------
# DATA GENERATION
# ------------------------------

def generate_sample_data():
    """
    Generate customers.csv, products.csv, sales.csv if they don't exist.
    Customer IDs, Product IDs, and Sales rows are consistent with a star schema.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if CUSTOMERS_CSV.exists() and PRODUCTS_CSV.exists() and SALES_CSV.exists():
        print("[DATA] Sample CSVs already exist. Skipping generation.")
        return

    print("[DATA] Generating sample customers, products, sales CSVs...")

    # --- customers.csv ---
    customers = []
    customers.append([1, "John", "Doe", "M", "$10,000.00", "USA", "john.doe@example.com"])
    customers.append([2, "Jane", "Smith", "F", "$100,000.00", "USA", "jane.smith@example.com"])
    customers.append([3, "Raj", "Kumar", "M", "$787,999.00", "USA", "raj.kumar@example.com"])

    first_names = [
        "Emily","Michael","Sophia","Daniel","Olivia","Ethan","Ava","Liam","Mia","Noah","Isabella",
        "Lucas","Amelia","James","Charlotte","Benjamin","Harper","Alexander","Evelyn","Henry",
        "Abigail","Matthew","Samuel","Elizabeth","David","Sofia","Joseph","Avery","Jackson",
        "Ella","Owen","Grace","Wyatt","Chloe","Jack","Scarlett","Julian","Victoria","Leo",
        "Hannah","Isaac","Nora","Gabriel","Lillian","Dylan","Zoey","Caleb","Aria","Nathan",
        "Peyton","Christopher","Penelope","Andrew","Madison","Joshua","Layla","Elijah","Audrey",
        "William","Stella","Luke","Ellie","Carter","Natalie","Jayden","Luna","Ryan","Brooklyn",
        "Cameron","Hailey","Christian","Addison","Jonathan","Skylar","Isaiah","Sadie","Thomas",
        "Aurora","Brayden","Allison","Nicholas","Samantha","Anna","Adrian","Claire","Easton",
        "Riley","Grayson","Paisley","Cooper","Elena","Aaron","Jason","Sienna"
    ]

    last_names = [
        "Johnson","Williams","Brown","Jones","Miller","Davis","Garcia","Martinez","Rodriguez","Hernandez",
        "Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee",
        "Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker",
        "Young","Hall","Allen","King","Wright","Scott","Green","Baker","Adams","Nelson","Hill","Rivera",
        "Campbell","Mitchell","Carter","Roberts","Gomez","Phillips","Evans","Turner","Diaz","Parker",
        "Cruz","Edwards","Collins","Stewart","Morris","Rogers","Reed","Cook","Morgan","Bell","Murphy",
        "Bailey","Richardson","Cox","Howard","Ward","Torres","Peterson","Gray","Ramsey","Kim",
        "Hamilton","Graham","Fisher","Wallace","Woods","Cole","West","Jenkins","Stone","Bishop",
        "Harper","Wheeler","Chapman","Fox","Hudson","Hunt","Burns","Black","Holmes","Fields",
        "Olson","Arnold"
    ]

    genders = ["M", "F"]

    for i in range(4, 101):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        gender = random.choice(genders)
        salary_val = random.randint(40_000, 150_000)
        salary_str = f"${salary_val:,.2f}"
        email = f"{fn.lower()}.{ln.lower()}@example.com"
        customers.append([i, fn, ln, gender, salary_str, "USA", email])

    customers_df = pd.DataFrame(
        customers,
        columns=["CustomerID", "FirstName", "LastName", "Gender", "Salary", "Country", "Email"]
    )
    customers_df.to_csv(CUSTOMERS_CSV, index=False)
    print(f"[DATA] Wrote {len(customers_df)} customers to {CUSTOMERS_CSV}")

    # --- products.csv ---
    products = []
    product_names = [
        ("Laptop Pro 14", "Electronics"),
        ("Laptop Air 13", "Electronics"),
        ("4K Monitor 27", "Electronics"),
        ("Mechanical Keyboard", "Electronics"),
        ("Wireless Mouse", "Electronics"),
        ("Noise-Canceling Headphones", "Electronics"),
        ("Office Chair Ergo", "Furniture"),
        ("Standing Desk", "Furniture"),
        ("Conference Table", "Furniture"),
        ("LED Desk Lamp", "Furniture"),
        ("Team License - Analytics", "Software"),
        ("Cloud Backup 1TB", "Software"),
        ("CRM Seat License", "Software"),
        ("Email Automation Suite", "Software"),
        ("Security Suite", "Software"),
    ]

    product_id = 1
    for name, cat in product_names:
        base_price = random.randint(80, 2500)
        price = round(base_price + random.random() * 200, 2)
        cost = round(price * random.uniform(0.5, 0.8), 2)
        products.append([product_id, name, cat, price, cost])
        product_id += 1

    products_df = pd.DataFrame(
        products,
        columns=["ProductID", "ProductName", "Category", "UnitPrice", "UnitCost"]
    )
    products_df.to_csv(PRODUCTS_CSV, index=False)
    print(f"[DATA] Wrote {len(products_df)} products to {PRODUCTS_CSV}")

    # --- sales.csv ---
    regions = ["West", "East", "North", "South", "Central"]
    start_date = datetime(2024, 1, 1)
    num_days = 365

    sales = []
    sale_id = 1
    num_rows = 2000  # demo size

    for _ in range(num_rows):
        cust = random.choice(customers)
        cust_id = cust[0]
        prod = random.choice(products)
        prod_id = prod[0]
        unit_price = prod[3]
        qty = random.randint(1, 10)
        total = round(unit_price * qty, 2)
        delta = random.randint(0, num_days - 1)
        sale_date = (start_date + timedelta(days=delta)).strftime("%Y-%m-%d")
        region = random.choice(regions)
        sales.append([sale_id, sale_date, cust_id, prod_id, qty, unit_price, total, region])
        sale_id += 1

    sales_df = pd.DataFrame(
        sales,
        columns=["SaleID", "SaleDate", "CustomerID", "ProductID", "Quantity", "UnitPrice", "TotalAmount", "Region"]
    )
    sales_df.to_csv(SALES_CSV, index=False)
    print(f"[DATA] Wrote {len(sales_df)} sales rows to {SALES_CSV}")
    print("[DATA] Sample data generation complete.")


def generate_big_sales(n_rows=1_000_000):
    """
    Generate a large sales CSV (sales_big.csv) for performance/load demos.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CUSTOMERS_CSV.exists() or not PRODUCTS_CSV.exists():
        print("[BIG DATA] Base customers/products missing. Generating base sample data first...")
        generate_sample_data()

    print(f"[BIG DATA] Generating {n_rows:,} sales rows into {BIG_SALES_CSV} ...")

    customers = pd.read_csv(CUSTOMERS_CSV)["CustomerID"].tolist()
    products = pd.read_csv(PRODUCTS_CSV)[["ProductID", "UnitPrice"]].values.tolist()

    regions = ["West", "East", "North", "South", "Central"]
    start_date = datetime(2024, 1, 1)
    num_days = 365

    rows = []
    sale_id = 1
    for _ in range(n_rows):
        cust_id = random.choice(customers)
        prod_id, unit_price = random.choice(products)
        qty = random.randint(1, 10)
        total = round(unit_price * qty, 2)
        delta = random.randint(0, num_days - 1)
        sale_date = (start_date + timedelta(days=delta)).strftime("%Y-%m-%d")
        region = random.choice(regions)
        rows.append([sale_id, sale_date, cust_id, prod_id, qty, unit_price, total, region])
        sale_id += 1

    df = pd.DataFrame(
        rows,
        columns=["SaleID", "SaleDate", "CustomerID", "ProductID", "Quantity", "UnitPrice", "TotalAmount", "Region"]
    )
    df.to_csv(BIG_SALES_CSV, index=False)
    print(f"[BIG DATA] Wrote {len(df):,} rows to {BIG_SALES_CSV}")


# ------------------------------
# ETL: CSV -> STAGING -> STAR SCHEMA
# ------------------------------

def load_csv_to_table(conn, csv_path: Path, table_name: str):
    """
    Load CSV into SQLite, replacing the table if it exists.
    This makes it robust whether the table exists or not.
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"[ETL] Loaded {len(df):,} rows into {table_name}")


def build_star_schema(conn):
    """
    Build dim_customer, dim_product, dim_date, fact_sales from staging tables.
    All CREATEs are preceded by DROP TABLE IF EXISTS to handle 'table exists / not exists'.
    """
    cur = conn.cursor()
    print("[ETL] Building star schema tables...")

    # DIM CUSTOMER
    cur.execute("DROP TABLE IF EXISTS dim_customer;")
    cur.execute("""
        CREATE TABLE dim_customer AS
        SELECT
            CustomerID         AS customer_key,
            FirstName          AS first_name,
            LastName           AS last_name,
            Gender             AS gender,
            Salary             AS salary_text,
            Country            AS country,
            Email              AS email
        FROM stg_customers;
    """)

    # DIM PRODUCT
    cur.execute("DROP TABLE IF EXISTS dim_product;")
    cur.execute("""
        CREATE TABLE dim_product AS
        SELECT
            ProductID          AS product_key,
            ProductName        AS product_name,
            Category           AS category,
            UnitPrice          AS list_price,
            UnitCost           AS unit_cost
        FROM stg_products;
    """)

    # DIM DATE
    cur.execute("DROP TABLE IF EXISTS dim_date;")
    cur.execute("""
        CREATE TABLE dim_date AS
        SELECT
            DISTINCT
            REPLACE(SaleDate, '-', '')              AS date_key,
            SaleDate                                 AS date,
            SUBSTR(SaleDate, 1, 4)                  AS year,
            SUBSTR(SaleDate, 6, 2)                  AS month,
            SUBSTR(SaleDate, 9, 2)                  AS day
        FROM stg_sales;
    """)

    # FACT SALES
    cur.execute("DROP TABLE IF EXISTS fact_sales;")
    cur.execute("""
        CREATE TABLE fact_sales AS
        SELECT
            s.SaleID                      AS sale_id,
            REPLACE(s.SaleDate, '-', '')  AS date_key,
            s.CustomerID                  AS customer_key,
            s.ProductID                   AS product_key,
            s.Quantity                    AS quantity,
            s.UnitPrice                   AS unit_price,
            s.TotalAmount                 AS total_amount,
            s.Region                      AS region
        FROM stg_sales s;
    """)

    conn.commit()
    print("[ETL] Star schema tables created: dim_customer, dim_product, dim_date, fact_sales")


def run_etl(use_big_sales: bool = False):
    """
    Execute the full ETL:
    - ensure data exists
    - load staging tables
    - build star schema
    """
    if use_big_sales:
        if not BIG_SALES_CSV.exists():
            print("[ETL] Big sales CSV not found. Generating 1,000,000-row file...")
            generate_big_sales(1_000_000)
        sales_source = BIG_SALES_CSV
    else:
        if not (CUSTOMERS_CSV.exists() and PRODUCTS_CSV.exists() and SALES_CSV.exists()):
            print("[ETL] Sample data not found. Generating base data...")
            generate_sample_data()
        sales_source = SALES_CSV

    print(f"[ETL] Using sales source: {sales_source}")

    conn = sqlite3.connect(DB_PATH)
    try:
        load_csv_to_table(conn, CUSTOMERS_CSV, "stg_customers")
        load_csv_to_table(conn, PRODUCTS_CSV, "stg_products")
        load_csv_to_table(conn, sales_source, "stg_sales")
        build_star_schema(conn)
    finally:
        conn.close()
        print(f"[ETL] ETL complete. SQLite DB: {DB_PATH}")


# ------------------------------
# ANALYTICS DASHBOARD LAUNCHER
# ------------------------------

def launch_analytics_dashboard():
    """
    Launch the Streamlit analytics app (analytics_app.py).
    Requires 'streamlit' installed and analytics_app.py in the same folder.
    """
    app_path = Path("analytics_app.py")
    if not app_path.exists():
        print("[DASHBOARD] analytics_app.py not found in current directory.")
        print("            Please save the Streamlit app code as analytics_app.py next to this script.")
        return

    print("[DASHBOARD] Starting Streamlit analytics dashboard...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "analytics_app.py"], check=False)
    except FileNotFoundError:
        print("[DASHBOARD] Streamlit not found. Install it with: pip install streamlit")


# ------------------------------
# MENU / MAIN
# ------------------------------

def main_menu():
    while True:
        print("\n==============================")
        print(" FlowStraw Demo Runner")
        print("==============================")
        print("1) Ensure sample CSV data (customers/products/sales)")
        print("2) Run ETL (sample data -> SQLite star schema)")
        print("3) Generate BIG sales CSV + run ETL")
        print("4) Launch Analytics Dashboard (Streamlit)")
        print("5) Exit")
        choice = input("Choose an option [1-5]: ").strip()

        if choice == "1":
            generate_sample_data()
        elif choice == "2":
            run_etl(use_big_sales=False)
        elif choice == "3":
            run_etl(use_big_sales=True)
        elif choice == "4":
            launch_analytics_dashboard()
        elif choice == "5":
            print("Exiting FlowStraw Demo Runner.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()
