from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

def get_simulated_ram_data():
    
    # Simulation l'utilisation de la RAM en %.
    ram_usage = round(random.uniform(30.0, 85.0), 2)

    data = {
        'timestamp_utc': datetime.datetime.utcnow().isoformat(),
        'metrics': {
            'ram_percent': ram_usage
        },
        'source': 'api_simulator_v1_ram_only'
    }
    return data

@app.route('/metrics', methods=['GET'])
def get_metrics():
    #Le point d'entrée de l'API qui retourne  la RAM .
    print("API simulée : Requête reçue/ Envoi de la métrique RAM.")
    simulated_data = get_simulated_ram_data()
    return jsonify(simulated_data)

if __name__ == '__main__':
    print("Démarrage du simulateur d'API (RAM ) sur http://127.0.0.1:5000/metrics")
    app.run(debug=True, port=5000)