/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  /**
   * Proxy browser requests to FastAPI so the app works when NEXT_PUBLIC_API_URL is unset.
   * Browser → http://localhost:3000/api-backend/... → BACKEND_URL (default http://127.0.0.1:8000)
   */
  async rewrites() {
    const backend = (
      process.env.BACKEND_URL || 'http://127.0.0.1:8000'
    ).replace(/\/$/, '')
    return [
      {
        source: '/api-backend/:path*',
        destination: `${backend}/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
