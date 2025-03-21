
// pages/index.js – Homepage with a button to Pixel Art Generator

import Link from 'next/link';
import Head from 'next/head';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-950 text-white">
      <Head>
        <title>🎨 Welcome to Pixelator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <h1 className="text-4xl font-bold text-center mb-6">🎨 Welcome to Pixelator!</h1>
      <p className="text-lg text-gray-300 text-center max-w-xl mb-8">
        Turn your images into animated pixel art masterpieces!
      </p>

      <Link href="/pixel-art">
        <a className="px-6 py-3 bg-blue-600 text-white rounded-lg text-lg font-semibold shadow-md hover:bg-blue-500">
          🚀 Launch Pixel Art Generator
        </a>
      </Link>
    </div>
  );
}
