from flask import Flask, request, jsonify
from blockchain.blockchain import Blockchain
from blockchain.blockchain import analyze_logs
from blockchain.notifier import notify_admin
#lala

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/log', methods=['POST'])
def add_log():
    """
    Принимает лог через POST-запрос и добавляет его в блокчейн.
    Ожидаемый JSON: {"ip": "192.168.1.10", "event": "SQL-инъекция"}
    """
    data = request.get_json()
    ip = data.get("ip")
    event = data.get("event")
    
    if not ip or not event:
        return jsonify({"message": "Неверный формат запроса"}), 400
    
    blockchain.new_log(ip, event)
    return jsonify({"message": "Лог добавлен"}), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    """Возвращает всю цепочку блоков."""
    return jsonify(blockchain.chain), 200

@app.route('/analyze', methods=['GET'])
def analyze():
    """
    Анализирует логи и возвращает аномалии.
    Также вызывает уведомление администратора.
    """
    anomalies = analyze_logs(blockchain.chain, threshold=5, time_window=60)
    notify_admin(anomalies)
    return jsonify({"anomalies": anomalies}), 200

@app.route('/new_block', methods=['POST'])
def create_new_block():
    """Создаёт новый блок из накопленных логов."""
    last_block = blockchain.last_block()
    proof = 200  # Упрощённое доказательство
    block = blockchain.new_block(proof=proof, previous_hash=blockchain.hash(last_block))
    return jsonify({"message": "Новый блок создан", "block": block}), 201




@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Attack Logging System</h1>
    <p>Welcome! This is a blockchain-based system for recording and analyzing attacks.</p>
    <p>Available routes:</p>
    <ul>
        <li><b>POST /log</b> - add a log</li>
        <li><b>GET /chain</b> - view the chain</li>
        <li><b>GET /analyze</b> - analyze anomalies</li>
        <li><b>POST /new_block</b> - create a new block</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
