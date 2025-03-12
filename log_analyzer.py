from collections import defaultdict
import time

#lala

def analyze_logs(chain, threshold=10, time_window=60):
    """
    Анализирует логи в цепочке блоков и ищет аномалии.
    :param chain: цепочка блоков
    :param threshold: порог количества запросов для определения аномалии
    :param time_window: временное окно в секундах
    :return: словарь с аномальными IP и количеством запросов
    """
    ip_counter = defaultdict(int)
    current_time = time()

    for block in chain:
        for log in block['logs']:
            if current_time - log['timestamp'] <= time_window:
                ip_counter[log['ip']] += 1

    anomalies = {ip: count for ip, count in ip_counter.items() if count > threshold}
    return anomalies
