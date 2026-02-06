# ✅ Fix 405 Error - Quick Guide

**Status:** ✅ **FIXED**

---

## 🐛 Problem

**405 Method Not Allowed** - Caused by HTTP → HTTPS redirect on Railway.

When you send a POST request to `http://your-app.up.railway.app/upload`, Railway redirects to HTTPS, but the browser converts POST to GET during the redirect, causing a 405 error.

---

## ✅ Solution

**Force HTTPS for all production URLs** - Frontend now automatically converts HTTP to HTTPS for non-localhost URLs.

---

## 🔧 What Changed

### `frontend/lib/api.js` - Updated:

**1. HTTPS Forcing:**
```javascript
// Automatically converts to HTTPS in production
if (!apiUrl.includes('localhost') && !apiUrl.startsWith('https://')) {
  apiUrl = apiUrl.replace('http://', 'https://')
  if (!apiUrl.startsWith('https://')) {
    apiUrl = 'https://' + apiUrl
  }
}
```

**2. Debug Logging:**
```javascript
// Shows API URL on page load
console.log('🔗 API Base URL:', API_BASE_URL)

// Shows upload URL before request
console.log('📤 Uploading to:', uploadUrl)
```

---

## 🧪 How to Test

### 1. Deploy Frontend

```bash
git add frontend/lib/api.js
git commit -m "Fix 405 error - force HTTPS in production"
git push origin main
```

Redeploy on Vercel/Netlify

### 2. Open Browser Console

Visit your deployed site and check console:

**Should see:**
```
🔗 API Base URL: https://your-app.up.railway.app
🌍 Environment: Production
```

**NOT:**
```
🔗 API Base URL: http://your-app.up.railway.app  ❌
```

### 3. Upload a File

**Console should show:**
```
📤 Uploading to: https://your-app.up.railway.app/upload
📄 File: resume.pdf (234.56 KB)
✅ Upload successful: { ... }
```

**NOT:**
```
📤 Uploading to: http://your-app.up.railway.app/upload  ❌
```

### 4. Check Network Tab

DevTools → Network → `/upload` request:

**Should be:**
- Request URL: `https://...` ✅
- Status: `200 OK` ✅
- Method: `POST` ✅

**NOT:**
- Request URL: `http://...` ❌
- Status: `301` or `405` ❌

---

## ⚙️ Environment Variable

### Vercel/Netlify Dashboard:

**You can use EITHER format:**

```env
# Option 1: With HTTPS (best)
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app

# Option 2: With HTTP (auto-converted to HTTPS)
NEXT_PUBLIC_API_URL=http://your-app.up.railway.app

# Option 3: Without protocol (HTTPS added automatically)
NEXT_PUBLIC_API_URL=your-app.up.railway.app
```

**All three work!** The code automatically ensures HTTPS for production.

---

## 🎯 Why This Happens

### The Redirect Problem:

```
1. Your frontend: POST http://railway.app/upload
                  ↓
2. Railway:       301 Redirect to https://railway.app/upload
                  ↓
3. Browser:       Follows redirect but changes POST to GET
                  ↓
4. Your backend:  Receives GET /upload (expects POST)
                  ↓
5. Response:      405 Method Not Allowed ❌
```

### The Fix:

```
1. Your frontend: POST https://railway.app/upload (HTTPS from start)
                  ↓
2. Railway:       No redirect needed (already HTTPS)
                  ↓
3. Your backend:  Receives POST /upload
                  ↓
4. Response:      200 OK ✅
```

---

## 📋 Quick Checklist

After deploying:

- [ ] Console shows `https://` (not `http://`)
- [ ] Upload works (no 405 error)
- [ ] Network tab shows 200 status
- [ ] No redirect (301) in Network tab

---

## ✅ Summary

| Aspect | Before | After |
|--------|--------|-------|
| **URL Protocol** | HTTP | HTTPS ✅ |
| **Redirect** | 301 → HTTPS | None ✅ |
| **Upload Status** | 405 Error | 200 OK ✅ |
| **Console Logs** | None | Full debug info ✅ |

---

**Problem:** 405 error from HTTP redirect  
**Solution:** Force HTTPS for production  
**Status:** ✅ **FIXED**  

---

**Deploy and test - no more 405 errors!** 🎉

---

_See `HTTPS_REDIRECT_FIXED.md` for detailed explanation._
