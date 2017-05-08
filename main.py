import asyncio

PUBLISHER_SERVER_HOST = '0.0.0.0'
PUBLISHER_SERVER_PORT = 9999

SUBSCRIBER_SERVER_HOST = '0.0.0.0'
SUBSCRIBER_SERVER_PORT = 8888

async def handle_publisher(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        data = await reader.read(100)
        if data == b'':
            writer.close()
            break
        for writer in writers:
            writer.write(data)
            await writer.drain()

writers = []
async def handle_subscriber(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    writers.append(writer)
    while True:
        data = await reader.read(100)
        if data == b'':
            writer.close()
            writers.remove(writer)
            break


def start_server():
    loop = asyncio.get_event_loop()
    publisher_server_fut = asyncio.start_server(
        handle_publisher, PUBLISHER_SERVER_HOST, PUBLISHER_SERVER_PORT, loop=loop
    )
    subscriber_server_fut = asyncio.start_server(
        handle_subscriber, SUBSCRIBER_SERVER_HOST, SUBSCRIBER_SERVER_PORT, loop=loop
    )
    subscriber_server = loop.run_until_complete(subscriber_server_fut)
    publisher_server = loop.run_until_complete(publisher_server_fut)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        subscriber_server.close()
        publisher_server.close()
        loop.run_until_complete(subscriber_server.wait_closed())
        loop.run_until_complete(publisher_server.wait_closed())
        loop.close()


if __name__ == '__main__':
    start_server()
