# NiFiPulse
We chose this name as we beleive it reflects the essence of our capstone project with ArkXJobInTech and DXC.
**NiFiPulse** is a lightweight on-prem monitoring and alerting solution for Apache NiFi clusters.  
It continuously tracks system and pipeline health: CPU, RAM, disk usage, file I/O, NiFi pipeline metrics, and more, then triggers alerts when thresholds are exceeded.

## Features

- 📊 **Metrics Collection** – Gather CPU, RAM, file system, and NiFi flow stats.  [nifi_flows](nifi_flows)
- 🧩 **NiFi Integration** – Connects directly with NiFi APIs to pull processor and queue metrics.  
- ⚠️ **Alerting Engine** – Send email, Slack, or webhook alerts based on user-defined thresholds.  
- 🧠 **Custom Dashboards** – Visualize health trends and performance over time.  
- 🛠️ **On-Prem Ready** – Designed for environments without external cloud dependencies.  
- 🔐 **Secure Configuration** – Credentials and endpoints are managed via `.env` files.

## Architecture
![Architecture](images/Architecture.PNG) 
#
- Flow of simulation and extraction part in depth:
#
![simulation-extraction](images/simulation-extraction.png)
## State of Art
- [State of Art FR](state_of_art/Etat_de_l_art.pdf)
- [State of Art Eng](state_of_art/State_of_art.pdf)

## Data Simulation
Nifi Registery config
- [Nifi Prometheus Registery config](simulation/nifi_prom_conf.md)

### Files:
-`docker exec -it nifi /bin/bash` + `ls -l /opt/nifi/nifi-current/data/outgoing` to list simulated data files from NiFi.
- [Similated file workflows](simulation/file_simulation.md)
- [Similated Pipeline (success/failure)](simulation/pipeline_simulation.md)

## Configuration files
- [docker set-up for Nifi and Prometheus](docker-compose.yml)
- [Prometheus job configuration file](prometheus.yml)

# For Collaborators
- run `git clone https://github.com/DXC-DP-Monitoring/NiFiPulse.git` on your local machine, on your preferred folder.
## Pull for updates
- run `git branch` to make sure you are on main , if not run `git checkout main`
- run `git pull origin main`, this will fetche updates from the remote repo (`origin`) and merges them into your local `main` branch
- To keep the history linear: `git fetch origin` + `git rebase origin\main` (no merge)

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for the full license text.

Copyright (c) 2025 Amina BOUHAMRA, Fadwa EL AMRAOUI, Nawar TOUMI, Soukaina BOUCETTA