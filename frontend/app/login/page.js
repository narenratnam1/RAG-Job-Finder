'use client'

import { signIn, useSession } from 'next-auth/react'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Briefcase, Lock, AlertCircle } from 'lucide-react'

const errorMessages = {
  Configuration:
    'Server configuration error. Check GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and NEXTAUTH_SECRET in frontend/.env.local',
  AccessDenied: 'Sign in was cancelled or access was denied.',
  Verification: 'Verification token expired or invalid. Try again.',
  OAuthSignin: 'Could not start Google sign-in. Check OAuth credentials and redirect URIs in Google Cloud Console.',
  OAuthCallback: 'Google callback failed. Add http://localhost:3000/api/auth/callback/google to Authorized redirect URIs.',
  OAuthCreateAccount: 'Could not create account.',
  Callback: 'Callback error. Ensure NEXTAUTH_URL matches the URL in your browser (use http://localhost:3000, not 127.0.0.1, or set NEXTAUTH_URL to match).',
  Default: 'Sign-in error. Check the browser console and .env.local.',
}

export default function LoginPage() {
  const { status } = useSession()
  const router = useRouter()
  const [authStatus, setAuthStatus] = useState(null)
  const [urlError, setUrlError] = useState(null)

  useEffect(() => {
    if (typeof window === 'undefined') return
    const params = new URLSearchParams(window.location.search)
    setUrlError(params.get('error'))
  }, [])

  useEffect(() => {
    fetch('/api/auth/status')
      .then((r) => r.json())
      .then(setAuthStatus)
      .catch(() => setAuthStatus({ oauthReady: false }))
  }, [])

  useEffect(() => {
    if (status === 'authenticated') {
      router.push('/')
    }
  }, [status, router])

  const handleGoogleSignIn = () => {
    signIn('google', { callbackUrl: '/' })
  }

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  const friendlyError = urlError ? errorMessages[urlError] || errorMessages.Default : null

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-primary-50">
      <div className="max-w-md w-full mx-4">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-600 rounded-2xl mb-4 shadow-lg">
            <Briefcase className="h-10 w-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">TalentHub</h1>
          <p className="text-gray-600">AI-Powered Recruiting Dashboard</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <div className="text-center mb-6">
            <Lock className="h-12 w-12 text-primary-600 mx-auto mb-3" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back</h2>
            <p className="text-gray-600">Sign in to access your recruiting dashboard</p>
          </div>

          {friendlyError && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-800 flex gap-2">
              <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Sign-in error ({urlError})</p>
                <p className="mt-1">{friendlyError}</p>
              </div>
            </div>
          )}

          {authStatus && !authStatus.oauthReady && (
            <div className="mb-4 p-4 rounded-lg bg-amber-50 border border-amber-200 text-sm text-amber-950">
              <p className="font-semibold mb-2">Google sign-in is not configured yet</p>
              <ol className="list-decimal pl-4 space-y-1">
                <li>Copy <code className="bg-amber-100 px-1 rounded">frontend/.env.local.example</code> to{' '}
                  <code className="bg-amber-100 px-1 rounded">.env.local</code> in the <code className="bg-amber-100 px-1 rounded">frontend</code> folder.</li>
                <li>Add OAuth credentials from{' '}
                  <a className="underline text-amber-900" href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noreferrer">
                    Google Cloud Console
                  </a>{' '}
                  (OAuth client type: Web).</li>
                <li>Under <strong>Authorized redirect URIs</strong>, add exactly:{' '}
                  <code className="bg-amber-100 px-1 rounded break-all">http://localhost:3000/api/auth/callback/google</code></li>
                <li>Set <code className="bg-amber-100 px-1 rounded">NEXTAUTH_URL=http://localhost:3000</code> and generate{' '}
                  <code className="bg-amber-100 px-1 rounded">NEXTAUTH_SECRET</code> with{' '}
                  <code className="bg-amber-100 px-1 rounded">openssl rand -base64 32</code></li>
                <li>Restart <code className="bg-amber-100 px-1 rounded">npm run dev</code>.</li>
              </ol>
              <p className="mt-3 text-xs text-amber-900/80">
                Local dev without Google: set <code className="bg-amber-100 px-1">NEXT_PUBLIC_SKIP_AUTH=true</code> in{' '}
                <code className="bg-amber-100 px-1">.env.local</code> and restart (do not use in production).
              </p>
            </div>
          )}

          <button
            type="button"
            onClick={handleGoogleSignIn}
            disabled={authStatus && !authStatus.oauthReady}
            className="w-full flex items-center justify-center gap-3 bg-white border-2 border-gray-300 hover:border-primary-500 hover:bg-primary-50 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="h-6 w-6" viewBox="0 0 24 24" aria-hidden>
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Sign in with Google
          </button>

          <div className="mt-6 text-center text-sm text-gray-500">
            <p>Secure authentication powered by Google</p>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2026 TalentHub. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}
