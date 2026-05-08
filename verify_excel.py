import pandas as pd
import config
import os

print(f"Pandas version: {pd.__version__}")
print(f"Status file: {config.STATUS_FILE}")
print(f"File exists: {os.path.exists(config.STATUS_FILE)}")

try:
    print("Attempting to read excel file (default engine)...")
    df = pd.read_excel(config.STATUS_FILE)
    print("Success!")
    print(df.head())
except Exception as e:
    print(f"Failed with default: {e}")

try:
    print("\nAttempting to read excel file (engine='openpyxl')...")
    df = pd.read_excel(config.STATUS_FILE, engine='openpyxl')
    print("Success with engine='openpyxl'!")
    print(df.head())
except Exception as e:
    print(f"Failed with openpyxl: {e}")
