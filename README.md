# Stress_Testing
🛠️ Stress Testing Suite
Overview 📋
Welcome to the Stress Testing Suite, a powerful Python-based tool to stress-test various system resources and analyze performance limits. Test your memory, disk, CPU, network, and MySQL database, all with automated logging, notifications, and container support!

🌟 Features
🧠 Memory Stress Test: Allocates memory and monitors usage.

💾 Disk Stress Test: Writes large files to assess disk usage.

🌐 Network Stress Test: Simulates heavy traffic to evaluate network bandwidth.

🖥️ CPU Stress Test: Executes intensive calculations to gauge CPU performance.

🛢️ MySQL Stress Test: Runs predefined SQL queries to measure database load handling.

🤖 AI-Driven Logging: ai_suggestionsfile.py sends stress logs to the ChatGPT API and generates insights, saved in suggestions.txt.

📲 WhatsApp Alerts: send_to_whatsapp.py leverages Twilio to send performance suggestions and alerts directly to WhatsApp for real-time notifications.

📦 Installation
Clone the Repository:
```
https://github.com/tamannabothra/Stress_Testing.git
cd Stress_Testing
```

Install Required Libraries 📚:

Ensure you have the following installed:
```
pip install psutil mysql-connector-python requests twilio
```
Docker Setup 🐳:

A pre-built Docker image is available on Docker Hub for quick deployment!

Pull the image:
```
docker pull tamannabothra/system-stress-app
```
Run the container:
```
docker run -d --name stress_tester tamannabothra/system-stress-app
```
🚀 Running the Script
After installing dependencies, you can start the stress tests with:

python app.py
Or, if using Docker:

docker exec -it stress_tester python app.py
🔄 Continuous Integration with Jenkins
The project includes a Jenkinsfile that automates CI/CD through ngrok and webhooks, ensuring every update is tested and deployed effortlessly!
