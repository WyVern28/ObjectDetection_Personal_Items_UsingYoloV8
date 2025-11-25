import { useState } from 'react';

// url api backend
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

//icon (svg) components
const CameraIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
    <circle cx="12" cy="13" r="3"/>
  </svg>
);

const UploadIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="17 8 12 3 7 8"/>
    <line x1="12" x2="12" y1="3" y2="15"/>
  </svg>
);

const StopIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <circle cx="12" cy="12" r="10"/>
    <path d="m15 9-6 6"/>
    <path d="m9 9 6 6"/>
  </svg>
);

const ApertureIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <circle cx="12" cy="12" r="10"/>
    <path d="m14.31 8 5.74 9.94"/>
    <path d="M9.69 8h11.48"/>
    <path d="m7.38 12 5.74-9.94"/>
    <path d="M9.69 16 3.95 6.06"/>
    <path d="M14.31 16H2.83"/>
    <path d="m16.62 12-5.74 9.94"/>
  </svg>
);

export default function App() {
  // --- STATE ---
  const [inputType, setInputType] = useState('none'); // 'none', 'webcam', 'upload'
  const [imageResult, setImageResult] = useState(null);
  const [streamTrigger, setStreamTrigger] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  // --- HANDLERS ---

  const handleStop = async () => {
    setInputType('none');
    setImageResult(null);
    try {
      await fetch(`${API_BASE}/stop_camera`, { method: 'POST' });
    } catch (e) { console.error("Error stopping", e); }
  };

  const handleWebcam = async () => {
    setInputType('webcam');
    setImageResult(null);
    try {
      await fetch(`${API_BASE}/set_webcam`, { method: 'POST' });
      setStreamTrigger(prev => prev + 1);
    } catch (e) { console.error("Error webcam", e); }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setIsLoading(true);
    setInputType('upload');

    try {
      // upload file
      const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
      const data = await res.json();

      if (data.type === 'image') {
        // jika gambar, fetch hasil prosesnya
        const imgRes = await fetch(`${API_BASE}/processed_image`);
        const imgData = await imgRes.json();
        if (imgData.image) {
          setImageResult(imgData.image);
        }
      } else {
        // jika video upload, reset result dan trigger stream
        setImageResult(null);
        setStreamTrigger(prev => prev + 1);
      }
    } catch (error) {
      alert("Gagal upload atau backend offline.");
      handleStop();
    } finally {
      setIsLoading(false);
    }
  };

  //UIIII

  return (
    <div className="relative w-screen h-screen bg-neutral-950 overflow-hidden flex flex-col items-center justify-center text-white font-sans selection:bg-indigo-500 selection:text-white">
      
      {/* background */}
      <div className="absolute inset-0 flex items-center justify-center z-0">
        
        {/* state: loading */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center space-y-6 z-50">
             {/* animasi loading */}
            <div className="relative">
              <div className="w-20 h-20 border-4 border-indigo-500/30 rounded-full animate-spin"></div>
              <div className="absolute top-0 left-0 w-20 h-20 border-4 border-t-indigo-500 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <ApertureIcon className="w-8 h-8 text-indigo-400 animate-pulse" />
              </div>
            </div>
            
            <div className="text-center">
              <h2 className="text-xl font-bold tracking-[0.2em] text-white">ANALYZING</h2>
              <p className="text-sm text-indigo-400 mt-1 font-mono">Processing media data...</p>
            </div>
          </div>
        ) : (
          // State: DISPLAY CONTENT
          <>
            {inputType === 'none' && (
              // idle state (abstract background)
              <div className="flex flex-col items-center opacity-30 select-none">
                <div className="w-96 h-96 bg-indigo-600/20 rounded-full blur-[128px] absolute"></div>
                <h1 className="text-6xl md:text-8xl font-black text-white/10 tracking-tighter">AI DETECTION</h1>
                <p className="mt-4 text-white/40 font-light tracking-widest uppercase text-sm">Waiting for input source</p>
              </div>
            )}

            {inputType === 'webcam' && (
              <img 
                src={`${API_BASE}/video_feed?t=${streamTrigger}`} 
                className="w-full h-full object-contain"
                alt="Live Stream"
              />
            )}

            {inputType === 'upload' && imageResult && (
              <img 
                src={imageResult} 
                className="w-full h-full object-contain shadow-2xl"
                alt="Processed Result" 
              />
            )}
            
            {/* Fallback untuk upload video (jika backend streaming video upload) */}
            {inputType === 'upload' && !imageResult && (
               <img 
               src={`${API_BASE}/video_feed?t=${streamTrigger}`} 
               className="w-full h-full object-contain"
               alt="Uploaded Stream"
             />
            )}
          </>
        )}
      </div>

      {/* control panel */}
      <div className="absolute bottom-10 z-40 transition-all duration-500 ease-in-out transform translate-y-0">
        <div className="flex items-center gap-4 px-6 py-4 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl ring-1 ring-white/5">
          
          {/* button (stop) */}
          <button 
            onClick={handleStop}
            className={`group relative flex flex-col items-center justify-center w-16 h-16 rounded-xl transition-all duration-300
              ${inputType === 'none' 
                ? 'bg-red-500/20 text-red-400 ring-2 ring-red-500/50 shadow-[0_0_20px_rgba(239,68,68,0.3)]' 
                : 'hover:bg-white/10 text-gray-400 hover:text-white'}`}
          >
            <StopIcon className="w-6 h-6 mb-1" />
            <span className="text-[10px] font-bold tracking-wider">STOP</span>
          </button>

          {/* Divider Vertical */}
          <div className="w-px h-10 bg-white/10 mx-2"></div>

          {/* button (webcam) */}
          <button 
            onClick={handleWebcam}
            disabled={isLoading}
            className={`group relative flex flex-col items-center justify-center w-16 h-16 rounded-xl transition-all duration-300
              ${inputType === 'webcam' 
                ? 'bg-cyan-500/20 text-cyan-400 ring-2 ring-cyan-500/50 shadow-[0_0_20px_rgba(6,182,212,0.3)]' 
                : 'hover:bg-white/10 text-gray-400 hover:text-white'}`}
          >
            <CameraIcon className="w-6 h-6 mb-1" />
            <span className="text-[10px] font-bold tracking-wider">CAM</span>
          </button>

          {/* button (upload) */}
          <div className="relative">
            <input 
              type="file" 
              onChange={handleFileUpload} 
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              disabled={isLoading}
            />
            <button 
              className={`group relative flex flex-col items-center justify-center w-16 h-16 rounded-xl transition-all duration-300 pointer-events-none
                ${inputType === 'upload' 
                  ? 'bg-indigo-500/20 text-indigo-400 ring-2 ring-indigo-500/50 shadow-[0_0_20px_rgba(99,102,241,0.3)]' 
                  : 'group-hover:bg-white/10 text-gray-400 group-hover:text-white'}`}
            >
              <UploadIcon className="w-6 h-6 mb-1" />
              <span className="text-[10px] font-bold tracking-wider">FILE</span>
            </button>
          </div>

        </div>
      </div>

      {/* indicator status */}
      <div className="absolute top-6 left-6 z-30">
        <div className="flex items-center space-x-3">
          <div className={`w-2 h-2 rounded-full ${inputType !== 'none' && !isLoading ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-xs font-mono text-white/50 tracking-widest uppercase">
            {isLoading ? 'PROCESSING...' : inputType === 'none' ? 'SYSTEM IDLE' : `SOURCE: ${inputType}`}
          </span>
        </div>
      </div>

    </div>
  );
}