import os
import json

def reformat_data(filename):
    os.system("wget https://raw.githubusercontent.com/mistralai/mistral-finetune/main/utils/reformat_data.py")
    os.system(f"python reformat_data.py {filename}")

def validate_data(filename):
    os.system("wget https://raw.githubusercontent.com/mistralai/mistral-finetune/main/utils/validate_data.py")
    os.system(f"python validate_data.py {filename}")

def split_jsonl_file(input_file, output_files):
    output_file_objects = [open(file, "w") for file in output_files]
    counter = 0
    with open(input_file, "r") as f_in:
        for line in f_in:
            data = json.loads(line)
            output_file_objects[counter].write(json.dumps(data) + "\n")
            counter = (counter + 1) % len(output_files)
    for file in output_file_objects:
        file.close()
