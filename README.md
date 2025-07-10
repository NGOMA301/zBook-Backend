# Book Summarizer Backend

A FastAPI backend service that allows users to upload book files (PDF, TXT, etc.), extracts the text, and generates concise summaries and key points using an AI summarization service. The app supports user authentication and stores summaries per user in MongoDB.

---

## Features

- Upload and summarize book files  
- Extract key points and word counts  
- User authentication with JWT  
- Store summaries securely per user  
- Retrieve user’s previous summaries  
- File type validation and error handling  

---

## Tech Stack

- Python 3.13  
- FastAPI (async API framework)  
- MongoDB (NoSQL database)  
- Uvicorn (ASGI server)  
- AI summarization via OpenRouter API (or custom)  
- Authentication via JWT tokens  
- Bson for ObjectId handling

---

## Getting Started

### Prerequisites

- Python 3.13+ installed  
- MongoDB instance (local or cloud)  
- `pip` package manager  
- API keys/configuration for the summarization service  

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/NGOMA301/zBook-Backend.git
   cd book-summarizer-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/Scripts/activate   # Windows
   source env/bin/activate       # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env` or config file (`app/core/config.py`):

   * MongoDB connection URI
   * AI summarization API keys
   * JWT secret key
   * Allowed file extensions (pdf, txt, etc.)

### Running the Server

```bash
uvicorn app.main:app --reload
```

The server will run on `http://127.0.0.1:8000`.

---

## API Endpoints

### POST `/api/v1/summaries/`

* Upload a book file to summarize.
* Requires authentication via Bearer token.
* Request: multipart form-data with `file`.
* Response: JSON object with summary, key points, metadata.

### POST `/api/v1/summaries`

* Retrieve all summaries for the authenticated user.
* Requires authentication.
* Response: JSON array of summary objects.

---

## Project Structure

```
app/
├── api/
│   └── v1/
│       └── routes/
│           └── summarize.py         # Summarization endpoints
├── auth/
│   └── auth_handler.py               # Authentication logic
│   └── auth_routes.py                # Auth endpoints (login/register)
├── core/
│   └── config.py                    # Configurations & settings
├── db/
│   └── mongo.py                    # MongoDB client connection
├── services/
│   ├── file_reader.py               # File extraction utilities
│   └── summarizer.py                # AI summarization logic
└── main.py                         # FastAPI app startup
```

---

## Troubleshooting

* **ModuleNotFoundError: No module named 'passlib'**
  Make sure you activated the virtual environment and installed all requirements:

  ```bash
  source env/Scripts/activate
  pip install -r requirements.txt
  ```

* **MongoDB connection errors**
  Verify your MongoDB URI and network access settings.

* **Summary generation errors**
  Check your AI summarization API keys and quota limits.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.instagram.com/ngoma.301) file for details.

---

## Contact

Created by \[Your Name] - feel free to reach out via \[[ngoma@threezeroonellc.com](mailto:ngoma@threezeroonellc.com)] or open an issue.

