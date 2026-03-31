'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [slug, setSlug] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [attempts, setAttempts] = useState(0)
  const [locked, setLocked] = useState(false)
  const router = useRouter()

  const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    if (locked) return

    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_URL}/api/v1/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, password }),
      })

      const data = await res.json()

      if (res.ok) {
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        localStorage.setItem('org_slug', data.organization?.slug || slug)
        localStorage.setItem('org_name', data.organization?.name || slug)
        router.push('/dashboard')
      } else {
        const newAttempts = attempts + 1
        setAttempts(newAttempts)
        if (newAttempts >= 3) {
          setLocked(true)
          setError('Too many failed attempts. Locked for 15 minutes.')
          setTimeout(() => { setLocked(false); setAttempts(0) }, 15 * 60 * 1000)
        } else {
          setError(`Invalid credentials. ${3 - newAttempts} attempt${3 - newAttempts > 1 ? 's' : ''} remaining.`)
        }
      }
    } catch {
      setError('Unable to connect to server. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-[calc(100vh-8rem)] items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 backdrop-blur-sm">
          <div className="text-center mb-8">
            <div className="text-xs font-bold tracking-[4px] text-gray-500 uppercase mb-6">
              BloomFi Corp
            </div>
            <h1 className="text-2xl font-bold text-white mb-2">Sign In</h1>
            <p className="text-sm text-gray-500">Enter your organization credentials</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1.5">Organization ID</label>
              <input
                type="text"
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
                placeholder="e.g. fhcb"
                disabled={locked}
                className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white text-sm placeholder-gray-600 focus:outline-none focus:border-blue-500 transition disabled:opacity-50"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-400 mb-1.5">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                disabled={locked}
                className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white text-sm placeholder-gray-600 focus:outline-none focus:border-blue-500 transition disabled:opacity-50"
                required
              />
            </div>

            {error && (
              <p className="text-red-400 text-xs text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading || locked}
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-sm font-semibold rounded-lg hover:from-blue-600 hover:to-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Access Dashboard'}
            </button>
          </form>
        </div>
      </div>
    </main>
  )
}
