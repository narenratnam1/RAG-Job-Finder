import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'

// Super Admin email addresses - only these users get admin access
const ADMIN_EMAILS = [
  'narenratnam1@gmail.com',     // Replace with your actual email
  'upratnam@gmail.com',     // Replace with your dad's email
]

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      // Add custom properties to the session
      if (session?.user) {
        // Check if user is a super admin
        session.user.isAdmin = ADMIN_EMAILS.includes(session.user.email)
        
        // Add user ID from token
        session.user.id = token.sub
        
        // Log admin status for debugging
        if (session.user.isAdmin) {
          console.log('🔑 Admin user logged in:', session.user.email)
        } else {
          console.log('👤 Regular user logged in:', session.user.email)
        }
      }
      return session
    },
    async jwt({ token, user, account }) {
      // Add user info to JWT token
      if (user) {
        token.id = user.id
        token.email = user.email
      }
      return token
    },
  },
  pages: {
    signIn: '/login', // Custom sign-in page
    error: '/login', // Error page redirects to login
  },
  session: {
    strategy: 'jwt',
  },
  secret: process.env.NEXTAUTH_SECRET,
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }
