import httpx, asyncio

async def fetch_todo():
    async with httpx.AsyncClient() as client:
        url = "https://jsonplaceholder.typicode.com/todos/1"
        res = await client.get(url)
        result = res.json()
        return print(f"id : {result["id"]}, title : {result["title"]}")

async def main():
    await fetch_todo()

asyncio.run(main())