import asyncio
import random
import time

# Реалізація async_map для async-await
async def async_map(data, async_function):
    results = []
    errors = []

    async def handle_item(item):
        try:
            result = await async_function(item)
            results.append(result)
        except Exception as e:
            errors.append((item, str(e)))

    start_time = time.time()
    await asyncio.gather(*(handle_item(item) for item in data))
    end_time = time.time()
    print(f"Час виконання async_map: {end_time - start_time:.2f} секунд")
    return errors, results

# Реалізація promise_map із підтримкою контролю паралелізму
async def promise_map(data, async_function, max_parallel=None):
    semaphore = asyncio.Semaphore(max_parallel) if max_parallel else None

    async def handle_item(item):
        async with semaphore or asyncio.dummy_semaphore():
            return await async_function(item)

    tasks = [handle_item(item) for item in data]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Функція-імітація обробки замовлень з дебаунсом
async def process_order(order, min_time=2.0):
    preparation_time = random.uniform(0.5, 3)  # Час виконання від 0.5 до 3 секунд
    await asyncio.sleep(preparation_time)
    elapsed_time = preparation_time

    # Додатковий час очікування, якщо завдання виконується швидше мінімального часу
    if elapsed_time < min_time:
        await asyncio.sleep(min_time - elapsed_time)

    if random.random() < 0.1:  # 10% шанс на помилку
        raise Exception(f"Замовлення {order} не вдалося обробити.")
    return f"Замовлення {order} готове за {max(preparation_time, min_time):.2f} секунд."

# Використання async_map для async-await
async def manage_orders_with_async_map():
    orders = ["Замовлення 1", "Замовлення 2", "Замовлення 3"]

    print("\nОбробляємо замовлення з async_map...")
    errors, results = await async_map(orders, lambda order: process_order(order, min_time=2.0))

    if errors:
        print("\nПід час обробки сталися помилки:")
        for item, error in errors:
            print(f"{item}: {error}")

    if results:
        print("\nРезультати обробки замовлень:")
        for result in results:
            print(result)

# Використання promise_map для Promise-based підходу
async def manage_orders_with_promises():
    orders = ["Замовлення 1", "Замовлення 2", "Замовлення 3"]

    print("\nОбробляємо замовлення з обмеженням паралелізму (max 2)...")
    results = await promise_map(
        orders, lambda order: process_order(order, min_time=2.0), max_parallel=2
    )

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"{orders[i]}: Помилка: {result}")
        else:
            print(result)

# Головна функція для запуску прикладів
async def main():
    print("Async-await приклад:")
    await manage_orders_with_async_map()

    print("\nPromise-based приклад:")
    await manage_orders_with_promises()

if __name__ == "__main__":
    asyncio.run(main())
