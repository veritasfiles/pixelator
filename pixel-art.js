// Next.js (React) frontend with Tailwind for a mobile-friendly PWA pixel art editor

import { useState, useEffect } from 'react';
import Head from 'next/head';
import Image from 'next/image';
import axios from 'axios';

export default function Home() {
    const [image, setImage] = useState(null);
    const [effects, setEffects] = useState([]);
    const [pixelSize, setPixelSize] = useState(80);
    const [frameCount, setFrameCount] = useState(4);
    const [fps, setFps] = useState(12);
    const [generatedImage, setGeneratedImage] = useState(null);
    
    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            setImage(URL.createObjectURL(file));
        }
    };
    
    const handleEffectSelection = (effect) => {
        setEffects(prev => prev.includes(effect) ? prev.filter(e => e !== effect) : [...prev, effect]);
    };
    
    const generatePixelArt = async () => {
        const response = await axios.post('/api/generate', {
            pixelSize,
            frameCount,
            fps,
            effects,
            image,
        });
        setGeneratedImage(response.data.imageUrl);
    };

    return (
        <div className="flex flex-col items-center min-h-screen p-4 bg-gray-900 text-white">
            <Head>
                <title>Pixel Art Generator</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </Head>
            
            <h1 className="text-2xl font-bold">🎨 Pixel Art Generator</h1>
            <input type="file" accept="image/*" onChange={handleImageUpload} className="mt-4" />
            
            {image && <Image src={image} alt="Uploaded Image" width={300} height={200} className="mt-4" />}
            
            <div className="flex flex-wrap gap-2 mt-4">
                {['Blinking', 'Bobbing', 'Glitch', 'Shimmer', 'Colour Shift', 'Normal Glitch'].map(effect => (
                    <button key={effect} onClick={() => handleEffectSelection(effect)}
                        className={`px-4 py-2 border ${effects.includes(effect) ? 'bg-blue-500' : 'bg-gray-700'}`}>{effect}</button>
                ))}
            </div>
            
            <button onClick={generatePixelArt} className="mt-4 px-6 py-2 bg-green-500 text-white font-bold rounded">
                Generate Pixel Art
            </button>
            
            {generatedImage && <Image src={generatedImage} alt="Pixel Art" width={300} height={200} className="mt-4" />}
        </div>
    );
}
