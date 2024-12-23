import asyncio
import random

# Базова асинхронна функція async_map для обробки масиву даних з обробкою помилок

async def async_map(data, async_function, callback):
    results = [None] * len(data)
    errors = []

    async def handle_item(index, item):
        def handle_result(error, result):
            if error:
                errors.append((index, error))
            else:
                results[index] = result

        await async_function(item, handle_result)

    await asyncio.gather(*(handle_item(index, item) for index, item in enumerate(data)))
    callback(errors if errors else None, results)

# Функція-імітація обробки замовлень із випадковими затримками
async def process_order(order, callback):
    preparation_time = random.uniform(0.5, 3)  # Час виконання від 0.5 до 3 секунд
    await asyncio.sleep(preparation_time)

    if random.random() < 0.1:  # 10% шанс на помилку
        callback(f"Замовлення {order} не вдалося обробити.", None)
    else:
        callback(None, f"Замовлення {order} готове за {preparation_time:.2f} секунд.")

# Основна функція для управління замовленнями
async def manage_orders():
    print("Ласкаво просимо до системи управління замовленнями!")
    print("Введіть замовлення, які потрібно обробити.")

    # Збір замовлень від користувача
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
    def show_results(errors, results):
        if errors:
            print("\nПід час обробки сталися помилки:")
            for index, error in errors:
                print(f"Замовлення {orders[index]}: {error}")
        if results:
            print("\nРезультати обробки замовлень:")
            for index, result in enumerate(results):
                if result:
                    print(result)
        print("\nУсі замовлення оброблено! Смачного.")

    await async_map(orders, process_order, show_results)

if __name__ == "__main__":
    asyncio.run(manage_orders())
