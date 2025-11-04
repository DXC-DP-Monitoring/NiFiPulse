# NiFiPulse
We chose this name as we beleive it reflects the essence of our capstone project with Ark and DXC.
**NiFiPulse** is a lightweight on-prem monitoring and alerting solution for Apache NiFi clusters.  
It continuously tracks system and pipeline health: CPU, RAM, disk usage, file I/O, NiFi pipeline metrics, and more, then triggers alerts when thresholds are exceeded.

## Features

- 📊 **Metrics Collection** – Gather CPU, RAM, file system, and NiFi flow stats.  
- 🧩 **NiFi Integration** – Connects directly with NiFi APIs to pull processor and queue metrics.  
- ⚠️ **Alerting Engine** – Send email, Slack, or webhook alerts based on user-defined thresholds.  
- 🧠 **Custom Dashboards** – Visualize health trends and performance over time.  
- 🛠️ **On-Prem Ready** – Designed for environments without external cloud dependencies.  
- 🔐 **Secure Configuration** – Credentials and endpoints are managed via `.env` files.

## Architecture

```text
+---------------------------+
|        NiFiPulse          |
|---------------------------|
| Metrics Collector (Python)|
| Alert Manager (FastAPI)   |
| Data Storage (SQLite)     |
| Dashboard (PowerBI)     |
+---------------------------+
         ↑
         |
     NiFi API
```
# For Collaborators
- run `git clone https://github.com/DXC-DP-Monitoring/NiFiPulse.git` on your local machine, on your preferred folder.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for the full license text.

Copyright (c) 2025 Amina BOUHAMRA, Fadwa EL AMRAOUI, Nawar TOUMI, Soukaina BOUCETTA