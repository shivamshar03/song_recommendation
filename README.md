# 🎵 Music Recommendation System using LightFM

This project is a Flask-based API that provides personalized song recommendations using the [LightFM](https://github.com/lyst/lightfm) hybrid recommendation model. It fetches user and song data from a MongoDB database, builds features, and returns a ranked list of music recommendations.

---

## 🚀 Features

- 🎧 Recommends songs to users based on features and interactions.
- 🧠 Uses **LightFM** for collaborative + content-based filtering.
- 🌐 Flask REST API with endpoint to get recommendations.
- 📊 Connects to **MongoDB Atlas** or local MongoDB.
- 🐳 Fully Dockerized and deployable via Docker Hub or Render.

---
 
## 🛠️ Tech Stack

- Python 3.10+
- Flask
- LightFM
- Pandas
- PyMongo
- MongoDB (Atlas/local)
- Docker

---

## 📂 Project Structure
```
.
├── Dockerfile
├── requirements.txt
├── main.py
├── lightfm_model.pkl
├── .env # (Not committed, use secrets)
└── README.md

```

---
 
## ⚙️ API Endpoint

### `GET /recommended_songs`

Fetches song recommendations for the currently active user.

**Response:**
```json
[
  {
    "_id": "song123",
    "name": "Blinding Lights",
    "artistName": "The Weeknd",
    "genreName": "Pop"
  },
  ...
]
```

---
 
## 📦 Environment Variables
Create a .env file in your project root:

```
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/Popil
```

---
 
## 🐳 Docker Setup
1. Build the image locally
```
docker build -t yourusername/music-recommender .
```
2. Run the container
```
docker run -p 5000:5000 --env-file .env yourusername/music-recommender
```

---
 
## ☁️ Deploying to Docker Hub
```
# Login
docker login

# Tag and Push
docker tag music-recommender yourusername/music-recommender
docker push yourusername/music-recommender
```

---
 
## ☁️ Deploying to Render
#### Push this project to GitHub
#### Go to Render
#### Create new Web Service → Select your GitHub repo
#### Set:
#### Environment: Docker
#### Add MONGO_URI as an environment variable
#### Hit Deploy

---
 
## 📊 MongoDB Collections
- users – must contain _id and user features
- songs – must contain _id, name, artistName, genreName, and other features
- These are exported to CSV and used for prediction on the fly.

---
 
## 🧠 Model File
- This app expects a trained lightfm_model.pkl to be present in the root directory.
- Train and save the model separately using your datasets.

---
 
## 👤 Author
### - Shivam Sharma
### - Founder, NexHub | AI/ML + Python Enthusiast

## 📄 License
- MIT License. Feel free to use and adapt this project.
