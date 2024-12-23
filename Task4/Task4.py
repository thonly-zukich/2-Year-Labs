import asyncio

# Асинхронний генератор для імітації великого набору даних
async def generate_large_data(size):
    for i in range(size):
        await asyncio.sleep(0.1)  # Симуляція затримки при отриманні даних
        yield f"Елемент {i + 1}"

# Основна функція для демонстрації роботи генератора
async def test_large_data():
    print("Генерація великого набору даних...")
    async for item in generate_large_data(10):
        print(item)

if __name__ == "__main__":
    asyncio.run(test_large_data())
