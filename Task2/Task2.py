import asyncio
import random

# Базова реалізація async_map для асинхронної обробки масиву з колбеками

def async_map(data, async_function, callback):
    results = [None] * len(data)
    pending_tasks = len(data)

    def handle_result(index, error, result):
        nonlocal pending_tasks
        if error:
            results[index] = f"Помилка: {error}"
        else:
            results[index] = result
        pending_tasks -= 1
        if pending_tasks == 0:
            callback(results)

    for index, item in enumerate(data):
        async_function(item, lambda error, result, idx=index: handle_result(idx, error, result))

# Функція-імітація обробки замовлень з колбеками
async def process_order(order, callback):
    preparation_time = random.uniform(0.5, 3)  # Час виконання від 0.5 до 3 секунд
    await asyncio.sleep(preparation_time)
    if random.random() < 0.1:  # 10% шанс на помилку
        callback(f"Замовлення {order} не вдалося обробити.", None)
    else:
        callback(None, f"Замовлення {order} готове за {preparation_time:.2f} секунд.")

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

    def show_results(results):
        print("\nРезультати обробки замовлень:")
        for result in results:
            print(result)
        print("\nУсі замовлення оброблено! Смачного.")

    async_map(orders, lambda order, cb: asyncio.create_task(process_order(order, cb)), show_results)

if __name__ == "__main__":
    asyncio.run(manage_orders())
