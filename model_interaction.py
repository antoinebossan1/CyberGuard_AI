import os
import json
from mistralai.models.chat_completion import ChatMessage

def pprint(obj):
    print(json.dumps(obj.dict(), indent=4))

def interact_with_model(client, fine_tuned_model, user_message):
    print(f"Interacting with model {fine_tuned_model} with message: {user_message} and API key: {os.environ.get('MISTRAL_API_KEY')}")
    
    chat_response = client.chat(
        model=fine_tuned_model,
        messages=[ChatMessage(role='user', content=user_message)]
    )
    
    pprint(chat_response)
    return chat_response

if __name__ == "__main__":
    fine_tuned_model='ft:open-mistral-7b:a8d1498d:20240624:fa14c39d' 
    user_message = 'Flow ID: 172.16.0.1-192.168.10.50-61897-80-6. Source IP: 172.16.0.1. Source Port: 61897. Destination IP: 192.168.10.50. Destination Port: 80. Protocol: 6. Timestamp: 7/7/2017 4:04. Flow Duration: 9941735. Total Fwd Packets: 4. Total Backward Packets: 0. Total Length of Fwd Packets: 24. Total Length of Bwd Packets: 0. Fwd Packet Length Max: 6. Fwd Packet Length Min: 6. Fwd Packet Length Mean: 6.0. Fwd Packet Length Std: 0.0. Bwd Packet Length Max: 0. Bwd Packet Length Min: 0. Bwd Packet Length Mean: 0.0. Bwd Packet Length Std: 0.0. Flow Bytes/s: 2.414065553. Flow Packets/s: 0.402344259. Flow IAT Mean: 3313911.667. Flow IAT Std: 5738986.983. Flow IAT Max: 9940723. Flow IAT Min: 4. Fwd IAT Total: 9941735. Fwd IAT Mean: 3313911.667. Fwd IAT Std: 5738986.983. Fwd IAT Max: 9940723. Fwd IAT Min: 4. Bwd IAT Total: 0. Bwd IAT Mean: 0.0. Bwd IAT Std: 0.0. Bwd IAT Max: 0. Bwd IAT Min: 0.'
    
    if not os.environ.get("MISTRAL_API_KEY"):
        print("Error: Please set the MISTRAL_API_KEY environment variable.")
    else:
        interact_with_model(fine_tuned_model, user_message)
