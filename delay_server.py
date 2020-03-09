import asyncio
import json
import logging
import random
import time

from aiohttp import web

# Mean delay
MEAN_DELAY = 60

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


async def delay_response(request):
    stream = web.StreamResponse()
    await stream.prepare(request)
    delay = random.expovariate(1/MEAN_DELAY)

    remote_host, remote_port = request.transport.get_extra_info('peername')
    LOG.info("delaying request from %s:%d by %s seconds.", remote_host, remote_port, delay)
    
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
    app = web.Application()
    app.router.add_get('/', delay_response)
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
