from dotenv import load_dotenv
import os
import json

def load_env():
    load_dotenv()
    return os.environ.get("MISTRAL_API_KEY")


def pprint_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)