/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  env: {
    NEXT_PUBLIC_GIT_BRANCH:
      process.env.RAILWAY_GIT_BRANCH ||
      process.env.GIT_BRANCH ||
      "main",
    NEXT_PUBLIC_GIT_COMMIT:
      process.env.RAILWAY_GIT_COMMIT_SHA ||
      process.env.GIT_COMMIT ||
      "unknown",
  },
};

module.exports = nextConfig;
