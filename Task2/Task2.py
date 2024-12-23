import asyncio
import random

# Перехід на Task 2: async_map переписано для використання async-await

async def async_map(data, async_function):
    results = []
    errors = []

    async def handle_item(item):
        try:
            result = await async_function(item)
            results.append(result)
        except Exception as e:
            errors.append((item, str(e)))

    await asyncio.gather(*(handle_item(item) for item in data))
    return errors, results

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

# Функція для взаємодії з користувачем
async def manage_orders():
    print("Ласкаво просимо до системи управління замовленнями!")
    print("Введіть замовлення, які потрібно обробити.")

    orders = []
    while True:
        order = input("Введіть замовлення (або 'готово' для завершення): ")
        if order.lower() == 'готово':
            break
        orders.append(order)

    if not orders:
        print("Замовлення не додані. Вихід.")
        return

    print("\nОбробляємо замовлення... Зачекайте.")

    # Використання async_map для обробки замовлень
    errors, results = await async_map(orders, lambda order: process_order(order, min_time=2.0))

    # Відображення результатів
    if errors:
        print("\nПід час обробки сталися помилки:")
        for item, error in errors:
            print(f"Замовлення {item}: {error}")
    if results:
        print("\nРезультати обробки замовлень:")
        for result in results:
            print(result)
    print("\nУсі замовлення оброблено! Смачного.")

if __name__ == "__main__":
    asyncio.run(manage_orders())
