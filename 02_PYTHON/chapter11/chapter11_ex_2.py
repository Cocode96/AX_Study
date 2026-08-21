import asyncio, time

async def send_notification(customer, seconds):
    print("문자를 발송합니다.")
    await asyncio.sleep(seconds)
    print("문자가 전송되었습니다.")

async def main():
    start = time.perf_counter()

    await asyncio.gather(
        send_notification("A", 1),
        send_notification("B", 3),
        send_notification("C", 2)
    )

    end = time.perf_counter() - start

    print(f"{end:.2f}")

asyncio.run(main())