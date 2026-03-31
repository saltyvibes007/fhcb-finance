import './globals.css'
import type { Metadata } from 'next'
import Header from '@/components/Header'

export const metadata: Metadata = {
  title: 'BloomFi - Financial Dashboard',
  description: 'AI-powered financial dashboard for community organizations',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen">
        <Header />
        {children}
      </body>
    </html>
  )
}
