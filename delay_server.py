import argparse
import asyncio
import json
import logging
import math
import random
import time

from aiohttp import web

logging.basicConfig()
LOG = logging.getLogger(__name__)

LOG.setLevel(logging.INFO)


async def delay_response(mean_delay: int, max_delay: int, request):
    stream = web.StreamResponse()
    await stream.prepare(request)
    delay = random.expovariate(1/mean_delay)
    # If max_delay is set, clamp to it.
    if max_delay:
        delay = min(delay, max_delay)

    remote_host, remote_port = request.transport.get_extra_info('peername')
    LOG.info("delaying request from %s:%d by %s seconds.",
             remote_host, remote_port, round(delay, 1))

    await stream.write(json.dumps({
        'delay': delay,
        'peer': f"{remote_host}:{remote_port}"
    }).encode('utf8'))

    end = time.time() + delay
    while time.time() < end:
        await stream.write(b'.')

        time_left = end - time.time()

        await asyncio.sleep(time_left if time_left < 0.5 else 0.5)
    await stream.write_eof()
    return stream

def main():
    parser = argparse.ArgumentParser("A server that serves delays.")
    parser.add_argument("-p", "--port", default=8080, type=int,
                        help="Port to bind to.")
    parser.add_argument("--bind", default="127.0.0.1",
                        help="IP address(es) to bind to.")
    parser.add_argument("--max-delay", type=int,
                        help="Maximum delay (in seconds)")
    parser.add_argument("--mean-delay", type=int,
                        default=30,
                        help="Mean delay (in seconds)")


    args = parser.parse_args()
    if args.port <= 0:
        parser.print_help()
        sys.exit(2)

    app = web.Application()
    app.router.add_get('/', lambda request: delay_response(args.mean_delay, args.max_delay, request))
    web.run_app(app, host=args.bind, port=args.port)


if __name__ == '__main__':
    main()
