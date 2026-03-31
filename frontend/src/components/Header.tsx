import Link from 'next/link'

export default function Header() {
  return (
    <header className="border-b border-gray-800 bg-gray-950/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
              BloomFi
            </span>
            <span className="text-xs text-gray-500 font-medium border border-gray-700 rounded px-1.5 py-0.5">
              {process.env.NEXT_PUBLIC_BRANCH || 'dev'}
            </span>
          </Link>
          <nav className="flex items-center gap-6">
            <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white transition">
              Dashboard
            </Link>
            <Link href="/upload" className="text-sm text-gray-400 hover:text-white transition">
              Upload
            </Link>
            <Link href="/chat" className="text-sm text-gray-400 hover:text-white transition">
              AI Chat
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
