import argparse
import asyncio

from aiocoap import Code, Context, Message


async def run_client(uri, student_name, student_id):
    protocol = await Context.create_client_context()
    try:
        print("Sending GET request...")
        print(f"URI: {uri}")
        response = await protocol.request(
            Message(code=Code.GET, uri=uri)
        ).response
        print("\nResponse:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")

        payload = (
            f"Xin chao tu CoAP Client - {student_id} - {student_name}"
        ).encode("utf-8")
        print("\nSending POST request...")
        print(f"Payload: {payload.decode('utf-8')}")
        response = await protocol.request(
            Message(code=Code.POST, uri=uri, payload=payload)
        ).response
        print("\nResponse:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")
    finally:
        await protocol.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Bai 1 CoAP message client")
    parser.add_argument(
        "--server",
        default="localhost",
        help="CoAP server hostname or IP address",
    )
    parser.add_argument("--port", type=int, default=5683)
    parser.add_argument("--student-name", default="Sinh Vien")
    parser.add_argument("--student-id", default="MSSV")
    args = parser.parse_args()
    uri = f"coap://{args.server}:{args.port}/iot/lab/message"
    try:
        asyncio.run(
            run_client(uri, args.student_name, args.student_id)
        )
    except KeyboardInterrupt:
        print("\nClient stopped.")
    except Exception as exc:
        raise SystemExit(f"CoAP request failed: {exc}") from exc


if __name__ == "__main__":
    main()
