'use client'

import { usePathname } from 'next/navigation'
import Sidebar from './Sidebar'

/**
 * Login page is full-screen; all other routes use sidebar + main.
 */
export function AppShell({ children }) {
  const pathname = usePathname()

  if (pathname === '/login') {
    return <>{children}</>
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <div className="p-8">{children}</div>
      </main>
    </div>
  )
}
