# Outlook Calendar Meeting Alarm App

A lightweight Flask application that reminds you of your upcoming Outlook calendar meetings.  
You can also **set custom alarm times** and **control how far ahead** to fetch meetings.

---

## ✨ Features
- Read upcoming meetings from your Outlook Calendar.
- Set a custom "ring_before" time (minutes before the meeting to get alerted).
- Control "days_ahead" (how many days ahead to check meetings).
- Simple API-based setup (no complex UI needed).
- Auto recalculates alarms if configurations are changed.
---

## 🏗️ Architecture Overview

- **Flask Backend** serves REST APIs.
- **pywin32** connects to Microsoft Outlook.
- **config.json** stores settings and meetings locally.
- **CORS** enabled to allow frontend or other apps to interact easily.

> Outlook → Read Calendar → Backend (Flask) → Expose APIs → Client usage.

---

### config.json Example

```json
{
    "ring_before": 7,
    "days_ahead": 10,
    "meetings": [
        {
            "subject": "wrrfc",
            "start": "2025-04-28T09:00:00",
            "end": "2025-04-28T09:30:00",
            "account": "JGopa@technocratsdomain.com",
            "ring_at": "2025-04-28T08:53:00",
            "id": "7d98847d98e66601d40fae1222d8a13c4ef757effe815341fe4cb6d9f2df9a0b"
        }
    ]
}
```
---

# **PART 3** (Installation and Running the App)

```md
---

## ⚙️ Installation

Make sure you have:
- Python 3.8+
- Microsoft Outlook installed
- Virtual Environment ready (already included here as `venv/`)
```

```md
## 🚀 Running the Application

Just run the batch file:
```
```bash
start_flask_app.bat
```
---

# **PART 4** (API Endpoints)

```md
---

## 🔗 API Endpoints

| Endpoint | Method | Body (JSON) | Description |
|:---------|:-------|:------------|:------------|
| `/` | GET | - | Health check API. |
| `/get_meetings` | GET | - | Fetch top 5 upcoming meetings. |
| `/set_ring_before` | POST | `{ "ring_before": 7 }` | Set minutes before meeting to alert. |
| `/set_days_ahead` | POST | `{ "days_ahead": 12 }` | Set how many days ahead to fetch meetings. |

---
```
### Example `POST` Request to Set Ring Before

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"ring_before\":5}" http://127.0.0.1:5000/set_ring_before
```
---

# **PART 5** (Project Structure and Libraries)

```md
---

## 🗂️ Project Structure

```
---

## 📚 Key Libraries Used

- **Flask** — Web server
- **flask_cors** — CORS support
- **pywin32** — Outlook interaction
- **datetime** — Date/time calculations
- **hashlib** — Meeting unique IDs (SHA-256)

---
