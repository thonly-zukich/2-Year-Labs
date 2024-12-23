import asyncio
import random

# Клас для керування подіями (реалізація EventEmitter)
class EventEmitter:
    def __init__(self):
        self._events = {}

    def on(self, event_name, callback):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    async def emit(self, event_name, *args):
        if event_name in self._events:
            for callback in self._events[event_name]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args)
                else:
                    callback(*args)

# Клас для управління скасуванням завдань
class AbortController:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def is_cancelled(self):
        return self.cancelled

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

# Асинхронний генератор для імітації великого набору даних
async def generate_large_data(size):
    for i in range(size):
        await asyncio.sleep(0.1)  # Симуляція затримки при отриманні даних
        yield f"Елемент {i + 1}"

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

# Основна функція для управління потоковою обробкою
async def manage_stream():
    print("Ласкаво просимо до системи обробки великих наборів даних!")

    size = int(input("Введіть кількість елементів у наборі даних: "))
    abort_controller = AbortController()

    print("\nПочинаємо обробку... Зачекайте.")

    data_stream = generate_large_data(size)
    task = asyncio.create_task(async_stream_map(data_stream, lambda item: process_item(item, min_time=2.0), abort_controller))

    try:
        while not task.done():
            action = input("Натисніть 'с' для скасування завдань або 'продовжити' для очікування: ").lower()
            if action == 'с':
                abort_controller.cancel()
                print("Усі завдання скасовано.")
                break
            elif action == 'продовжити':
                print("Продовжуємо обробку завдань...")
                await task
                break
            await asyncio.sleep(0.1)

        if not abort_controller.is_cancelled():
            errors, results = await task
            if errors:
                print("\nПід час обробки сталися помилки:")
                for item, error in errors:
                    print(f"Елемент {item}: {error}")
            if results:
                print("\nРезультати обробки:")
                for result in results:
                    print(result)
            print("\nУсі елементи оброблено успішно.")
        else:
            print("\nОбробку даних скасовано. Немає результатів для показу.")

    except asyncio.CancelledError:
        print("\nЗавдання було скасовано через переривання.")

if __name__ == "__main__":
    asyncio.run(manage_stream())
