import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "media.parfumo.com",
      },
      {
        protocol: "https",
        hostname: "fimgs.net",
      },
      {
        protocol: "https",
        hostname: "www.fragrantica.com",
      },
      {
        protocol: "https",
        hostname: "img.fragrantica.com",
      },
      {
        protocol: "https",
        hostname: "belvish.com",
      },
      {
        protocol: "https",
        hostname: "larose.az",
      },
      {
        protocol: "https",
        hostname: "postimg.cc",
      },
      {
        protocol: "https",
        hostname: "i.postimg.cc",
      },
    ],
  },
};

export default nextConfig;