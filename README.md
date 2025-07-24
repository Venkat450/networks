### Network Security Phishing Detection

An MLOps-driven microservice that detects phishing URLs in real time.  
Combines feature engineering, model training, and production-grade deployment on AWS.

---

## 🚀 Features

- **Data Ingestion & Validation**  
  - `push_data.py` streams URL records into MongoDB, enforcing schemas defined under `data_schema/`.  
  - Automated tests in `test_mongodb.py` validate collection integrity.

- **Feature Engineering & Modeling**  
  - Scripts under `Network_Data/` compute lexical, host-based, and entropy features.  
  - Trained a RandomForest classifier in `main.py`, achieving **96%** accuracy on hold-out phishing/legitimate URL sets.  
  - Model artifacts saved in `final_model/`.

- **API Service**  
  - `app.py` exposes a `/predict` endpoint for single-URL or batch predictions.  
  - Templates under `templates/` deliver a minimal Flask UI for quick demos.

- **CI/CD & Containerization**  
  - GitHub Actions workflows in `.github/workflows/` run linting, unit tests, model training, and Docker builds on every push to `main`.  
  - `Dockerfile` packages the service; images are pushed to AWS ECR.

- **Deployment & MLOps**  
  - AWS ECS Fargate orchestrates the container for elastic scaling.  
  - EC2 instances host logging, monitoring, and MLflow tracking UI.  
  - MLflow logs all experiments, parameters, metrics, and model versions.

---

## 🛠 Tech Stack

- **Languages & Frameworks:** Python, Flask, Jinja2  
- **Database:** MongoDB  
- **ML & Tracking:** scikit-learn, MLflow  
- **CI/CD:** GitHub Actions  
- **Containerization:** Docker, AWS ECR, AWS ECS Fargate  
- **Hosting:** AWS EC2 (monitoring & tracking UI)  
- **Data Validation:** JSON Schema via `data_schema/`  

---

## 📥 Getting Started

1. **Clone & Install**  
   ```bash
   git clone https://github.com/Venkat450/networks.git
   cd networks
   pip install -r requirements.txt
