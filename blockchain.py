import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_logs = []
        # Создаём генезис-блок
        self.new_block(proof=100, previous_hash="1")

    def new_block(self, proof, previous_hash=None):
        """
        Создаёт новый блок в цепочке.
        :param proof: доказательство работы (упрощённое)
        :param previous_hash: хеш предыдущего блока
        :return: новый блок
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'logs': self.current_logs,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_logs = []
        self.chain.append(block)
        return block

    def new_log(self, ip, event):
        """
        Добавляет новый лог в текущий список.
        :param ip: IP-адрес источника
        :param event: описание события (например, "SQL-инъекция")
        """
        log = {
            'ip': ip,
            'event': event,
            'timestamp': time()
        }
        self.current_logs.append(log)

    @staticmethod
    def hash(block):
        """
        Вычисляет хеш блока.
        :param block: словарь с данными блока
        :return: строка с SHA-256 хешем
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def last_block(self):
        """Возвращает последний блок в цепочке."""
        return self.chain[-1]