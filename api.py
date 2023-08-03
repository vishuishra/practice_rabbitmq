# app.py
from fastapi import FastAPI, HTTPException, Request
import aio_pika


app = FastAPI()

async def publish_to_queue(queue_name: str, message: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    await channel.declare_queue(queue_name)
    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=queue_name  # Use the queue_name as the routing_key
    )
    await connection.close()

async def get_processed_message_from_queue(queue_name: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    message = await queue.get()
    if message:
        processed_message = message.body.decode()
        await message.ack()  # Acknowledge the message to remove it from the queue
    else:
        processed_message = None
    await connection.close()
    return processed_message

# @app.post("/process_message/")
# async def process_message(message: str):
#     try:
#         await publish_to_queue("input_queue", message)
#         return {"message": "Message sent for processing"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/processed_message/")
# async def get_processed_message():
#     processed_message = await get_processed_message_from_queue("output_queue")
#     if processed_message:
#         return {"processed_message": processed_message}
#     else:
#         return {"message": "No processed messages available"}


@app.post("/messages/")
@app.get("/messages/")
async def get_and_display_messages(request:Request):
    if request.method == 'POST':
        try:
            request_body  = await request.json()
            message = request_body.get('message')
            await publish_to_queue("input_queue", message)
            return {"message": "Message sent for processing"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    elif request.method == 'GET':
        processed_message = await get_processed_message_from_queue("output_queue")
        if processed_message:
            return {"processed_message": processed_message}
        else:
            return {"message": "No processed messages available"}
