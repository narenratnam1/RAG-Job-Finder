import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'
import { Providers } from './providers'
import { AuthWrapper } from '../components/AuthWrapper'
import { AppShell } from '../components/AppShell'

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
            <AppShell>{children}</AppShell>
          </AuthWrapper>
          <Toaster position="top-right" />
        </Providers>
      </body>
    </html>
  )
}
