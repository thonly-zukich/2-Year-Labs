import asyncio
import random

# Базова реалізація async_map для асинхронної обробки масиву з обробкою помилок і підтримкою дебаунсу

def async_map(data, async_function, callback):
    results = [None] * len(data)
    errors = []
    pending_tasks = len(data)

    def handle_result(index, error, result):
        nonlocal pending_tasks
        if error:
            errors.append((index, error))
        else:
            results[index] = result
        pending_tasks -= 1
        if pending_tasks == 0:
            callback(errors if errors else None, results)

    for index, item in enumerate(data):
        async_function(item, lambda error, result, idx=index: handle_result(idx, error, result))

# Функція-імітація обробки замовлень з дебаунсом
async def process_order(order, callback, min_time=2.0):
    preparation_time = random.uniform(0.5, 3)  # Час виконання від 0.5 до 3 секунд
    await asyncio.sleep(preparation_time)
    elapsed_time = preparation_time

    # Додатковий час очікування, якщо завдання виконується швидше мінімального часу
    if elapsed_time < min_time:
        await asyncio.sleep(min_time - elapsed_time)

    if random.random() < 0.1:  # 10% шанс на помилку
        callback(f"Замовлення {order} не вдалося обробити.", None)
    else:
        callback(None, f"Замовлення {order} готове за {max(preparation_time, min_time):.2f} секунд.")

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

    def show_results(errors, results):
        if errors:
            print("\nПід час обробки сталися помилки:")
            for index, error in errors:
                print(f"Замовлення {orders[index]}: {error}")
        print("\nРезультати обробки замовлень:")
        for result in results:
            print(result)
        print("\nУсі замовлення оброблено! Смачного.")

    async_map(orders, lambda order, cb: asyncio.create_task(process_order(order, cb, min_time=2.0)), show_results)

if __name__ == "__main__":
    asyncio.run(manage_orders())
