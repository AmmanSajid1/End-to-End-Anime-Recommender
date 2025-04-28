# 🎌 End-to-End Hybrid Anime Recommender System

This project is a full-scale **hybrid anime recommender system** that combines **Collaborative Filtering** and **Content-Based Filtering** techniques to suggest anime titles to users based on their preferences.  
Built for real-world scalability with **TensorFlow**, **Google Cloud**, **DVC**, **Docker**, **Kubernetes**, **Flask**, and **Comet ML** for experiment tracking.

---

## 🚀 Tech Stack

- **Modeling:** TensorFlow, Keras
- **Data Versioning:** DVC (Data Version Control)
- **Cloud:** Google Cloud Platform (GCP) - Storage Buckets, GKE
- **Deployment:** Docker, Kubernetes
- **CI/CD:** Jenkins
- **Frontend:** Flask Web Framework
- **Experiment Tracking:** Comet ML
- **Other:** Custom Logging, Exception Handling, Warmup + Exponential LR Decay Scheduler

---

## 📚 Dataset

- User preference data from **73,516 users** on **12,294 anime titles**.
- Dataset includes ratings, synopsis, and other metadata.

---

## 🏗️ Project Architecture

```bash
|-- Anime_Recommender.egg-info/    # Metadata for package
|-- artifacts/                     # DVC managed datasets and models
|-- config/                        # Config files and paths
|-- custom_jenkins/                # Jenkins custom Docker setup
|-- logs/                          # Logs for tracking pipeline runs
|-- notebooks/                     # Jupyter notebooks for EDA
|-- pipeline/                      # Training and prediction pipelines
|-- src/                           # Core source code (models, processing, logging)
|-- static/                        # Static files (images)
|-- templates/                     # Flask templates (HTML)
|-- utils/                         # Utility functions
|-- application.py                 # Flask app
|-- deployment.yaml                # Kubernetes deployment file
|-- Dockerfile                     # Docker container definition
|-- Jenkinsfile                    # Jenkins CI/CD pipeline
|-- requirements.txt               # Project dependencies
|-- setup.py                       # Setup script
|-- tester.py                      # Quick testing script
|-- README.md                      # Project documentation
```

---

## 🧠 Model Overview

The hybrid model leverages:

- **Collaborative Filtering** with Embeddings:
  ```python
  user_embedding = Embedding(input_dim=n_users, output_dim=embedding_size)(user_input)
  anime_embedding = Embedding(input_dim=n_anime, output_dim=embedding_size)(anime_input)
  dot_product = Dot(axes=2, normalize=True)([user_embedding, anime_embedding])
  ```

- **Content-Based Filtering:** Uses cosine similarity between anime synopsis and features.

- **Training Strategies:**
  - **Custom Learning Rate Scheduler:** Warm-up followed by Exponential Decay.
  - **Callbacks:** Early Stopping, ModelCheckpoint.
  - **Experiment Tracking:** Automatic logging of metrics and parameters to **Comet ML**.

- **Deployment:** Model artifacts tracked with **DVC** and pulled automatically during CI/CD.

---

## 🛠️ Features

- ✅ **Hybrid Recommender:** Combines user preferences and content similarity.
- ✅ **End-to-End MLOps:** Data versioning, model building, containerization, deployment.
- ✅ **Fully Automated Training and Deployment Pipelines:** Managed with Jenkins.
- ✅ **Cloud-Native:** Storage, computation, and orchestration handled via GCP.
- ✅ **Experiment Management:** Comet ML integration for visualizing experiments.
- ✅ **Custom Logging & Exception Handling:** Robust monitoring and debugging support.
- ✅ **Lightweight Frontend:** Flask app to display anime recommendations with images.

---

## 🖥️ Frontend (Flask)

A simple, responsive web interface where users can input their user ID and get real-time anime recommendations, including anime titles and their images.

---

## 🔥 How It Works

1. **Data Ingestion**  
   Load and process user ratings, anime metadata, and synopsis from GCP bucket.

2. **Model Training**  
   Train a hybrid model combining collaborative and content-based methods.

3. **DVC Data Management**  
   Version control of large datasets and models.

4. **Dockerization and CI/CD**  
   Docker builds triggered via Jenkins -> Images pushed to GCR -> Deployed on Kubernetes.

5. **Real-time Predictions**  
   Flask frontend fetches recommendations dynamically based on trained models.

---

## 🐳 Deployment Overview

- Docker builds pushed to **Google Container Registry (GCR)**.
- Kubernetes deployment on **Google Kubernetes Engine (GKE)**.
- CI/CD handled via **Jenkins Pipelines**.
- Data pulled and managed via **DVC** automatically in pipelines.

---

## 📝 Setup Instructions

```bash
# Clone the repository
git clone https://github.com/AmmanSajid1/End-to-End-Anime-Recommender.git
cd End-to-End-Anime-Recommender

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model (ensure data is pulled via DVC)
python -m pipeline.training_pipeline

# Launch the Flask app
python application.py
```

---

## 📈 Results

- Achieved strong validation performance through careful hyperparameter tuning.
- Highly personalized and diverse anime recommendations.
- Seamless user experience from model training to Kubernetes deployment.

---

## 🏆 Highlights

- **End-to-End MLOps:** Not just modeling — full production-level delivery.
- **Hybrid Recommendation:** Balances personalization and content diversity.
- **Cloud-Native & Scalable:** Designed to scale for real-world use cases.

---

## ✨ Future Enhancements

- Fine-tune embeddings with advanced architectures (e.g., attention mechanisms).
- Implement streaming data support for real-time retraining.
- UI improvements to support multiple recommendations at once.
- More extensive hyperparameter optimization using Comet ML sweeps.

---

# 📬 Contact

Feel free to connect with me!  
**Email:** ammansajid1@gmail.com  
**LinkedIn:** [Amman Sajid](https://www.linkedin.com/in/amman-sajid-47bb481ba/)  

---
