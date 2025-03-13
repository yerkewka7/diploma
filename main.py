from flask import Flask, request, jsonify
from blockchain import Blockchain
from log_analyzer import analyze_logs
from notifier import notify_admin
import csv
import os


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
blockchain = Blockchain(filepath="blockchain.json")

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
        <li><b>POST /upload_csv</b> - upload a CSV file with logs</li>
        <li><b>GET /validate</b> - validate the blockchain</li>
    </ul>
    """

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return "", 204

@app.route('/log', methods=['POST'])
def add_log():
    data = request.get_json()
    ip = data.get("ip")
    event = data.get("event")
    if not ip or not event:
        return jsonify({"message": "Invalid request format"}, ensure_ascii=False), 400
    blockchain.new_log(ip, event)
    return jsonify({"message": "Log added"}, ensure_ascii=False), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.chain, ensure_ascii=False), 200

@app.route('/analyze', methods=['GET'])
def analyze():
    anomalies = analyze_logs(blockchain.chain, threshold=5, time_window=60)
    notify_admin(anomalies)
    return jsonify({"anomalies": anomalies}, ensure_ascii=False), 200

@app.route('/new_block', methods=['POST'])
def create_new_block():
    last_block = blockchain.last_block()
    proof = 200
    block = blockchain.new_block(proof=proof, previous_hash=blockchain.hash(last_block))
    return jsonify({"message": "New block created", "block": block}, ensure_ascii=False), 201

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.validate_chain()
    if is_valid:
        return jsonify({"message": "Blockchain is valid"}, ensure_ascii=False), 200
    else:
        return jsonify({"message": "Blockchain is invalid"}, ensure_ascii=False), 400

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in request"}, ensure_ascii=False), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}, ensure_ascii=False), 400
    
    if file and file.filename.endswith('.csv'):
        # Читаем CSV построчно для экономии памяти
        logs_added = 0
        try:
            # Временное сохранение файла
            filepath = "temp_logs.csv"
            file.save(filepath)
            
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if 'ip' not in reader.fieldnames or 'event' not in reader.fieldnames:
                    return jsonify({"message": "CSV must contain 'ip' and 'event' columns"}, ensure_ascii=False), 400
                
                for row in reader:
                    blockchain.new_log(row['ip'], row['event'])
                    logs_added += 1
                    # Создаём новый блок каждые 1000 логов (настраиваемо)
                    if logs_added % 1000 == 0:
                        blockchain.new_block(proof=200)
            
            # Создаём финальный блок для оставшихся логов
            if blockchain.current_logs:
                blockchain.new_block(proof=200)
            
            os.remove(filepath)  # Удаляем временный файл
            return jsonify({"message": f"Processed {logs_added} logs from CSV"}, ensure_ascii=False), 201
        
        except Exception as e:
            return jsonify({"message": f"Error processing CSV: {str(e)}"}, ensure_ascii=False), 500
    
    return jsonify({"message": "Invalid file format, CSV required"}, ensure_ascii=False), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
