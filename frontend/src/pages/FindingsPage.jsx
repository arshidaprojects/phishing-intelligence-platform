import { useEffect, useState } from "react";
import { getFindings } from "../api/client";

const riskColour = { Low:"bg-green-900 text-green-300", Medium:"bg-yellow-900 text-yellow-300", High:"bg-orange-900 text-orange-300", Critical:"bg-red-900 text-red-300" };

export default function FindingsPage() {
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFindings().then(r => {
      setFindings(r.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <p className="text-slate-400">Loading findings...</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">Findings</h1>
      <p className="text-slate-400 mb-8">{findings.length} phishing samples analysed and stored.</p>

      <div className="space-y-4">
        {findings.map((f, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-start justify-between mb-3">
              <div>
                <span className="text-blue-400 font-medium">{f.attack_type}</span>
                <span className="text-slate-400 mx-2">—</span>
                <span className="text-slate-300">{f.subtype}</span>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${riskColour[f.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {f.risk_level} Risk
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 mb-3">
              {[["Channel", f.channel], ["Sophistication", f.sophistication], ["Target", f.target_sector]].map(([k,v]) => (
                <div key={k} className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-400 text-xs mb-1">{k}</p>
                  <p className="text-slate-200 text-sm font-medium">{v}</p>
                </div>
              ))}
            </div>

            <p className="text-slate-400 text-sm mb-3">{f.technique_description}</p>

            <div className="flex flex-wrap gap-2 mb-3">
              {f.indicators?.map((ind, j) => (
                <span key={j} className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full">{ind}</span>
              ))}
            </div>

            <div className="flex items-center justify-between">
              <p className="text-slate-600 text-xs">
                Method: {f.input_method} · {new Date(f.detected_at).toLocaleString()}
              </p>
              <span className="text-xs bg-slate-800 text-slate-400 px-2 py-1 rounded">
                {f.source}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}