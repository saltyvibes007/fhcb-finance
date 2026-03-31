'use client'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://uat-backend-corp.bloomfi.ai'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
          BloomFi
        </h1>
        <p className="text-xl text-gray-400 mb-8">
          AI-powered financial dashboard for community organizations
        </p>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 text-left">
          <h2 className="text-lg font-semibold mb-4">System Status</h2>
          <div className="space-y-2 text-sm text-gray-400">
            <div className="flex justify-between">
              <span>Backend API</span>
              <span className="text-green-400">{API_URL}</span>
            </div>
            <div className="flex justify-between">
              <span>Branch</span>
              <span className="text-blue-400">{process.env.NEXT_PUBLIC_BRANCH}</span>
            </div>
            <div className="flex justify-between">
              <span>Commit</span>
              <span className="text-gray-500 font-mono text-xs">{process.env.NEXT_PUBLIC_COMMIT?.slice(0, 8)}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
