'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Upload, FileSearch, Wand2, Briefcase, Users, Shield, LogOut } from 'lucide-react'
import { useSession, signOut } from 'next-auth/react'
import { API_BASE_URL } from '../lib/api'

const navigation = [
  { name: 'Candidate Upload', href: '/', icon: Upload },
  { name: 'Candidate Search', href: '/search', icon: Users },
  { name: 'Resume Screener', href: '/screener', icon: FileSearch },
  { name: 'AI Resume Tailor', href: '/tailor', icon: Wand2 },
]

export default function Sidebar() {
  const pathname = usePathname()
  const { data: session } = useSession()

  const handleSignOut = () => {
    signOut({ callbackUrl: '/login' })
  }

  return (
    <div className="w-64 bg-gradient-to-b from-primary-800 to-primary-900 text-white shadow-2xl flex flex-col">
      {/* Logo/Brand */}
      <div className="p-6 border-b border-primary-700">
        <div className="flex items-center space-x-3">
          <div className="bg-white rounded-lg p-2">
            <Briefcase className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-xl font-bold">TalentHub</h1>
            <p className="text-xs text-primary-200">Recruiting Dashboard</p>
          </div>
        </div>
      </div>

      {/* User Info */}
      {session?.user && (
        <div className="p-4 border-b border-primary-700 bg-primary-800/50">
          <div className="flex items-center space-x-3">
            {session.user.image && (
              <img
                src={session.user.image}
                alt={session.user.name}
                className="h-10 w-10 rounded-full border-2 border-primary-300"
              />
            )}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-white truncate">
                {session.user.name}
              </p>
              <p className="text-xs text-primary-200 truncate">
                {session.user.email}
              </p>
              {session.user.isAdmin && (
                <span className="inline-flex items-center mt-1 px-2 py-0.5 rounded text-xs font-medium bg-yellow-400 text-yellow-900">
                  <Shield className="h-3 w-3 mr-1" />
                  Admin
                </span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          const Icon = item.icon

          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-white text-primary-900 shadow-md'
                  : 'text-primary-100 hover:bg-primary-700 hover:text-white'
              }`}
            >
              <Icon className="h-5 w-5" />
              <span className="font-medium">{item.name}</span>
            </Link>
          )
        })}

        {/* Admin Panel Link - Only for admins */}
        {session?.user?.isAdmin && (
          <>
            <div className="my-4 border-t border-primary-700"></div>
            <Link
              href="/admin"
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                pathname === '/admin'
                  ? 'bg-yellow-400 text-yellow-900 shadow-md'
                  : 'text-yellow-300 hover:bg-yellow-500/20 hover:text-yellow-200 border-2 border-yellow-400/50'
              }`}
            >
              <Shield className="h-5 w-5" />
              <span className="font-bold">Admin Panel</span>
            </Link>
          </>
        )}
      </nav>

      {/* Sign Out Button */}
      <div className="p-4 border-t border-primary-700">
        <button
          onClick={handleSignOut}
          className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-primary-100 hover:bg-red-600 hover:text-white transition-all"
        >
          <LogOut className="h-5 w-5" />
          <span className="font-medium">Sign Out</span>
        </button>
      </div>

      {/* Footer Info */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-primary-700">
        <div className="text-xs text-primary-200">
          <p className="font-semibold mb-1">API Status</p>
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="truncate">
              {API_BASE_URL.replace('http://', '').replace('https://', '')}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
