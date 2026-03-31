/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://uat-backend-corp.bloomfi.ai',
    NEXT_PUBLIC_BRANCH: process.env.RAILWAY_GIT_BRANCH || 'unknown',
    NEXT_PUBLIC_COMMIT: process.env.RAILWAY_GIT_COMMIT_SHA || 'unknown',
  },
}

module.exports = nextConfig
