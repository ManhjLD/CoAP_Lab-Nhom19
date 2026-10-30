import argparse
import asyncio
import json
from datetime import datetime

from aiocoap import Code, Context, Message


def show_state(response, initial):
    if response.code != Code.CONTENT:
        raise RuntimeError(f"Unexpected CoAP response: {response.code}")
    data = json.loads(response.payload.decode("utf-8"))
    device_id = data["device_id"]
    status = data["status"]
    if status not in {"ON", "OFF"}:
        raise ValueError(f"Invalid light status: {status!r}")
    label = "Initial State" if initial else "State Updated"
    timestamp = datetime.now().astimezone().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] {label}")
    print(f"Device: {device_id}")
    print(f"Status: {status}")


async def monitor(uri):
    protocol = await Context.create_client_context()
    request = protocol.request(
        Message(code=Code.GET, uri=uri, observe=0)
    )
    try:
        response = await request.response
        show_state(response, initial=True)
        print("\nObserve registration successful. Waiting for changes...")
        async for notification in request.observation:
            show_state(notification, initial=False)
    finally:
        await protocol.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 3 CoAP Observe monitor")
    parser.add_argument("--server", default="localhost")
    parser.add_argument("--port", type=int, default=5683)
    args = parser.parse_args()
    uri = f"coap://{args.server}:{args.port}/iot/lab/light01/status"
    try:
        asyncio.run(monitor(uri))
    except KeyboardInterrupt:
        print("\nObserve monitoring stopped.")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"Invalid Observe notification: {exc}") from exc
    except Exception as exc:
        raise SystemExit(f"CoAP Observe failed: {exc}") from exc


if __name__ == "__main__":
    main()
