'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function Header() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [orgName, setOrgName] = useState('')
  const router = useRouter()
  const branch = process.env.NEXT_PUBLIC_GIT_BRANCH || 'dev'

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const name = localStorage.getItem('org_name')
    setLoggedIn(!!token)
    setOrgName(name || '')
  }, [])

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('org_slug')
    localStorage.removeItem('org_name')
    setLoggedIn(false)
    router.push('/')
  }

  return (
    <header className="border-b border-gray-800 bg-gray-950/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
              BloomFi
            </span>
            <span className="text-xs text-gray-500 font-medium border border-gray-700 rounded px-1.5 py-0.5">
              {branch}
            </span>
          </Link>
          <nav className="flex items-center gap-6">
            {loggedIn ? (
              <>
                <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white transition">
                  Dashboard
                </Link>
                <Link href="/upload" className="text-sm text-gray-400 hover:text-white transition">
                  Upload
                </Link>
                <Link href="/chat" className="text-sm text-gray-400 hover:text-white transition">
                  AI Chat
                </Link>
                <span className="text-xs text-gray-500">{orgName}</span>
                <button onClick={logout} className="text-sm text-gray-500 hover:text-red-400 transition">
                  Sign Out
                </button>
              </>
            ) : (
              <Link href="/login" className="text-sm text-blue-400 hover:text-blue-300 transition">
                Sign In
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
