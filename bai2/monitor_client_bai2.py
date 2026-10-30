import argparse
import asyncio
import json
from datetime import datetime

from aiocoap import Code, Context, Message


async def monitor(uri, interval):
    protocol = await Context.create_client_context()
    print(f"Monitoring sensor at {uri} every {interval:g} seconds")
    try:
        while True:
            try:
                response = await protocol.request(
                    Message(code=Code.GET, uri=uri)
                ).response
                if response.code != Code.CONTENT:
                    raise RuntimeError(f"Unexpected CoAP response: {response.code}")
                data = json.loads(response.payload.decode("utf-8"))
                device_id = data["device_id"]
                temperature = float(data["temperature"])
                humidity = float(data["humidity"])

                print(
                    f"\n[{datetime.now().astimezone().strftime('%H:%M:%S')}] "
                    "Received sensor data"
                )
                print(f"\nDevice: {device_id}")
                print(f"Temperature: {temperature:.1f} C")
                print(f"Humidity: {humidity:.1f} %")
                if temperature > 35:
                    print("\nCANH BAO: Nhiet do cao")
                if humidity < 40:
                    print("\nCANH BAO: Do am thap")
                if temperature <= 35 and humidity >= 40:
                    print("\nTrang thai: Binh thuong")
                print("\n------------------------------")
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                print(f"Invalid sensor response: {exc}")
            except Exception as exc:
                print(f"Sensor request failed: {exc}")
            await asyncio.sleep(interval)
    finally:
        await protocol.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 2 sensor monitor")
    parser.add_argument("--server", default="localhost")
    parser.add_argument("--port", type=int, default=5683)
    parser.add_argument("--interval", type=float, default=3.0)
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    uri = f"coap://{args.server}:{args.port}/iot/lab/sensor01/data"
    try:
        asyncio.run(monitor(uri, args.interval))
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
