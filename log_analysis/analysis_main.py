import pandas as pd
from collections import defaultdict
import re

LOG_FILE = "logs/webserver.log"
THRESHOLD = 5  # Если запросов больше 5 - подозрительный IP домлмю


def parse_logs(file_path):
    ip_counter = defaultdict(int)

    with open(file_path, "r") as f:
        for line in f:
            match = re.match(r"(\d+\.\d+\.\d+\.\d+)", line)  # Извлекаем IP
            if match:
                ip = match.group(1)
                ip_counter[ip] += 1

    return ip_counter


def detect_suspicious_ips(ip_counter):
    suspicious_ips = {ip: count for ip, count in ip_counter.items() if count > THRESHOLD}
    return suspicious_ips


def main():
    ip_counts = parse_logs(LOG_FILE)
    suspicious_ips = detect_suspicious_ips(ip_counts)

    print("\nАнализ логов завершён.")
    print("Всего IP-адресов обнаружено:", len(ip_counts))
    print("Подозрительные IP (более 5 запросов):")
    for ip, count in suspicious_ips.items():
        print(f"{ip} - {count} запросов")


if __name__ == "__main__":
    main()
