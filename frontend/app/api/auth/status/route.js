import { NextResponse } from 'next/server'

/**
 * Lets the login page show setup help without exposing secrets.
 */
export async function GET() {
  const skipAuth = process.env.NEXT_PUBLIC_SKIP_AUTH === 'true'

  const hasGoogle =
    !!process.env.GOOGLE_CLIENT_ID &&
    process.env.GOOGLE_CLIENT_ID !== 'your_google_client_id_here'
  const hasGoogleSecret =
    !!process.env.GOOGLE_CLIENT_SECRET &&
    process.env.GOOGLE_CLIENT_SECRET !== 'your_google_client_secret_here'
  const hasNextAuthSecret =
    !!process.env.NEXTAUTH_SECRET &&
    process.env.NEXTAUTH_SECRET !== 'your_nextauth_secret_here'
  const hasNextAuthUrl = !!process.env.NEXTAUTH_URL

  const googleReady = hasGoogle && hasGoogleSecret && hasNextAuthSecret && hasNextAuthUrl

  return NextResponse.json({
    skipAuth,
    /** True when real Google OAuth + NextAuth can run */
    googleReady,
    /** @deprecated use googleReady — kept for older clients */
    oauthReady: googleReady,
    hasNextAuthUrl,
    /** Show the long "configure Google" banner only when not in skip-auth dev mode and Google is not set up */
    showGoogleSetup: !skipAuth && !googleReady,
    missing: {
      googleClientId: !hasGoogle,
      googleClientSecret: !hasGoogleSecret,
      nextAuthSecret: !hasNextAuthSecret,
      nextAuthUrl: !hasNextAuthUrl,
    },
  })
}
