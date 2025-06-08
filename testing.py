import os
import asyncio
import websockets
import socket
from sys import exit

def find_free_port():
    for port in range(42000, 42100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port  # This port is free!
            except OSError:
                continue
    raise RuntimeError("No free port found in 84200–84299")
async def ping_port(host, port):
    uri = f"ws://{host}:{port}/"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send("ping")
            response = await websocket.recv()
            if response == "pong":
                print(f"✔ WebSocket server on port {port}")
                return port
    except:
        return None
async def fast_scan_ports(host="localhost", ports=range(42000, 42099)):
    tasks = [ping_port(host, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return [port for port in results if port is not None]

async def websocket_handler(websocket, path):
    print("Client connected")
    try:
        # Launch a background task to send periodic pings
        async def ping_task():
            while True:
                try:
                    await websocket.ping()
                except websockets.exceptions.ConnectionClosed:
                    print("Ping failed: connection closed")
                    break
                await asyncio.sleep(10)
        pinger = asyncio.create_task(ping_task())

        async for message in websocket:
            print(f"Received: {message}")
            if message == "ping":
                await websocket.send("pong")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected (exception): code={e.code}, reason={e.reason}")
    finally:
        pinger.cancel()
        print("Client disconnected (finally block)")
async def start_server(port):
    print(f"Starting WebSocket server on ws://localhost:{port}")
    return await websockets.serve(websocket_handler, "localhost", port, ping_interval=None)
async def receive_messages(websocket):
    try:
        async for message in websocket:
            print(f"\nServer: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by server")
async def send_messages(websocket):
    loop = asyncio.get_event_loop()
    while True:
        msg = await loop.run_in_executor(None, input, "You: ")
        if msg.lower() in {"exit", "quit"}:
            print("Disconnecting...")
            await websocket.close()
            break
        await websocket.send(msg)
async def connect_to_server(port):
    uri = f"ws://localhost:{port}/"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket server on port {port}")
            await websocket.send("ping")
            response = await websocket.recv()
            print(f"Received from server: {response}")

            # Launch send and receive concurrently
            await asyncio.gather(
                receive_messages(websocket),
                send_messages(websocket)
            )

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    i = input("would you like to start a websocket server? (y/n): ")
    if i.lower() == 'y':
        port = find_free_port()
        server = await start_server(port)
        print(f"WebSocket server started on ws://localhost:{port}")
        try:
            await asyncio.Future()  # run forever
        except KeyboardInterrupt:
            print("Server stopped")
            server.close()
            await server.wait_closed()
    else:
        print("Skipping WebSocket server setup.")
        i = input("would you like to scan for existing websocket servers? (y/n): ")
        if i.lower() == 'y':
            print("Scanning for WebSocket servers...")
            ports = await fast_scan_ports()
            if ports:
                i = input("Would you like to connect to a WebSocket server? (y/n): ")
                if i.lower() == 'y':
                    i = input(f"Enter the port number to connect to (default {ports[0]}): ")
                    await connect_to_server(int(i.strip()) if i else ports[0])
            else:
                print("No WebSocket servers found in the specified range.")
        else:
            print("Skipping WebSocket server scan.")
            exit()
asyncio.run(main())