/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable strict mode
  reactStrictMode: true,
  // Since we're using the App Router, no experimental flag needed
  experimental: {},
  // Add trailing slash to match backend expectations
  trailingSlash: false,
  // Image optimization settings
  images: {
    unoptimized: true, // Disable Next.js image optimization for now to avoid issues
  },
  // Configure headers for static assets
  async headers() {
    return [
      {
        // Apply security headers to all routes
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ]
  },
  // Configure redirects for API calls to backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*', // Proxy to backend
      },
      {
        source: '/auth/:path*',
        destination: 'http://localhost:8000/auth/:path*', // Proxy to backend auth
      },
      {
        source: '/health',
        destination: 'http://localhost:8000/health', // Health check
      },
    ]
  },
}

module.exports = nextConfig