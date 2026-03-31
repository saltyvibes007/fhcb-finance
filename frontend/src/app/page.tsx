import Link from 'next/link'

export default function Home() {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-300 to-emerald-400 bg-clip-text text-transparent">
          BloomFi
        </h1>
        <p className="text-xl text-gray-400 mb-4">
          AI-powered financial intelligence for community organizations
        </p>
        <p className="text-sm text-gray-500 mb-8">
          Upload your bank statements. Get instant CFO-grade dashboards, insights, and forecasts.
        </p>
        <Link
          href="/login"
          className="inline-block px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-blue-700 transition"
        >
          Sign In to Dashboard
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="text-3xl mb-4">📊</div>
          <h2 className="text-lg font-semibold mb-2">Financial Dashboard</h2>
          <p className="text-sm text-gray-400">Balance sheet, P&L, cash flow — generated automatically from your statements.</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="text-3xl mb-4">🤖</div>
          <h2 className="text-lg font-semibold mb-2">AI Advisor</h2>
          <p className="text-sm text-gray-400">Ask questions about your finances in plain English. Get answers backed by your real data.</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="text-3xl mb-4">📈</div>
          <h2 className="text-lg font-semibold mb-2">Forecasting</h2>
          <p className="text-sm text-gray-400">Cash flow projections, seasonal trends, and budget recommendations.</p>
        </div>
      </div>
    </main>
  )
}
