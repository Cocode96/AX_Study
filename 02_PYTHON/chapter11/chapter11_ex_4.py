import httpx, asyncio

todo_list = [ f"{i}번 할일" for i in range(1,6)]

async def fetch_todo_by_id(todo_nums):
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://jsonplaceholder.typicode.com/todos/{todo_nums}"
            res = await client.get(url)
            res.raise_for_status()
    except httpx.HTTPError as e:
        print(e)
        return ("수집 에러 대체 데이터","삐빅 에러")
    else:
        result = res.json()
        return result["id"], result["title"]
    
async def main():
    #fetch_todo_by_ids = [fetch_todo_by_id(i) for i in range(1,3)]
    
    result = await asyncio.gather(
        fetch_todo_by_id(1),
        fetch_todo_by_id(2),
        fetch_todo_by_id(3),
        fetch_todo_by_id(999),
        )
    print(*result)

asyncio.run(main())