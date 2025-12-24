import asyncio
import aiohttp
import time

API_URL = "http://www.serafettinkucuktas.com.tr"
TOTAL_REQUESTS = 10000
CONCURRENCY = 10000

sem = asyncio.Semaphore(CONCURRENCY)

async def send_request(session, index):
    async with sem:
        start = time.time()
        try:
            async with session.get(API_URL, timeout=10) as resp:
                elapsed = int((time.time() - start) * 1000)
                print(f"[{index}] {resp.status} - {elapsed}ms")
        except Exception as e:
            print(f"[{index}] ERROR: {e}")

async def main():
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            asyncio.create_task(send_request(session, i))
            for i in range(TOTAL_REQUESTS)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
