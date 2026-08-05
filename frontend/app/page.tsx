"use client";

import { useState } from "react";

type ClaimResult = {
  user_id: string;
  claim_status: string;
  issue_type: string;
  object_part: string;
  severity: string;
  evidence_standard_met: boolean;
  risk_flags: string[];
  claim_status_justification: string;
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [userId, setUserId] = useState("U1001");
  const [claimObject, setClaimObject] = useState("car");
  const [userClaim, setUserClaim] = useState("I scratched the door on a pole.");
  const [useMock, setUseMock] = useState(true);
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ClaimResult | null>(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an image.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("claim_object", claimObject);
    formData.append("user_claim", userClaim);
    formData.append("use_mock", useMock.toString());
    formData.append("images", file);

    try {
      const res = await fetch("http://localhost:8000/api/v1/claims/submit", {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) {
        throw new Error(`API returned ${res.status}`);
      }
      
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 md:p-24 flex flex-col items-center">
      <div className="w-full max-w-5xl">
        <header className="mb-12 text-center md:text-left">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-300">
            Multi-Modal Evidence Review
          </h1>
          <p className="text-slate-400 text-lg">
            Enterprise-grade claims processing powered by Vision-Language Models.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div className="glass-panel p-8 rounded-2xl">
            <h2 className="text-2xl font-semibold mb-6">Submit Claim</h2>
            <form onSubmit={handleSubmit} className="space-y-5">
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Claim Object</label>
                <select 
                  value={claimObject} 
                  onChange={(e) => setClaimObject(e.target.value)}
                  className="w-full bg-slate-800/50 border border-slate-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                >
                  <option value="car">Car</option>
                  <option value="laptop">Laptop</option>
                  <option value="package">Package</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">User Description</label>
                <textarea 
                  value={userClaim} 
                  onChange={(e) => setUserClaim(e.target.value)}
                  className="w-full bg-slate-800/50 border border-slate-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all min-h-[100px]"
                  placeholder="Describe what happened..."
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Evidence Image</label>
                <div className="border-2 border-dashed border-slate-600 rounded-xl p-6 text-center hover:border-blue-500 transition-colors bg-slate-800/30 cursor-pointer relative">
                  <input 
                    type="file" 
                    accept="image/*"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  {file ? (
                    <span className="text-blue-400 font-medium">{file.name}</span>
                  ) : (
                    <span className="text-slate-400">Drag & drop an image, or click to browse</span>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-3 pt-2">
                <input 
                  type="checkbox" 
                  id="useMock" 
                  checked={useMock} 
                  onChange={(e) => setUseMock(e.target.checked)}
                  className="w-5 h-5 rounded border-slate-600 bg-slate-800 text-blue-500 focus:ring-blue-500"
                />
                <label htmlFor="useMock" className="text-sm font-medium text-slate-300 cursor-pointer">
                  Use Mock AI (Fast Local Simulation)
                </label>
              </div>

              <button 
                type="submit" 
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-4 rounded-xl transition-all shadow-lg shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                ) : "Process Claim"}
              </button>
            </form>
          </div>

          {/* Results Column */}
          <div className="flex flex-col gap-6">
            {error && (
              <div className="bg-red-900/40 border border-red-500/50 text-red-200 px-6 py-4 rounded-xl flex items-center gap-3">
                <span className="text-xl">⚠️</span> {error}
              </div>
            )}
            
            {result ? (
              <div className="glass-panel p-8 rounded-2xl animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="flex items-center justify-between mb-6 border-b border-slate-700/50 pb-4">
                  <h2 className="text-2xl font-semibold">AI Analysis Result</h2>
                  <span className={`px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-wider ${
                    result.claim_status === 'supported' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                    result.claim_status === 'rejected' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                    'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  }`}>
                    {result.claim_status}
                  </span>
                </div>
                
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
                      <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">Detected Object Part</div>
                      <div className="font-medium text-lg text-indigo-300 capitalize">{result.object_part.replace('_', ' ')}</div>
                    </div>
                    <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
                      <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">Detected Issue</div>
                      <div className="font-medium text-lg text-amber-300 capitalize">{result.issue_type.replace('_', ' ')}</div>
                    </div>
                  </div>

                  <div className="bg-slate-800/40 p-5 rounded-xl border border-slate-700/50">
                    <div className="text-slate-400 text-xs uppercase tracking-wider mb-2">Justification</div>
                    <p className="text-slate-200 leading-relaxed text-sm">
                      {result.claim_status_justification}
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="flex flex-col gap-1">
                      <span className="text-slate-400 text-xs uppercase tracking-wider">Severity</span>
                      <span className="text-slate-200 capitalize font-medium">{result.severity}</span>
                    </div>
                    <div className="flex flex-col gap-1">
                      <span className="text-slate-400 text-xs uppercase tracking-wider">Evidence Standard</span>
                      <span className="text-slate-200 font-medium">
                        {result.evidence_standard_met ? '✅ Met' : '❌ Not Met'}
                      </span>
                    </div>
                  </div>

                  {result.risk_flags && result.risk_flags.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-slate-700/50">
                      <div className="text-slate-400 text-xs uppercase tracking-wider mb-3">Risk & Fraud Flags</div>
                      <div className="flex flex-wrap gap-2">
                        {result.risk_flags.map((flag, idx) => (
                          <span key={idx} className="bg-rose-500/10 text-rose-400 border border-rose-500/20 px-3 py-1 rounded-md text-xs font-medium uppercase tracking-wide">
                            {flag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="glass-panel p-8 rounded-2xl h-full flex flex-col items-center justify-center text-center opacity-50">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-medium text-slate-300 mb-2">Ready to Analyze</h3>
                <p className="text-slate-400 text-sm max-w-xs">
                  Submit a claim and evidence image to see the multi-modal pipeline in action.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
