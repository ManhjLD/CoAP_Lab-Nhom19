import argparse
import asyncio
import json
import random

from aiocoap import Code, Context, Message, resource
from aiocoap.numbers import ContentFormat


class SensorDataResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.temperature = round(random.uniform(20.0, 38.0), 1)
        self.humidity = round(random.uniform(30.0, 80.0), 1)

    async def render_get(self, request):
        payload = {
            "device_id": "sensor01",
            "temperature": self.temperature,
            "humidity": self.humidity,
        }
        return Message(
            code=Code.CONTENT,
            payload=json.dumps(payload).encode("utf-8"),
            content_format=ContentFormat.JSON,
        )

    async def update(self):
        while True:
            await asyncio.sleep(3)
            self.temperature = round(random.uniform(20.0, 38.0), 1)
            self.humidity = round(random.uniform(30.0, 80.0), 1)
            print(
                "Sensor updated: "
                f"{self.temperature:.1f} C, {self.humidity:.1f} %"
            )


async def serve(host, port):
    sensor = SensorDataResource()
    site = resource.Site()
    site.add_resource(("iot", "lab", "sensor01", "data"), sensor)
    context = await Context.create_server_context(site, bind=(host, port))
    update_task = asyncio.create_task(sensor.update())
    print(f"Sensor CoAP Server started on {host}:{port}")
    print("Resource: /iot/lab/sensor01/data")
    try:
        await asyncio.get_running_loop().create_future()
    finally:
        update_task.cancel()
        await asyncio.gather(update_task, return_exceptions=True)
        await context.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 2 sensor server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="IP address to bind; use the server's LAN IP for remote clients",
    )
    parser.add_argument("--port", type=int, default=5683)
    args = parser.parse_args()
    try:
        asyncio.run(serve(args.host, args.port))
    except KeyboardInterrupt:
        print("\nSensor server stopped.")


if __name__ == "__main__":
    main()
