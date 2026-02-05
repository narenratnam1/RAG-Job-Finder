'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Upload, FileSearch, Wand2, Briefcase } from 'lucide-react'

const navigation = [
  { name: 'Candidate Upload', href: '/', icon: Upload },
  { name: 'Resume Screener', href: '/screener', icon: FileSearch },
  { name: 'AI Resume Tailor', href: '/tailor', icon: Wand2 },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="w-64 bg-gradient-to-b from-primary-800 to-primary-900 text-white shadow-2xl">
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

      {/* Navigation */}
      <nav className="p-4 space-y-2">
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
      </nav>

      {/* Footer Info */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-primary-700">
        <div className="text-xs text-primary-200">
          <p className="font-semibold mb-1">API Status</p>
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>
            <span>Connected to localhost:8000</span>
          </div>
        </div>
      </div>
    </div>
  )
}
