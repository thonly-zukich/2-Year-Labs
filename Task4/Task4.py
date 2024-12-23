import asyncio
import random

# Клас для управління скасуванням завдань
class AbortController:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def is_cancelled(self):
        return self.cancelled

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

# Завдання 4: Обробка великих наборів даних за допомогою потоків (AsyncIterator)
async def async_stream_map(data_stream, async_function, abort_controller):
    results = []
    errors = []

    async for item in data_stream:
        if abort_controller.is_cancelled():
            errors.append((item, "Завдання скасовано."))
            continue
        try:
            result = await async_function(item)
            results.append(result)
        except Exception as e:
            errors.append((item, str(e)))

    return errors, results

# Тестова функція для демонстрації
async def test_stream_map():
    async def mock_stream():
        for i in range(5):
            yield f"Елемент {i + 1}"
            await asyncio.sleep(0.1)

    abort_controller = AbortController()
    errors, results = await async_stream_map(mock_stream(), process_item, abort_controller)
    print("Результати:", results)
    print("Помилки:", errors)

if __name__ == "__main__":
    asyncio.run(test_stream_map())
