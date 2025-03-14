import hashlib
import json
from time import time
import os

class Blockchain:
    def __init__(self, filepath="blockchain.json"):
        self.chain = []
        self.current_logs = []
        self.filepath = filepath
        # Загружаем цепочку из файла, если она есть, иначе создаём генезис-блок
        if os.path.exists(filepath):
            self.load_chain()
        else:
            self.new_block(proof=100, previous_hash="1")
            self.save_chain()

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'logs': self.current_logs,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_logs = []
        self.chain.append(block)
        self.save_chain()  # Сохраняем после каждого нового блока
        return block

    def new_log(self, ip, event):
        log = {
            'ip': ip,
            'event': event,
            'timestamp': time()
        }
        self.current_logs.append(log)

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block['previous_hash'] != self.hash(previous_block):
                print(f"Invalid hash at block {i}: expected {self.hash(previous_block)}, got {current_block['previous_hash']}")
                return False
            if current_block['index'] != previous_block['index'] + 1:
                print(f"Invalid index at block {i}: expected {previous_block['index'] + 1}, got {current_block['index']}")
                return False
        return True

    def save_chain(self):
        """Сохраняет цепочку в файл."""
        with open(self.filepath, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def load_chain(self):
        """Загружает цепочку из файла."""
        with open(self.filepath, 'r') as f:
            self.chain = json.load(f)