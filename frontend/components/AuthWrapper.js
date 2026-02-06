'use client'

import { useSession } from 'next-auth/react'
import { usePathname, useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { Briefcase } from 'lucide-react'

export function AuthWrapper({ children }) {
  const { data: session, status } = useSession()
  const pathname = usePathname()
  const router = useRouter()

  useEffect(() => {
    // Allow access to login page without authentication
    if (pathname === '/login') {
      return
    }

    // Redirect to login if not authenticated
    if (status === 'unauthenticated') {
      router.push('/login')
    }
  }, [status, pathname, router])

  // Show loading spinner while checking authentication
  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-600 rounded-2xl mb-4 shadow-lg animate-pulse">
            <Briefcase className="h-10 w-10 text-white" />
          </div>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Loading TalentHub...</p>
        </div>
      </div>
    )
  }

  // Show login page or nothing while redirecting
  if (status === 'unauthenticated' && pathname !== '/login') {
    return null
  }

  // Show children if authenticated or on login page
  return children
}
