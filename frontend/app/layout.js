import { Inter } from 'next/font/google'
import './globals.css'
import Sidebar from '../components/Sidebar'
import { Toaster } from 'react-hot-toast'
import { Providers } from './providers'
import { AuthWrapper } from '../components/AuthWrapper'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'TalentHub - Recruiting Dashboard',
  description: 'AI-powered recruiting and resume management',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <AuthWrapper>
            <div className="flex h-screen bg-gray-50">
              <Sidebar />
              <main className="flex-1 overflow-y-auto">
                <div className="p-8">
                  {children}
                </div>
              </main>
            </div>
          </AuthWrapper>
          <Toaster position="top-right" />
        </Providers>
      </body>
    </html>
  )
}
