import argparse
import asyncio
from datetime import datetime

from aiocoap import Code, Context, Message, resource


class MessageResource(resource.Resource):
    async def render_get(self, request):
        print(f"\nGET request received: /iot/lab/message")
        return Message(code=Code.CONTENT, payload=b"Xin chao tu CoAP Server")

    async def render_post(self, request):
        payload = request.payload.decode("utf-8", errors="replace")
        print("\nPOST request received:")
        print(f"Payload: {payload}")
        print(f"Time: {datetime.now().astimezone().strftime('%H:%M:%S')}")
        return Message(
            code=Code.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8"),
        )


async def serve(host, port):
    site = resource.Site()
    site.add_resource(("iot", "lab", "message"), MessageResource())
    context = await Context.create_server_context(site, bind=(host, port))
    print(f"CoAP Server started on {host}:{port}")
    try:
        await asyncio.get_running_loop().create_future()
    finally:
        await context.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 1 CoAP message server")
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
        print("\nCoAP Server stopped.")


if __name__ == "__main__":
    main()
