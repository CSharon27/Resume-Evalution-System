# 🚀 HireLens Quick Start Guide

## The Problem You're Experiencing

If you see `main.css` and `main.js` showing as **(pending)** in the browser Network tab, it's because you're opening `index.html` directly by double-clicking it. Modern browsers block JavaScript execution when opening files directly (file:// protocol) for security reasons.

## ✅ SOLUTION: Use HTTP Server for Frontend

You **MUST** serve the frontend through an HTTP server for JavaScript to work properly.

---

## 📋 Step-by-Step Instructions

### **Step 1: Start the Backend**

Open **Terminal/PowerShell #1** in the HireLens directory:

```powershell
# Activate virtual environment
venv\Scripts\activate

# Start backend
python -m uvicorn backend.main:app --reload
```

✅ You should see:
```
INFO:     Uvicorn running on http://localhost:8000
```

**Keep this terminal open!**

---

### **Step 2: Start the Frontend Server**

Open **Terminal/PowerShell #2** in the HireLens directory:

```powershell
# Run the frontend server script
start-frontend.bat
```

OR manually:

```powershell
# Change to frontend directory
cd frontend

# Start HTTP server (port 3000)
python -m http.server 3000
```

✅ You should see:
```
Serving HTTP on :: port 3000 (http://[::]:3000/) ...
```

**Keep this terminal open too!**

---

### **Step 3: Open in Browser**

Open your browser and go to:

```
http://localhost:3000
```

**🚫 DO NOT:**
- Double-click `index.html`
- Open file:/// directly in browser

**✅ DO:**
- Use `http://localhost:3000`

---

## 🧪 Testing the Upload

Once you're on `http://localhost:3000`:

1. **Check Network Tab** (F12 → Network):
   - `main.css` should show status **200** (not pending)
   - `main.js` should show status **200** (not pending)

2. **Upload a Resume**:
   - Click "Select File" button
   - Choose `mock_resume.pdf` (or any PDF/DOCX)
   - Add job description
   - Click "Evaluate Resume"

3. **Watch for Results**:
   - First evaluation takes 15-30 seconds (loading NLP models)
   - Subsequent evaluations are faster (2-5 seconds)

---


## 📊 What You Should See

### **Correct Setup:**

**Terminal 1 (Backend):**
```
INFO:     Uvicorn running on http://localhost:8000
INFO:     Application startup complete.
```

**Terminal 2 (Frontend):**
```
Serving HTTP on 0.0.0.0 port 3000 ...
```

**Browser Network Tab:**
```
Name          Status    Type        
index.html    304       document    
main.css      200       stylesheet  ✅
main.js       200       script      ✅
```

### **Incorrect Setup (Your Current Issue):**

**Browser Network Tab:**
```
Name          Status      Type        
index.html    304         document    
main.css      (pending)   stylesheet  ❌
main.js       (pending)   script      ❌
```

This means JavaScript isn't loading - you opened the file directly!

---

## 🛠️ Troubleshooting

### Problem: "Backend is not running"

**Solution:**
```powershell
# Terminal 1

venv\Scripts\activate
python -m uvicorn backend.main:app --reload
```

### Problem: "Port 3000 already in use"

**Solution:** Use a different port:
```powershell
cd frontend
python -m http.server 8080
```
Then open `http://localhost:8080`

### Problem: "main.css still showing (pending)"

**Solution:** 
1. Press `Ctrl+Shift+R` to hard refresh browser
2. Make sure you're on `http://localhost:3000` (NOT file://)
3. Check browser console (F12) for errors

### Problem: "Evaluation takes too long"

**First time:** 15-30 seconds is normal (downloading NLP models)  
**After first time:** Should be 2-5 seconds

If it times out:
- Check backend terminal for errors
- Ensure you have stable internet (first-time model download)
- Try again - models cache after first download

---

## ✅ Complete Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend server running on http://localhost:3000
- [ ] Browser open to http://localhost:3000 (not file://)
- [ ] Network tab shows main.css and main.js as **200** (not pending)
- [ ] File upload works
- [ ] Evaluation completes and shows results

---

## 🎯 Quick Commands Summary

```powershell
# Terminal 1 - Backend
venv\Scripts\activate
python -m uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend
python -m http.server 3000

# Browser
http://localhost:3000
```

---

**That's it!** The upload issue is caused by opening HTML directly. Using an HTTP server fixes it.
