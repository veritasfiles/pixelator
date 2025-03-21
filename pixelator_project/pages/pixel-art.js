
// pages/pixel-art.js – Main Pixel Art Generator

import { useState } from 'react';
import Head from 'next/head';

export default function PixelArtPage() {
  const [image, setImage] = useState(null);
  const [effects, setEffects] = useState([]);
  const [pixelSize, setPixelSize] = useState(80);
  const [frameCount, setFrameCount] = useState(4);
  const [fps, setFps] = useState(12);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [intensity, setIntensity] = useState({ Glitch: 5, Shimmer: 5 });

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImage(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const handleEffectToggle = (effect) => {
    setEffects((prev) =>
      prev.includes(effect) ? prev.filter((e) => e !== effect) : [...prev, effect]
    );
  };

  const generate = async () => {
    const res = await fetch('/api/generate', {
      method: 'POST',
      body: JSON.stringify({
        image,
        effects,
        pixelSize,
        frameCount,
        fps,
        intensity,
      }),
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await res.json();
    setGeneratedImage(data.image);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white px-4 py-6 flex flex-col items-center">
      <Head>
        <title>Pixel Art Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <h1 className="text-2xl font-bold mb-4">🎨 Pixel Art Generator</h1>

      <input type="file" accept="image/*" onChange={handleImageUpload} className="mb-4" />

      {image && <img src={image} alt="Input" className="max-w-xs mb-4 rounded shadow" />}

      <div className="grid gap-2 mb-4">
        {['Blinking', 'Bobbing', 'Glitch', 'Shimmer', 'Colour Shift', 'Normal Glitch'].map((effect) => (
          <div key={effect} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={effects.includes(effect)}
              onChange={() => handleEffectToggle(effect)}
            />
            <label>{effect}</label>
            {(effect === 'Glitch' || effect === 'Shimmer') && effects.includes(effect) && (
              <input
                type="range"
                min="1"
                max="10"
                value={intensity[effect]}
                onChange={(e) =>
                  setIntensity((prev) => ({ ...prev, [effect]: parseInt(e.target.value) }))
                }
              />
            )}
          </div>
        ))}
      </div>

      <button onClick={generate} className="px-6 py-3 bg-green-600 text-white rounded-lg text-lg font-semibold hover:bg-green-500">
        Generate Pixel Art
      </button>

      {generatedImage && (
        <div className="mt-6">
          <h2 className="text-lg font-semibold mb-2">Result:</h2>
          <img src={generatedImage} alt="Pixel Art Output" className="rounded shadow" />
          <a href={generatedImage} download="pixel_art.gif" className="block mt-2 text-blue-400 underline">
            Download GIF
          </a>
        </div>
      )}
    </div>
  );
}
