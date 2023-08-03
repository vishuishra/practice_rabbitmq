# processor.py
import aio_pika
import asyncio

async def process_message(message: str):
    # Simulate a delay in processing (you can adjust the sleep time as needed)
    await asyncio.sleep(10)
    return f"{message} World"

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        processed_message = await process_message(body)
        connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
        channel = await connection.channel()
        await channel.declare_queue("output_queue")
        
        # Use the default exchange to publish the processed message to the output_queue
        await channel.default_exchange.publish(
            aio_pika.Message(body=processed_message.encode()),
            routing_key="output_queue"
        )
        
        await connection.close()

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    input_queue = await channel.declare_queue("input_queue")
    await input_queue.consume(on_message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    # asyncio.run(main())
