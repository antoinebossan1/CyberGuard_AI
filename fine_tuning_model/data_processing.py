import pandas as pd
from sklearn.model_selection import train_test_split
import os
import json
import uuid

def load_and_preprocess_data(directory_path):
    all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.csv')]
    print(f"Found {len(all_files)} CSV files in the directory.")
    print(f"all_files: {all_files}")

    df_list = []
    encodings = ['utf-8', 'latin1', 'ISO-8859-1']

    for file in all_files:
        for encoding in encodings:
            try:
                df = pd.read_csv(file, encoding=encoding)
                df_list.append(df)
                print(f"Successfully read {file} with encoding {encoding}")
                break
            except UnicodeDecodeError:
                print(f"Failed to read {file} with encoding {encoding}, trying next encoding.")
            except Exception as e:
                print(f"Failed to read {file} with error: {e}")
                break

    if not df_list:
        raise ValueError("No dataframes were loaded. Check your files and encodings.")
    
    df = pd.concat(df_list, ignore_index=True)

    def row_to_text(row):
        return (
            f"Flow ID: {row['Flow ID']}. Source IP: {row[' Source IP']}. "
            f"Source Port: {row[' Source Port']}. Destination IP: {row[' Destination IP']}. "
            f"Destination Port: {row[' Destination Port']}. Protocol: {row[' Protocol']}. "
            f"Timestamp: {row[' Timestamp']}. Flow Duration: {row[' Flow Duration']}. "
            f"Total Fwd Packets: {row[' Total Fwd Packets']}. Total Backward Packets: {row[' Total Backward Packets']}. "
            f"Total Length of Fwd Packets: {row['Total Length of Fwd Packets']}. Total Length of Bwd Packets: {row[' Total Length of Bwd Packets']}. "
            f"Fwd Packet Length Max: {row[' Fwd Packet Length Max']}. Fwd Packet Length Min: {row[' Fwd Packet Length Min']}. "
            f"Fwd Packet Length Mean: {row[' Fwd Packet Length Mean']}. Fwd Packet Length Std: {row[' Fwd Packet Length Std']}. "
            f"Bwd Packet Length Max: {row['Bwd Packet Length Max']}. Bwd Packet Length Min: {row[' Bwd Packet Length Min']}. "
            f"Bwd Packet Length Mean: {row[' Bwd Packet Length Mean']}. Bwd Packet Length Std: {row[' Bwd Packet Length Std']}. "
            f"Flow Bytes/s: {row['Flow Bytes/s']}. Flow Packets/s: {row[' Flow Packets/s']}. "
            f"Flow IAT Mean: {row[' Flow IAT Mean']}. Flow IAT Std: {row[' Flow IAT Std']}. "
            f"Flow IAT Max: {row[' Flow IAT Max']}. Flow IAT Min: {row[' Flow IAT Min']}. "
            f"Fwd IAT Total: {row['Fwd IAT Total']}. Fwd IAT Mean: {row[' Fwd IAT Mean']}. "
            f"Fwd IAT Std: {row[' Fwd IAT Std']}. Fwd IAT Max: {row[' Fwd IAT Max']}. "
            f"Fwd IAT Min: {row[' Fwd IAT Min']}. Bwd IAT Total: {row['Bwd IAT Total']}. "
            f"Bwd IAT Mean: {row[' Bwd IAT Mean']}. Bwd IAT Std: {row[' Bwd IAT Std']}. "
            f"Bwd IAT Max: {row[' Bwd IAT Max']}. Bwd IAT Min: {row[' Bwd IAT Min']}."
        )

    df['text'] = df.apply(row_to_text, axis=1)
    df = df.rename(columns={' Label': 'Label'})

    train_df, eval_df = train_test_split(df[['text', 'Label']], test_size=0.005, random_state=42)

    train_data = train_df.to_dict(orient='records')
    eval_data = eval_df.to_dict(orient='records')

    create_jsonl(train_data, "cicids2017_train.jsonl")
    create_jsonl(eval_data, "cicids2017_eval.jsonl")

    print("Training and validation data prepared and saved in JSONL format.")

def create_jsonl(data, filename):
    with open(filename, 'w') as f:
        for entry in data:
            jsonl_entry = {
                "prompt": entry['text'],
                "prompt_id": str(uuid.uuid4().hex),
                "messages": [
                    {"role": "user", "content": entry['text']},
                    {"role": "assistant", "content": entry['Label']}
                ]
            }
            f.write(json.dumps(jsonl_entry) + '\n')
