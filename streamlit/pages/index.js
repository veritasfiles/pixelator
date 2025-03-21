import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-4xl font-bold mb-4">🟣 Pixel Art Lab</h1>
      <p className="text-lg text-center max-w-xl mb-6">
        Turn your images into customisable pixel animations – with full control over effects like shimmering, blinking, bobbing, glitching, and more.
      </p>
      <Link href="/pixel-art">
        <button className="px-6 py-3 bg-green-500 text-white rounded text-lg font-semibold hover:bg-green-600">
          Try the Pixel Art Generator →
        </button>
      </Link>
    </main>
  );
}
