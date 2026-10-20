# Automotive Firmware Security Analyzer API

A multi-threaded, asynchronous Flask HTTP server designed to extract firmware archives and scan system binaries for proprietary vendor authentication tokens.

## 🚀 Key Features
- **Parallel Analysis Engine:** Uses a concurrent thread pool to read and process deep file structures simultaneously.
- **Asynchronous Processing Pipeline:** Accepts zip file payloads immediately, issues an tracking Job UUID, and processes the computation completely in the background.
- **Thread-Safe State Management:** Employs synchronized system threading locks to guarantee clean memory state boundaries across requests.
- **Comprehensive Test Suite:** Contains unit, component-level, and fully localized live HTTP integration tests executing automatically without side-effects.

---

## 🛠️ Project Structure
```text
firmware_extractor_app/
│
├── app/
│   ├── __init__.py          # Application Factory configuration
│   ├── config.py            # Global environment controls
│   ├── routes/              # Flask API Blueprint Route Endpoints
│   │   ├── analyze.py       # POST /analyze (Handles uploads)
│   │   └── results.py       # GET /results/<job_id> (Handles polling)
│   ├── services/            # Business Logic Layer
│   │   ├── analyzer.py      # Core Regex Token Scraper
│   │   └── firmware_service.py # Async Task Coordinator
│   └── tests/               # High-Coverage Automated Test Suites
│       ├── __init__.py
│       ├── test_base.py
│       ├── test_analyzer.py
│       └── test_integration.py
│
├── tmp/                     # Sandboxed file runtime folders (Auto-managed)
├── run.py                   # Local application entrypoint
└── README.md                # System documentation
```

---

## 🏁 Getting Started

### 1. Install System Dependencies
Ensure you have Python 3.10+ installed. Install the lightweight route router handling files:
```bash
pip install flask requests
```

### 2. Running the Server Locally
To start the API gateway interface engine, run:
```bash
python run.py
```
The application will boot up at `http://127.0.0.1:8080`.

---

## 🧪 Testing and Quality Control

The repository contains an automated test matrix isolating individual service modules and full end-to-end processing loops. Run the complete engine verification suite using standard test discovery:

```bash
python -m unittest discover -s app/tests -p "test_*.py"
```

---

## 🛰️ API Specification

### 1. Queue Analysis Workload
- **Endpoint:** `POST /analyze`
- **Payload:** `multipart/form-data` containing a `file` field with a valid `.zip` archive.
- **Response Format (`202 Accepted`):**
```json
{
  "message": "firmware analysis successfully queued asynchronously",
  "job_id": "d615b516-9b25-42a1-8650-8b1cffb905df",
  "poll_url": "/results/d615b516-9b25-42a1-8650-8b1cffb905df"
}
```

### 2. Poll Status or Pull Results
- **Endpoint:** `GET /results/<job_id>`
- **Response Format (`200 OK` - Processing):**
```json
{
  "status": "processing",
  "results": {}
}
```
- **Response Format (`200 OK` - Completed):**
```json
{
  "status": "completed",
  "results": {
    "<Tkn123PATCHTkn>": 2,
    "<Tkn777XXXXXTkn>": 5
  }
}
```
