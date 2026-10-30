import argparse
import asyncio
import json

from aiocoap import Code, Context, Message
from aiocoap.numbers import ContentFormat


def display_response(response):
    print(f"Response Code: {response.code}")
    print(f"Response: {response.payload.decode('utf-8', errors='replace')}")


async def control(uri):
    protocol = await Context.create_client_context()
    print(f"Connected to smart light at {uri}")
    try:
        while True:
            try:
                command = input("Nhap lenh (ON/OFF/STATUS/EXIT): ").strip().upper()
            except EOFError:
                break

            if command == "EXIT":
                break
            if command == "STATUS":
                print("\nSending GET request...")
                response = await protocol.request(
                    Message(code=Code.GET, uri=uri)
                ).response
                display_response(response)
                continue
            if command not in {"ON", "OFF"}:
                print("Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.")
                continue

            payload = json.dumps(
                {"device_id": "light01", "command": command}
            ).encode("utf-8")
            print("\nSending PUT request...")
            response = await protocol.request(
                Message(
                    code=Code.PUT,
                    uri=uri,
                    payload=payload,
                    content_format=ContentFormat.JSON,
                )
            ).response
            display_response(response)
    finally:
        await protocol.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 3 light controller")
    parser.add_argument("--server", default="localhost")
    parser.add_argument("--port", type=int, default=5683)
    args = parser.parse_args()
    uri = f"coap://{args.server}:{args.port}/iot/lab/light01/status"
    try:
        asyncio.run(control(uri))
    except KeyboardInterrupt:
        print("\nController stopped.")
    except Exception as exc:
        raise SystemExit(f"CoAP request failed: {exc}") from exc


if __name__ == "__main__":
    main()
