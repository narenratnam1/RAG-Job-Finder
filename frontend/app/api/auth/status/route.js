import { NextResponse } from 'next/server'

/**
 * Lets the login page show setup help without exposing secrets.
 */
export async function GET() {
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

  return NextResponse.json({
    oauthReady: hasGoogle && hasGoogleSecret && hasNextAuthSecret,
    hasNextAuthUrl,
    // hints only — never send actual values
    missing: {
      googleClientId: !hasGoogle,
      googleClientSecret: !hasGoogleSecret,
      nextAuthSecret: !hasNextAuthSecret,
      nextAuthUrl: !hasNextAuthUrl,
    },
  })
}
