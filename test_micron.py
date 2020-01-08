from micron import micron

import asyncio
from micron.micron import Micron

mc = Micron()


@mc.consumer('pool_queue')
@mc.publisher('pool_queue')
async def send_beat(msg):
    await asyncio.sleep(1)
    print('RECIEVED %s' % msg)
    if msg == 'STOP':
        return ''
    return 'STOP'


mc.run()