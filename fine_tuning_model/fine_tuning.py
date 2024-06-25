from mistralai.client import MistralClient
from mistralai.models.jobs import TrainingParameters

def upload_datasets(api_key, filenames):
    client = MistralClient(api_key=api_key)
    file_ids = []
    try:
        for filename in filenames:
            with open(filename, "rb") as f:
                uploaded_file = client.files.create(
                    file=(filename, f)
                )
                file_ids.append(uploaded_file.id)
        return file_ids
    except Exception as e:
        print(f"Error uploading datasets: {e}")
        return None

def create_fine_tuning_job(client, training_file_ids, validation_file_id):
    try:
        created_jobs = client.jobs.create(
            model="open-mistral-7b",
            training_files=training_file_ids,
            validation_files=[validation_file_id],
            hyperparameters=TrainingParameters(
                training_steps=10,
                learning_rate=0.0001,
            )
        )
        return created_jobs
    except Exception as e:
        print(f"Error creating fine-tuning job: {e}")
        return None
