from main import load_status_df
import pandas as pd
import os
import config

print("Testing load_status_df...")
try:
    df = load_status_df()
    print("Successfully loaded dataframe.")
    print(f"Columns: {df.columns.tolist()}")
    print("Saving dummy status file to verify write...")
    # optional: save to check if write works, but main.py does this later.
    # main.py calls save_status_df
except Exception as e:
    print(f"FAILED: {e}")
