# FastAPI Backend - Video Game Sales API
![homepage image](/static/page.png)
This is the backend service for the **Video Game Sales** project, built using **FastAPI**.

## 🚀 Features
- RESTful API with **FastAPI**
- Automatic API documentation with **Swagger** and **Redoc**
- Uses **dotenv** for environment variables
- Deployment-ready with **Vercel**

## 📂 Project Structure
```
/video-game-sales-backend
│── main.py               # FastAPI application
│── .env                  # Environment variables (ignored in Git)
│── requirements.txt      # Python dependencies
│── README.md             # Documentation
│── .gitignore            # Ignored files (e.g., .env, __pycache__)
```

## 🛠 Installation

### 1️⃣ Setup Virtual Environment (Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run FastAPI Server
```sh
uvicorn main:app --reload
```

The API will be available at:
👉 **http://localhost:8000**

## 📖 API Documentation
FastAPI automatically generates interactive API docs:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔑 Environment Variables
Create a `.env` file and define the required environment variables:
```
PG_HOST=
PG_DATABASE=
PG_USER=
PG_PASSWORD=
PG_PORT=
```

## 🚀 Deployment
To deploy on **Vercel**, set environment variables in the Vercel dashboard and use:
```sh
vercel --prod
```

## 👥 Contributors
- [Your Name](https://github.com/yourgithub)

