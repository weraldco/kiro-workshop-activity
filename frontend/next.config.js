/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // API proxy configuration - proxies to Python Flask backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:3535/api/:path*', // Python Flask backend
      },
    ];
  },
};

module.exports = nextConfig;
