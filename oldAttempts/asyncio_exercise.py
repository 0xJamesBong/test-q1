import asyncio


async def get_text(text):
    return f"this is your text: {text}"

# await main()
# print(main())


async def foo(text):
    await asyncio.sleep(1)
    new_text = await get_text(text)

    print(f"this is another text: {new_text}")

asyncio.run(foo("Eternal father strong to save"))
