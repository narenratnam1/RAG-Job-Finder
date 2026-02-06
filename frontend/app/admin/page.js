'use client'

import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Shield, Users, Database, Activity, Settings, AlertTriangle } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AdminPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Redirect non-admin users
    if (status === 'authenticated' && !session?.user?.isAdmin) {
      toast.error('Access denied. Admin privileges required.')
      router.push('/')
    }
  }, [status, session, router])

  useEffect(() => {
    // Fetch admin stats (placeholder)
    const fetchStats = async () => {
      try {
        // In the future, you can add a backend endpoint for admin stats
        // For now, just mock data
        setTimeout(() => {
          setStats({
            totalUsers: 1,
            totalResumes: 0,
            totalSearches: 0,
            pineconeVectors: 0,
          })
          setLoading(false)
        }, 500)
      } catch (error) {
        console.error('Failed to fetch stats:', error)
        setLoading(false)
      }
    }

    if (session?.user?.isAdmin) {
      fetchStats()
    }
  }, [session])

  // Show loading while checking admin status
  if (status === 'loading' || !session?.user?.isAdmin) {
    return null
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-2">
          <Shield className="h-8 w-8 text-yellow-600" />
          <h1 className="text-3xl font-bold text-gray-900">Admin Panel</h1>
        </div>
        <p className="text-gray-600">
          Welcome, <span className="font-semibold">{session.user.name}</span>. You have super admin access.
        </p>
      </div>

      {/* Admin Notice */}
      <div className="mb-8 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg">
        <div className="flex items-start">
          <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5 mr-3" />
          <div>
            <h3 className="text-sm font-semibold text-yellow-800">Super Admin Access</h3>
            <p className="text-sm text-yellow-700 mt-1">
              You are logged in as a super administrator. Handle all user data and settings with care.
            </p>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Stat Card 1 */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-primary-100 p-3 rounded-lg">
              <Users className="h-6 w-6 text-primary-600" />
            </div>
            <span className="text-sm text-gray-500">Total</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {loading ? '...' : stats?.totalUsers || 0}
          </p>
          <p className="text-sm text-gray-600 mt-1">Active Users</p>
        </div>

        {/* Stat Card 2 */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-green-100 p-3 rounded-lg">
              <Database className="h-6 w-6 text-green-600" />
            </div>
            <span className="text-sm text-gray-500">Uploaded</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {loading ? '...' : stats?.totalResumes || 0}
          </p>
          <p className="text-sm text-gray-600 mt-1">Resumes in Library</p>
        </div>

        {/* Stat Card 3 */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-blue-100 p-3 rounded-lg">
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
            <span className="text-sm text-gray-500">Total</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {loading ? '...' : stats?.totalSearches || 0}
          </p>
          <p className="text-sm text-gray-600 mt-1">Candidate Searches</p>
        </div>

        {/* Stat Card 4 */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-purple-100 p-3 rounded-lg">
              <Database className="h-6 w-6 text-purple-600" />
            </div>
            <span className="text-sm text-gray-500">Pinecone</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {loading ? '...' : stats?.pineconeVectors || 0}
          </p>
          <p className="text-sm text-gray-600 mt-1">Vector Embeddings</p>
        </div>
      </div>

      {/* Admin Actions */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Settings className="h-5 w-5 mr-2 text-gray-600" />
          System Management
        </h2>
        <p className="text-gray-600 mb-6">
          Admin-only actions and system management tools.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Action Button 1 */}
          <button
            onClick={() => toast('Feature coming soon!', { icon: '🚧' })}
            className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
          >
            <div className="flex items-center space-x-3">
              <Users className="h-5 w-5 text-gray-600" />
              <span className="font-medium text-gray-900">Manage Users</span>
            </div>
            <span className="text-sm text-gray-500">→</span>
          </button>

          {/* Action Button 2 */}
          <button
            onClick={() => toast('Feature coming soon!', { icon: '🚧' })}
            className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
          >
            <div className="flex items-center space-x-3">
              <Database className="h-5 w-5 text-gray-600" />
              <span className="font-medium text-gray-900">Vector Database</span>
            </div>
            <span className="text-sm text-gray-500">→</span>
          </button>

          {/* Action Button 3 */}
          <button
            onClick={() => toast('Feature coming soon!', { icon: '🚧' })}
            className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
          >
            <div className="flex items-center space-x-3">
              <Activity className="h-5 w-5 text-gray-600" />
              <span className="font-medium text-gray-900">Activity Logs</span>
            </div>
            <span className="text-sm text-gray-500">→</span>
          </button>

          {/* Action Button 4 */}
          <button
            onClick={() => toast('Feature coming soon!', { icon: '🚧' })}
            className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
          >
            <div className="flex items-center space-x-3">
              <Settings className="h-5 w-5 text-gray-600" />
              <span className="font-medium text-gray-900">System Settings</span>
            </div>
            <span className="text-sm text-gray-500">→</span>
          </button>
        </div>
      </div>

      {/* Admin Info */}
      <div className="bg-primary-50 rounded-xl border border-primary-200 p-6">
        <h3 className="text-lg font-semibold text-primary-900 mb-3">Admin Privileges</h3>
        <ul className="space-y-2 text-sm text-primary-700">
          <li className="flex items-start">
            <span className="mr-2">✅</span>
            <span>Access to all user data and resumes</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✅</span>
            <span>Manage vector database and embeddings</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✅</span>
            <span>View system logs and activity</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✅</span>
            <span>Configure system settings</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
