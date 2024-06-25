import time
from pprint import pprint

def monitor_job(client, job_id):
    retrieved_job = client.jobs.retrieve(job_id)
    while retrieved_job.status in ["RUNNING", "QUEUED"]:
        retrieved_job = client.jobs.retrieve(job_id)
        pprint(retrieved_job)
        print(f"Job is {retrieved_job.status}, waiting 10 seconds")
        time.sleep(10)
    return retrieved_job
