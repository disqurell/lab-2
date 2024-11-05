import random
import time
from multiprocessing import Process, Queue

# Параметры вероятностей запросов книг
book_probabilities = [0.02, 0, 0.08, 0, 0.3, 0.3, 0.3]
Rr = 75  # время в читальном зале, мин


# Этапы обслуживания
def process_request_books(num_books):
    # Имитируем различные временные затраты в зависимости от количества книг
    times = {
        "b": num_books * 0.5,  # Время объяснения запроса оператору ПК
        "z": num_books * 0.3,  # Время ввода запроса
        "f": num_books * 1.2,  # Время поиска информации
        "g": num_books * 0.2,  # Время уточнения запроса
        "h": num_books * 0.6,  # Время печати на ПК листков требований
        "s": num_books * 1.5,  # Время выбора изданий
        "v": num_books * 0.8,  # Время выдачи книг
        "r": Rr,               # Время работы в читальном зале
        "w": num_books * 0.4,  # Время возврата книг библиотекарю
    }

    # Выполняем все этапы
    for _, delay in times.items():
        time.sleep(delay / 60)  # Преобразуем минуты в секунды для моделирования


def reader(queue, total_books):
    # Случайное количество книг на основе вероятности
    num_books = random.choices(range(1, 8), weights=book_probabilities, k=1)[0]
    queue.put(num_books)  # Отправляем количество книг в очередь для подсчета
    process_request_books(num_books)  # Обрабатываем запрос читателя


def main():
    queue = Queue()
    total_books = 0
    readers = []

    # Моделируем количество читателей в течение дня
    for _ in range(100):  # например, 100 читателей за день
        p = Process(target=reader, args=(queue, total_books))
        readers.append(p)
        p.start()

    # Собираем данные о количестве выданных книг
    for p in readers:
        total_books += queue.get()
        p.join()

    print("Общее количество выданных книг за день:", total_books)


if __name__ == "__main__":
    main()
