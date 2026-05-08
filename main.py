import pandas as pd
import time
from datetime import datetime
import config
from sender import send_email
import os

def load_status_df():
    if os.path.exists(config.STATUS_FILE):
        return pd.read_excel(config.STATUS_FILE)
    else:
        return pd.DataFrame(columns=["email", "status", "sent_at", "error"])

def save_status_df(df):
    df.to_excel(config.STATUS_FILE, index=False)

def update_status(df, email, status, error=None):
    sent_at = datetime.now().isoformat() if status == "SENT" else None
    
    # Check if email exists in df
    if email in df['email'].values:
        idx = df.index[df['email'] == email].tolist()[0]
        df.at[idx, 'status'] = status
        df.at[idx, 'sent_at'] = sent_at
        df.at[idx, 'error'] = error
    else:
        new_row = pd.DataFrame([{
            "email": email, 
            "status": status, 
            "sent_at": sent_at, 
            "error": error
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    
    save_status_df(df)
    return df

if __name__ == "__main__":
    # Load source emails
    df_source = pd.read_excel(config.EXCEL_PATH)
    source_emails = df_source["email"].dropna().unique()

    # Load status DF
    df_status = load_status_df()

    with open("templates/email.txt") as f:
        email_body = f.read()

    sent_count = 0

    print(f"Found {len(source_emails)} emails to process.")

    for email in source_emails:
        # Check if already sent
        existing_status = df_status.loc[df_status["email"] == email, "status"]
        if not existing_status.empty and existing_status.values[0] == "SENT":
            print(f"Skipping {email}: Already SENT")
            continue

        print(f"Sending to {email}...")
        try:
            send_email(email, email_body, config)
            df_status = update_status(df_status, email, "SENT")
            print(f" -> SENT")
            
            sent_count += 1
            time.sleep(config.DELAY_BETWEEN_EMAILS)

            if sent_count % config.BATCH_SIZE == 0:
                print(f"Batch limit reached. Sleeping for {config.DELAY_BETWEEN_BATCHES}s...")
                time.sleep(config.DELAY_BETWEEN_BATCHES)

        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            error_msg = str(e)
            print(f" -> FAILED: {error_msg}")
            df_status = update_status(df_status, email, "FAILED", error_msg)

    print("Done.")
