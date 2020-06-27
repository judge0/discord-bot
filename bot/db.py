import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='', password='',
                                 database='', host='')
    values = await conn.fetch('''SELECT * FROM firstable''')
    print(values)
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())