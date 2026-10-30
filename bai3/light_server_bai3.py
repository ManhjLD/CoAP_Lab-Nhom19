import argparse
import asyncio
import json

from aiocoap import Code, Context, Message, resource
from aiocoap.numbers import ContentFormat


class LightStatusResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"

    def status_payload(self):
        return json.dumps(
            {"device_id": "light01", "status": self.status}
        ).encode("utf-8")

    async def render_get(self, request):
        return Message(
            code=Code.CONTENT,
            payload=self.status_payload(),
            content_format=ContentFormat.JSON,
        )

    async def render_put(self, request):
        try:
            command_data = json.loads(request.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return Message(
                code=Code.BAD_REQUEST,
                payload=b"Payload must be valid JSON",
            )

        if not isinstance(command_data, dict):
            return Message(
                code=Code.BAD_REQUEST,
                payload=b"Payload must be a JSON object",
            )
        if command_data.get("device_id") != "light01":
            return Message(code=Code.NOT_FOUND, payload=b"Unknown device")

        command = command_data.get("command")
        if not isinstance(command, str) or command.strip().upper() not in {
            "ON",
            "OFF",
        }:
            return Message(
                code=Code.BAD_REQUEST,
                payload=b"command must be ON or OFF",
            )

        command = command.strip().upper()
        print("\nPUT request received:")
        print("Device: light01")
        print(f"Command: {command}")
        if command != self.status:
            previous_status = self.status
            self.status = command
            self.updated_state()
            print(f"Light state changed: {previous_status} -> {self.status}")
            print(f"Notify observers: {self.status}")
        else:
            print(f"Light state unchanged: {self.status}")

        return Message(
            code=Code.CHANGED,
            payload=self.status_payload(),
            content_format=ContentFormat.JSON,
        )

    async def add_observation(self, request, serverobservation):
        print("\nNew Observe registration received")
        await super().add_observation(request, serverobservation)


async def serve(host, port):
    light = LightStatusResource()
    site = resource.Site()
    site.add_resource(("iot", "lab", "light01", "status"), light)
    context = await Context.create_server_context(site, bind=(host, port))
    print(f"CoAP Smart Light Server started on {host}:{port}")
    print("Resource: /iot/lab/light01/status")
    try:
        await asyncio.get_running_loop().create_future()
    finally:
        await context.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 3 smart light server")
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
        print("\nSmart light server stopped.")


if __name__ == "__main__":
    main()
