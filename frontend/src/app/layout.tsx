import './globals.css'
import type { Metadata } from 'next'
import Header from '@/components/Header'

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://uat-corp.bloomfi.ai'

export const metadata: Metadata = {
  title: 'BloomFi - AI Financial Intelligence',
  description: 'AI-powered financial dashboard for community organizations. Upload statements, get instant CFO-grade dashboards, insights, and forecasts.',
  openGraph: {
    title: 'BloomFi - AI Financial Intelligence',
    description: 'Upload your bank statements. Get instant CFO-grade dashboards, insights, and forecasts.',
    url: BASE_URL,
    siteName: 'BloomFi',
    images: [
      {
        url: `${BASE_URL}/og-image.svg`,
        width: 1200,
        height: 630,
        alt: 'BloomFi - AI-Powered Financial Intelligence',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BloomFi - AI Financial Intelligence',
    description: 'Upload your bank statements. Get instant CFO-grade dashboards.',
    images: [`${BASE_URL}/og-image.svg`],
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const branch = process.env.NEXT_PUBLIC_GIT_BRANCH || 'dev'
  const commit = (process.env.NEXT_PUBLIC_GIT_COMMIT || 'unknown').slice(0, 8)

  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen flex flex-col">
        <Header />
        <div className="flex-1">{children}</div>
        <footer className="border-t border-gray-800/50 py-3 px-4 text-center">
          <span className="text-xs text-gray-600 font-mono">{branch}@{commit}</span>
        </footer>
      </body>
    </html>
  )
}
