# 🎯 Quick Commands Reference

## 🚀 Starting the Server

### Method 1: Simple Start (Recommended)
```bash
source venv/bin/activate
python start.py
```
✅ **Easiest** - Just activate and run!

### Method 2: With Verification
```bash
./run.sh
```
✅ **Safest** - Checks everything first

### Method 3: Direct Uvicorn
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```
✅ **Developer Mode** - Auto-reload on changes

### Method 4: Production Mode
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
✅ **Production** - No auto-reload

---

## 🔧 Setup Commands

### First Time Setup
```bash
./setup_env.sh
```

### Verify Installation
```bash
source venv/bin/activate
python verify_setup.py
```

### Reinstall Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Testing Commands

### Test Root Endpoint
```bash
curl http://localhost:8000/
```

### Upload a PDF
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_document.pdf"
```

### Test Imports
```bash
source venv/bin/activate
python test_imports.py
```

---

## 🗑️ Cleanup Commands

### Remove Virtual Environment
```bash
rm -rf venv
```

### Remove ChromaDB Data
```bash
rm -rf chroma_db
```

### Fresh Start
```bash
rm -rf venv chroma_db
./setup_env.sh
```

---

## 📊 Useful Commands

### Check Python Version
```bash
python --version
```

### List Installed Packages
```bash
source venv/bin/activate
pip list
```

### Check ChromaDB Status
```bash
ls -la chroma_db/
```

### View Server Logs
Just watch the terminal where the server is running!

---

## 🌐 Access Points

Once server is running:

- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **MCP Endpoint**: http://localhost:8000/mcp

---

## ⚡ Quick Workflow

### Complete Workflow
```bash
# 1. Setup (first time only)
./setup_env.sh

# 2. Start server
source venv/bin/activate
python start.py

# 3. In another terminal, upload a PDF
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"

# 4. Open browser and test
open http://localhost:8000/docs
```

---

## 🛑 Stop Server

Press **Ctrl+C** in the terminal where the server is running

---

## 🆘 If Something Goes Wrong

### Import Errors
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Module Not Found
```bash
# Use one of these:
python start.py                    # From project root
uvicorn app.main:app --reload      # From project root
```

### Port Already in Use
```bash
# Change port in command:
uvicorn app.main:app --port 8001 --reload
```

### ChromaDB Issues
```bash
rm -rf chroma_db
python start.py
```

---

## 💡 Pro Tips

1. **Always activate venv first**: `source venv/bin/activate`
2. **Use start.py for simplicity**: `python start.py`
3. **Use --reload for development**: Auto-restarts on code changes
4. **Check verify_setup.py if issues**: Diagnoses problems
5. **Keep terminal open**: See real-time logs

---

## 📝 Remember

- ✅ Run from project root: `/Users/narenratnam/Desktop/RAG and MCP Project`
- ✅ Activate venv first: `source venv/bin/activate`
- ✅ Use `start.py` for easiest startup
- ✅ Check docs at: http://localhost:8000/docs
