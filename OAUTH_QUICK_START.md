# ⚡ Google OAuth - Quick Start

**Time:** 15 minutes  
**Status:** ✅ Code ready - needs credentials

---

## 🚀 3-Step Setup

### Step 1: Get Google OAuth Credentials (5 min)

#### Go to Google Cloud Console:
https://console.cloud.google.com/apis/credentials

#### Create OAuth 2.0 Client:

1. Click **"Create Credentials"** → **"OAuth client ID"**
2. **Application type:** Web application
3. **Name:** TalentHub
4. **Authorized JavaScript origins:**
   ```
   http://localhost:3000
   ```
5. **Authorized redirect URIs:**
   ```
   http://localhost:3000/api/auth/callback/google
   ```
6. Click **"Create"**
7. **Copy these values:**
   - Client ID: `123456789-xxx.apps.googleusercontent.com`
   - Client secret: `GOCSPX-xxx...`

### Step 2: Generate Secret (1 min)

```bash
openssl rand -base64 32
```

Copy the output (e.g., `Kx8j2mP9vQ3wR7tY...`)

### Step 3: Create .env.local (2 min)

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000

GOOGLE_CLIENT_ID=paste_client_id_from_step_1
GOOGLE_CLIENT_SECRET=paste_client_secret_from_step_1

NEXTAUTH_SECRET=paste_secret_from_step_2
NEXTAUTH_URL=http://localhost:3000
```

---

## 🔧 Configure Admin Emails

Edit: `frontend/app/api/auth/[...nextauth]/route.js`

**Line 6-9:**
```javascript
const ADMIN_EMAILS = [
  'your_email@gmail.com',     // ← Replace with YOUR Gmail
  'dads_email@gmail.com',     // ← Replace with dad's Gmail
]
```

---

## 🚀 Start the App

```bash
cd frontend
npm run dev
```

Go to `http://localhost:3000` → Should redirect to login!

---

## 🧪 Test

1. **Click "Sign in with Google"**
2. **Choose your Google account**
3. **Should redirect to dashboard**
4. **Check sidebar:**
   - ✅ Your profile picture
   - ✅ Your name/email
   - ✅ Admin badge (if your email is in ADMIN_EMAILS)
   - ✅ Admin Panel link (if admin)

---

## ✅ What Users See

### Regular User:
- ✅ Can sign in with Google
- ✅ Can use all features
- ❌ Cannot see admin panel
- ❌ Cannot access /admin page

### Super Admin (Your Email):
- ✅ Can sign in with Google
- ✅ Can use all features
- ✅ See yellow "Admin" badge
- ✅ See gold "Admin Panel" link
- ✅ Can access /admin page

---

## 🚨 Quick Troubleshooting

### "Sign in doesn't work"
→ Check `.env.local` exists and has all 4 variables

### "Can't see admin badge"
→ Check your email is in ADMIN_EMAILS list (exact match)

### "OAuth error"
→ Check redirect URI in Google Console matches exactly

### "NEXTAUTH_SECRET error"
→ Generate secret with `openssl rand -base64 32`

---

## 📋 Quick Checklist

- [ ] Got Google Client ID
- [ ] Got Google Client secret
- [ ] Generated NEXTAUTH_SECRET
- [ ] Created `.env.local`
- [ ] Updated ADMIN_EMAILS
- [ ] Restarted frontend
- [ ] Tested login

---

**Status:** ✅ Ready to configure!

**Time:** 15 minutes

---

_See `GOOGLE_AUTH_SETUP.md` for detailed documentation!_
