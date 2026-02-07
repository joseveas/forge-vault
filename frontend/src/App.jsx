import { useState } from 'react';

function App() {
  const [prompt, setPrompt] = useState('');
  const [respuesta, setRespuesta] = useState(null);
  const [loading, setLoading] = useState(false);

  // Función que conecta con TU backend
  const enviarAGemini = async () => {
    if (!prompt) return;
    setLoading(true);
    setRespuesta(null);

    try {
      // 1. Llamada a tu API Python
      const response = await fetch('http://localhost:8000/test-gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: prompt }),
      });

      // 2. Procesar respuesta
      const data = await response.json();
      setRespuesta(data);
    } catch (error) {
      console.error("Error:", error);
      setRespuesta({ error: "❌ Error: ¿Está corriendo el backend en el puerto 8000?" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center p-4">
      <div className="max-w-xl w-full bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700">
        
        {/* Encabezado */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-blue-500 mb-2">ForgeVault 🛡️</h1>
          <p className="text-slate-400">Inventory AI System</p>
        </div>

        {/* Input Area */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2 text-slate-300">
              Consulta a Gemini 3:
            </label>
            <textarea
              className="w-full p-4 bg-slate-950 border border-slate-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-slate-200 placeholder-slate-600 transition-all"
              rows="3"
              placeholder="Ej: Inventa un nombre para una poción de mana..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <button
            onClick={enviarAGemini}
            disabled={loading}
            className={`w-full py-4 px-6 rounded-xl font-bold text-lg transition-all transform active:scale-95 ${
              loading 
                ? 'bg-slate-700 text-slate-500 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 shadow-lg shadow-blue-900/20'
            }`}
          >
            {loading ? '🔄 Procesando...' : 'Enviar Comando 🚀'}
          </button>
        </div>

        {/* Área de Resultados */}
        {respuesta && (
          <div className="mt-8 pt-6 border-t border-slate-700 animate-pulse-once">
            <h3 className="text-sm font-bold text-emerald-400 mb-3 uppercase tracking-wider">
              Respuesta del Sistema:
            </h3>
            
            <div className="bg-slate-950 rounded-lg p-4 border border-slate-700/50">
              {respuesta.gemini_dijo ? (
                <>
                  <p className="text-slate-300 leading-relaxed whitespace-pre-wrap">
                    {respuesta.gemini_dijo}
                  </p>
                  <div className="mt-4 flex items-center gap-2 text-xs text-slate-500 font-mono">
                    <span>💾 ID Firestore:</span>
                    <span className="text-orange-400">{respuesta.firestore_id}</span>
                  </div>
                </>
              ) : (
                <p className="text-red-400 font-bold">{respuesta.error}</p>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;