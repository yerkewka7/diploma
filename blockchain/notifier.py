def notify_admin(anomalies):
    """
    Уведомляет администратора об аномалиях.
    :param anomalies: словарь с аномальными IP и количеством запросов
    """
    if anomalies:
        print("Обнаружены аномалии:")
        for ip, count in anomalies.items():
            print(f"IP: {ip} - Запросов: {count}")
    else:
        print("Аномалий не обнаружено.")

#lala
