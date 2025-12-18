# Apache NiFi Alerting System
The flow continuously monitors system and NiFi metrics (CPU, RAM, Threads, Disk usage, etc.), evaluates them against predefined thresholds, and triggers alerts via HTTP and Email when anomalies are detected.

The alerting pipeline is built around the following logical stages:

- **Flow Triggering**
- **Metrics Collection** 
- **Metrics Extraction**
- **Threshold Evaluation** 
- **Routing** 
- **Notification**
  
## Main Alerting Process Group
![Main Alerting Process Group](../images/Principale_AlertingFlow.png)
## Metrics System Alerting – Sub Process Group
![Metrics Alerting – Sub Process Group](../images/AlertingFlow_System.png)
## Metrics Alerting System Flow 
![Metrics System Alerting Flow p1](../images/AlertinSystem_p1.png)
![Metrics System Alerting Flow p2](../images/AlertingSystem_p2.png)
## Processors Description
- **GenerateFlowFile**
  
Acts as a scheduler to trigger the monitoring flow periodically.
![GenerateFlowFile](../images/generatF.png)
- **InvokeHTTP**
  
Metrics Collection
![InvokeHTTP](../images/inv_http_sys.png)

Calls a monitoring endpoint (NiFi API / system metrics API).

GET /nifi-api/system-diagnostics

![system metrics API](../images/API_SYS.png)
- **EvaluateJsonPath**
  
Extracts metrics from the JSON response.
![EvaluateJsonPath](../images/Json_sys.png)
- **UpdateAttribute**
  
Normalizes metrics and defines the necessary attributes, such as metric thresholds for alerts.
![UpdateAttribute](../images/Updat_atri.png)
- **RouteOnAttribute**
  
Alert Detection : Compares metrics against thresholds and routes FlowFiles.
![RouteOnAttribute](../images/onrot.png)
- **ReplaceText**
  
Alert Message Formatting : Builds a clean and readable alert message.
![ReplaceText](../images/replace_text.png)
## Notification Processors
- **PutEmail**
  
Sends alert notifications via email.
![PutEmail](../images/PUTEMAIL_CONFIG.png)
- **InvokeHTTP (Webhook / API)**
  
Sends alerts to external systems (Slack, Teams, Monitoring API, etc.).
![InvokeHTTP (Webhook / API)](../images/inv_http_url.png)

## Queue Alerting – Sub Process Group 
![Queue Alerting – Sub Process Group](../images/Alerting_Que_ByFlow.png)
## Queue Alerting Flow
![Queue Alerting Flow](../images/Alerting_Que.png)
## Processors Description
In this sub-process group, we use the same processors; the only difference is the API endpoint used to extract different NiFi metrics.
- **InvokeHTTP**
  
Metrics Collection
![InvokeHTTP2](../images/inv_http_que.png)

Calls a monitoring endpoint (NiFi API / system metrics API).

GET /nifi-api/flow/status

![system metrics API2](../images/API_QU.png)
- **EvaluateJsonPath**
  
Extracts metrics from the JSON response.

![EvaluateJsonPath2](../images/json_que.png)

## Results
## Email Notification
- **CPU metric alert**
![CPU metric alert](../images/cpu_Em.png)
- **Threads metric alert**
![threads metric alert](../images/threads_Em.png)
- **Que FlowFile metric alert**
![Que FlowFile metric alert](../images/que_flofil_Em.png)

## Webhook / API Notification
- **CPU metric alert**
![CPU metric alert1](../images/cpu_urll.png)
- **Threads metric alert**
![Threads metric alert1](../images/THRED_urll.png)
- **Que FlowFile metric alert**
![Que FlowFile metric alert1](../images/quefil_urll.png)

## Requirements
- Apache NiFi 1.22
- Access to metrics endpoint
- SMTP server (for email alerts)
- Optional webhook endpoint



