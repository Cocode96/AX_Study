import asyncio, time

async def cook_ramen():
    start = time.perf_counter()

    print("라면 조리를 시작합니다.")
    await asyncio.sleep(3)
    print("라면 조리가 완료되었습니다.")

    end = time.perf_counter() - start
    print(end)

asyncio.run(cook_ramen())