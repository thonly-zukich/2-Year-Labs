import asyncio
import random

# Функція-імітація обробки замовлень із затримкою (дебаунс)
async def process_item(item, min_time=2.0):
    processing_time = random.uniform(0.5, 3)  # Час виконання від 0.5 до 3 секунд
    await asyncio.sleep(processing_time)
    elapsed_time = processing_time

    # Додатковий час очікування, якщо завдання виконується швидше мінімального часу
    if elapsed_time < min_time:
        await asyncio.sleep(min_time - elapsed_time)

    if random.random() < 0.1:  # 10% шанс на помилку
        raise Exception(f"Елемент {item} не вдалося обробити.")
    return f"Елемент {item} оброблено за {max(processing_time, min_time):.2f} секунд."

# Тестова функція для демонстрації
async def test_process_item():
    items = [f"Елемент {i}" for i in range(5)]
    for item in items:
        try:
            result = await process_item(item)
            print(result)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(test_process_item())
