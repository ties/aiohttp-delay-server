import argparse
import aiohttp
import asyncio
import logging
import time

from typing import Optional

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


async def perform_request(conn: Optional[aiohttp.TCPConnector],
                          i: int,
                          sem: asyncio.Semaphore,
                          url: str):
    t0 = time.time()
    try:
        async with aiohttp.request('get', url, connector=conn) as resp:
            # Read wjhole response without buffering.
            chunk = True
            while chunk:
                chunk = await resp.content.read(1024*1024)

            delta = time.time() - t0
            LOG.info("[%d] HTTP %d after %s seconds", i, resp.status, delta)
    except aiohttp.client_exceptions.ClientConnectorError as e:
        LOG.info("[%d] %s", i, e)
    finally:
        sem.release()


async def make_requests(url, k: int, keepalive: bool) -> None:
    LOG.info("Starting %d parallel requests to '%s'", k, url)
    sem = asyncio.Semaphore(k)
    loop = asyncio.get_event_loop()

    i = 0

    # TCPConnector supports keepalive.
    connector = aiohttp.TCPConnector() if keepalive else None

    while True:
        await sem.acquire()
        loop.create_task(perform_request(connector, i, sem, url))
        i += 1


def main():
    parser = argparse.ArgumentParser("Keep n parallel connections active.")
    parser.add_argument("url", help="URL to make requests to.")
    parser.add_argument("-p", "--parallel", default=2, type=int,
                        help="Number of parallel requests (> 0)")
    parser.add_argument("-K", "--keepalive", action='store_true',
                        help="Use HTTP keepalive")

    args = parser.parse_args()
    if args.parallel <= 0:
        parser.print_help()
        sys.exit(2)

    reqs = make_requests(args.url, args.parallel, args.keepalive)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(reqs)


if __name__ == '__main__':
    main()
