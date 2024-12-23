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

# Завдання 2: Реалізація async-await без використання колбеків із підтримкою AbortController
async def async_map(data, async_function, abort_controller):
    results = []
    errors = []

    async def handle_item(item):
        if abort_controller.is_cancelled():
            errors.append((item, "Завдання скасовано."))
            return
        try:
            result = await async_function(item)
            results.append(result)
        except Exception as e:
            errors.append((item, str(e)))

    tasks = [asyncio.create_task(handle_item(item)) for item in data]
    await asyncio.gather(*tasks)
    return errors, results

# Функція-імітація обробки замовлень із затримкою (дебаунс)
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

    abort_controller = AbortController()

    print("\nОбробляємо замовлення... Зачекайте.")

    # Створення завдання для обробки замовлень
    task = asyncio.create_task(async_map(orders, lambda order: process_order(order, min_time=2.0), abort_controller))

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

        if not abort_controller.is_cancelled():
            errors, results = await task
            if errors:
                print("\nПід час обробки сталися помилки:")
                for item, error in errors:
                    print(f"Замовлення {item}: {error}")
            if results:
                print("\nРезультати обробки замовлень:")
                for result in results:
                    print(result)
            print("\nУсі замовлення оброблено! Смачного.")
        else:
            print("\nОбробку замовлень скасовано. Немає результатів для показу.")

    except asyncio.CancelledError:
        print("\nЗавдання було скасовано через переривання.")

    print("\nДодатковий звіт про дебаунс: кожне замовлення виконувалося не менше ніж за 2 секунди.")

if __name__ == "__main__":
    asyncio.run(manage_orders())
