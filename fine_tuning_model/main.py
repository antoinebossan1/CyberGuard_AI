import os
from data_processing import load_and_preprocess_data
from file_operations import reformat_data, split_jsonl_file
from fine_tuning import upload_datasets, create_fine_tuning_job
from monitor import monitor_job
from utils import load_env, pprint_file
from mistralai.client import MistralClient

if __name__ == "__main__":
    directory_path = '/Users/guidance/Desktop/CyberGuard_AI/data/TrafficLabelling'
    load_and_preprocess_data(directory_path)

    api_key = load_env()
    
    reformat_data("cicids2017_train.jsonl")
    reformat_data("cicids2017_eval.jsonl")
    
    split_jsonl_file("cicids2017_train.jsonl", ["cicids2017_train_1.jsonl", "cicids2017_train_2.jsonl", "cicids2017_train_3.jsonl"])

    client = MistralClient(api_key=api_key)
    train_files = ["cicids2017_train_1.jsonl", "cicids2017_train_2.jsonl", "cicids2017_train_3.jsonl"]
    eval_file = "cicids2017_eval.jsonl"
    
    for file in train_files + [eval_file]:
        size = os.path.getsize(file)
        print(f"File {file} size: {size} bytes")

    file_ids = upload_datasets(api_key, train_files + [eval_file])
    
    if file_ids:
        validation_file_id = file_ids[-1]
        job = create_fine_tuning_job(client, file_ids[:-1], validation_file_id)
        if job:
            completed_job = monitor_job(client, job.id)
            pprint_file(completed_job)
