# app.py
from fastapi import FastAPI, HTTPException
import pika,json
from fastapi.responses import JSONResponse

app = FastAPI()

def publish_to_queue(queue_name: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message)
    connection.close()


def get_processed_message_from_queue(queue_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    connection.close()
    if method_frame:
        return body.decode()
    return None

@app.post("/publish_message/")
def publish_message(message: str):
    try:
        publish_to_queue("input_queue", message)
        return {"message": "Message published to input_queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/processed_message/")
def get_processed_message():
    processed_message = get_processed_message_from_queue("output_queue")
    if processed_message:
        # Convert the processed message to a JSON format
        # processed_message_json = json.dumps({"processed_message": processed_message})
        print(processed_message)

        # Use JSONResponse to return the JSON-formatted processed message
        return JSONResponse(content={"processed_message": processed_message})
    else:
        return {"message": "No processed messages available"}
