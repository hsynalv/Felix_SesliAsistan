from flask import Flask, render_template, request, jsonify, Response
import threading
import assistant
import time
import os
import json

app = Flask(__name__)

clients = []

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/activate_assistant', methods=['POST'])
def activate_assistant():
    data = request.json
    custom_instruction = data.get('custom_instruction')
    safety_settings = data.get('safety_settings', [])
    assistant_thread = threading.Thread(target=assistant.run_assistant, args=(custom_instruction, safety_settings))
    assistant_thread.start()
    return jsonify({"message": "Assistant activated with custom instruction and safety settings"})


@app.route('/deactivate_felix', methods=['POST'])
def deactivate_felix():
    # Ek hata mesajı için log ekliyoruz
    return jsonify({"message": "Deactivate Felix"})

@app.route('/get_reminder', methods=['GET'])
def get_reminder():
    reminder_file_path = 'reminder.json'
    if os.path.exists(reminder_file_path):
        with open(reminder_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    else:
        return jsonify({"error": "Reminder file not found"}), 404


@app.route('/get_dataset', methods=['GET'])
def get_dataset():
    reminder_file_path = 'DataSet.json'
    if os.path.exists(reminder_file_path):
        with open(reminder_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    else:
        return jsonify({"error": "Reminder file not found"}), 404

@app.route('/events')
def events():
    def event_stream():
        while True:
            if clients:
                msg = "data: {}\n\n".format("Activate Felix")
                for client in clients:
                    client.put(msg)
            time.sleep(1)

    return Response(event_stream(), content_type='text/event-stream')

def notify_clients(message):
    for client in clients:
        client.put(message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
