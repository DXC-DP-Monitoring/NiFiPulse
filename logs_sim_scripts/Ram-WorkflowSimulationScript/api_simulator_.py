from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

def get_simulated_data():
   
    
    # Simulation de l'utilisation de la RAM 
    ram_usage = round(random.uniform(30.0, 85.0), 2)
    
    # Simulation  du statut du workflow ('RUNNING', 'SUCCESS', 'FAILED')
    workflow_status = random.choices(
        ['RUNNING', 'SUCCESS', 'FAILED'], 
        weights=[0.3, 0.6, 0.1], # Plus de poids à 'SUCCESS'
        k=1
    )[0]

    data = {
        'timestamp_utc': datetime.datetime.utcnow().isoformat(),
        'metrics': {
            'ram_percent': ram_usage,
            'last_workflow_status': workflow_status
        },
        'source': 'api_simulator_v1_ram_workflow'
    }
    return data

@app.route('/metrics', methods=['GET'])
def get_metrics():
    #Le point d'entrée de l'API qui retourne RAM et statut du workflow.
    print("API simulée :(RAM+Workflow) / Requête reçue.")
    simulated_data = get_simulated_data()
    return jsonify(simulated_data)

if __name__ == '__main__':
    print("Démarrage du simulateur d'API (RAM + Workflow) sur http://127.0.0.1:5000/metrics")
    app.run(debug=True, port=5000)