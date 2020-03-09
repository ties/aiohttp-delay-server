import argparse
import aiohttp
import asyncio
import logging
import time

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


async def perform_request(session: aiohttp.ClientSession,
                          sem: asyncio.Semaphore,
                          url: str):
    t0 = time.time()
    try:
        async with session.get(url) as resp:
            # Read wjhole response without buffering.
            chunk = True
            while chunk:
                chunk = await resp.content.read(1024*1024)

            LOG.info("HTTP %d after %s seconds", resp.status, time.time() - t0)
    finally:
        sem.release()


async def make_requests(url, k) -> None:
    LOG.info("Starting %d parallel requests to '%s'", k, url)
    sem = asyncio.Semaphore(k)
    loop = asyncio.get_event_loop()

    async with aiohttp.ClientSession() as session:
        while True:
            await sem.acquire()
            loop.create_task(perform_request(session, sem, url))


def main():
    parser = argparse.ArgumentParser("Keep n parallel connections active.")
    parser.add_argument("url", help="URL to make requests to.")
    parser.add_argument("-p", "--parallel", default=2, type=int,
                        help="Number of parallel requests (> 0)")

    args = parser.parse_args()
    if args.parallel <= 0:
        parser.print_help()
        sys.exit(2)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests(args.url, args.parallel))


if __name__ == '__main__':
    main()
