# 🛡️ CodeSentinel

> AI-powered application vulnerability scanner built with Mistral Codestral and FastAPI

**Live Demo:** [snehallaldas.github.io/CodeSentinel](https://snehallaldas.github.io/CodeSentinel)

---

## What is CodeSentinel?

CodeSentinel is a security tool that analyzes your code for vulnerabilities using AI. Paste your code or upload a file and get instant findings with severity ratings and fix suggestions — powered by Mistral's Codestral model.

---

## Features

- **AI Vulnerability Detection** — detects SQL injection, hardcoded secrets, insecure auth, missing validation, and more
- **File Upload** — upload `.py`, `.js`, `.php`, `.java`, `.ts`, `.cpp`, `.c`, `.rb` files directly
- **Auto Language Detection** — automatically detects the programming language from the file extension
- **Severity Ratings** — findings classified as Critical, High, Medium, or Low
- **Fix Suggestions** — each vulnerability includes a concrete fix recommendation
- **Scan History** — all scans saved and accessible from the sidebar
- **User Authentication** — signup, login, logout with JWT tokens
- **Retractable Sidebar** — clean ChatGPT-style interface

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI Model | Mistral Codestral |
| Database | SQLite + SQLAlchemy |
| Auth | JWT + bcrypt |
| Deployment | Render (backend) + GitHub Pages (frontend) |

---

## Project Structure

```
CodeSentinel/
├── backend/
│   ├── main.py          # FastAPI server & endpoints
│   ├── scanner.py       # Mistral AI integration
│   ├── database.py      # SQLite models & queries
│   ├── auth.py          # Password hashing & JWT tokens
│   └── requirements.txt
├── index.html           # Frontend UI
└── README.md
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/snehallaldas/CodeSentinel.git
cd CodeSentinel
```

**2. Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

**3. Add your Mistral API key**

Create a `.env` file in the backend folder:
```
MISTRAL_API_KEY=your_key_here
```

Get your API key from [console.mistral.ai](https://console.mistral.ai)

**4. Start the backend**
```bash
uvicorn main:app --reload
```

**5. Serve the frontend**
```bash
cd ..
python -m http.server 3000
```

**6. Open your browser**
```
http://localhost:3000
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/scan` | Scan pasted code |
| POST | `/scan-file` | Scan uploaded file |
| GET | `/history` | Get all scan history |
| DELETE | `/history/{id}` | Delete a scan |
| POST | `/signup` | Create an account |
| POST | `/login` | Login and get token |

---

## Screenshots

<img width="952" height="411" alt="image" src="https://github.com/user-attachments/assets/66946e1b-e3bc-426b-bfbf-9db40220e2f2" />
<img width="1900" height="821" alt="image" src="https://github.com/user-attachments/assets/5e5d9041-0e57-4433-9882-8be4257b2c17" />



---

## License

MIT — feel free to use, modify, and distribute.

---

Built by [Snehal](https://github.com/snehallaldas) as a learning project.
