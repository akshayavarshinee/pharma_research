# Quick Start - Agent Integration

## 🚀 5-Minute Setup

### 1. Add API Keys to `.env`

```env
OPENAI_API_KEY=sk-your-key-here
SERPER_API_KEY=your-key-here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Update Database

```bash
# Option A: Fresh start (deletes data)
python init_db.py

# Option B: Migrate existing data
psql -U postgres -d pharma_research -f migrations/add_query_status.sql
```

### 4. Test Agent Import

```bash
python test_agent_import.py
```

### 5. Run Application

```bash
uvicorn app.main:app --reload
```

### 6. Test in Browser

1. Go to `http://localhost:8000`
2. Create account / Login
3. Submit a query
4. Wait for processing (2-5 minutes)
5. View generated report

---

## 📁 Integration Architecture

```
Your Query Submission
        ↓
app/queries/routes.py (submit_query)
        ↓
app/services/background_tasks.py (background task)
        ↓
app/services/agent_service.py (run_pharma_research)
        ↓
agents/src/pharma_researcher/crew.py (PharmaResearcher)
        ↓
Report Generated & Saved to Database
```

---

## 🔍 Status Checking

**Via API:**

```bash
GET /api/query/status/{query_id}
```

**Response:**

```json
{
  "status": "pending" | "processing" | "completed" | "failed",
  "report_id": 123  // if completed
}
```

---

## ⚠️ Common Issues

| Issue                      | Solution                          |
| -------------------------- | --------------------------------- |
| "Agent module not found"   | Run `python test_agent_import.py` |
| "OpenAI API key not found" | Check `.env` file                 |
| Query stuck in "pending"   | Check logs, restart app           |
| "Column does not exist"    | Run migration SQL script          |

---

## 📊 File Changes Summary

| File                               | Status      | Purpose                  |
| ---------------------------------- | ----------- | ------------------------ |
| `app/services/agent_service.py`    | ✅ NEW      | Bridges FastAPI ↔ CrewAI |
| `app/services/background_tasks.py` | ✅ NEW      | Async processing         |
| `app/queries/models.py`            | ✅ MODIFIED | Added status fields      |
| `app/queries/routes.py`            | ✅ MODIFIED | Uses agents now          |
| `requirements.txt`                 | ✅ MODIFIED | Added CrewAI             |

---

**Full guide:** See [walkthrough.md](file:///C:/Users/Akshaya%20Varshinee/.gemini/antigravity/brain/f0544a4b-720f-42e1-bc92-4a341d422dcd/walkthrough.md)
