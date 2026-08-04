import React, { useState, useEffect, useRef } from "react";

/**
 * dashboard.jsx
 * SideChannel Sentinel — Operator Console
 * Dark radar/signal-analysis aesthetic: agents surface as a live trace feed,
 * detection results resolve on a sweeping risk dial instead of a stat card.
 */

const AGENTS = ["Supervisor", "Detector", "Retriever", "Reporter"];

const MOCK_TRACE = [
  { agent: "Supervisor", msg: "Routing query → risk assessment path", t: 0 },
  { agent: "Detector", msg: "Running CNN classifier on trace window #482", t: 900 },
  { agent: "Detector", msg: "Leakage signature match: power-analysis, conf 0.91", t: 1600 },
  { agent: "Retriever", msg: "Rewriting query for MITRE lookup", t: 2300 },
  { agent: "Retriever", msg: "Retrieved 4 docs · relevance: pass", t: 3100 },
  { agent: "Reporter", msg: "Drafting mitigation + incident report", t: 3900 },
  { agent: "Reporter", msg: "Hallucination check: pass · quality: pass", t: 4600 },
];

const AGENT_COLOR = {
  Supervisor: "#4FD8E8",
  Detector: "#FF6B6B",
  Retriever: "#F5A623",
  Reporter: "#8B7CFF",
};

function RiskDial({ score }) {
  const angle = (score / 100) * 270 - 135;
  return (
    <div className="relative w-56 h-56 mx-auto">
      <svg viewBox="0 0 200 200" className="w-full h-full">
        <circle cx="100" cy="100" r="88" fill="none" stroke="#151B22" strokeWidth="14" />
        <circle
          cx="100" cy="100" r="88" fill="none"
          stroke={score > 66 ? "#FF4757" : score > 33 ? "#F5A623" : "#4FD8E8"}
          strokeWidth="14" strokeLinecap="round"
          strokeDasharray={`${(score / 100) * 415} 415`}
          transform="rotate(-135 100 100)"
          className="transition-all duration-700 ease-out"
        />
        <line
          x1="100" y1="100"
          x2={100 + 62 * Math.cos((angle * Math.PI) / 180)}
          y2={100 + 62 * Math.sin((angle * Math.PI) / 180)}
          stroke="#E8EDF2" strokeWidth="2"
          className="transition-all duration-700 ease-out"
        />
        <circle cx="100" cy="100" r="5" fill="#E8EDF2" />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center pt-6">
        <span className="text-4xl font-mono font-semibold text-[#E8EDF2]">{score}</span>
        <span className="text-[10px] tracking-[0.2em] text-[#5A6673] uppercase mt-1">Risk Index</span>
      </div>
    </div>
  );
}

function AgentPill({ name, active }) {
  return (
    <div
      className="flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all duration-300"
      style={{
        borderColor: active ? AGENT_COLOR[name] : "#1E2530",
        backgroundColor: active ? `${AGENT_COLOR[name]}14` : "transparent",
      }}
    >
      <span
        className="w-1.5 h-1.5 rounded-full"
        style={{ backgroundColor: active ? AGENT_COLOR[name] : "#3A4250" }}
      />
      <span
        className="text-xs font-mono"
        style={{ color: active ? AGENT_COLOR[name] : "#5A6673" }}
      >
        {name}
      </span>
    </div>
  );
}

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [running, setRunning] = useState(false);
  const [trace, setTrace] = useState([]);
  const [activeAgent, setActiveAgent] = useState(null);
  const [riskScore, setRiskScore] = useState(0);
  const [verdict, setVerdict] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [trace]);

  const runAnalysis = () => {
    if (!query.trim() || running) return;
    setRunning(true);
    setTrace([]);
    setVerdict(null);
    setRiskScore(0);

    MOCK_TRACE.forEach((step, i) => {
      setTimeout(() => {
        setActiveAgent(step.agent);
        setTrace((prev) => [...prev, step]);
        if (i === MOCK_TRACE.length - 1) {
          setTimeout(() => {
            setRiskScore(78);
            setVerdict({
              label: "ATTACK DETECTED",
              type: "Power-Analysis Side-Channel",
              confidence: 0.91,
            });
            setActiveAgent(null);
            setRunning(false);
          }, 500);
        }
      }, step.t);
    });
  };

  return (
    <div className="min-h-screen bg-[#0B0F14] text-[#E8EDF2] font-sans">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');
        .font-sans { font-family: 'Inter', sans-serif; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        @keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
        .scanline::after {
          content: ''; position: absolute; inset: 0; height: 40%;
          background: linear-gradient(180deg, transparent, rgba(79,216,232,0.05), transparent);
          animation: scan 3s linear infinite;
        }
      `}</style>

      {/* Header */}
      <header className="border-b border-[#151B22] px-8 py-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-[#4FD8E8]/10 border border-[#4FD8E8]/30 flex items-center justify-center">
            <span className="text-[#4FD8E8] text-sm font-mono">◈</span>
          </div>
          <div>
            <h1 className="text-sm font-semibold tracking-wide">SIDECHANNEL SENTINEL</h1>
            <p className="text-[10px] text-[#5A6673] font-mono tracking-widest">OPERATOR CONSOLE</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-mono text-[#5A6673]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#39D98A] animate-pulse" />
          LOCAL · OLLAMA CONNECTED
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-10 grid grid-cols-3 gap-8">
        {/* Left: Query + Agent trace */}
        <section className="col-span-2 space-y-6">
          <div>
            <label className="text-[10px] tracking-[0.2em] text-[#5A6673] uppercase mb-2 block">
              Query / Trace Input
            </label>
            <div className="flex gap-2">
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && runAnalysis()}
                placeholder="e.g. Analyze trace window #482 for power-analysis leakage"
                className="flex-1 bg-[#12171E] border border-[#1E2530] rounded-lg px-4 py-3 text-sm font-mono
                           placeholder:text-[#3A4250] focus:outline-none focus:border-[#4FD8E8]/60 transition-colors"
              />
              <button
                onClick={runAnalysis}
                disabled={running}
                className="px-5 py-3 rounded-lg bg-[#4FD8E8] text-[#0B0F14] text-sm font-semibold
                           hover:bg-[#6EE3F0] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                {running ? "Running…" : "Analyze"}
              </button>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {AGENTS.map((a) => (
              <AgentPill key={a} name={a} active={activeAgent === a} />
            ))}
          </div>

          <div>
            <label className="text-[10px] tracking-[0.2em] text-[#5A6673] uppercase mb-2 block">
              Live Agent Trace
            </label>
            <div
              ref={scrollRef}
              className="relative overflow-hidden bg-[#0E1319] border border-[#1E2530] rounded-lg h-72 p-4 overflow-y-auto scanline"
            >
              {trace.length === 0 && (
                <p className="text-[#3A4250] text-xs font-mono">Awaiting query…</p>
              )}
              {trace.map((step, i) => (
                <div key={i} className="flex gap-3 mb-2.5 text-xs font-mono animate-[fadeIn_0.3s_ease]">
                  <span style={{ color: AGENT_COLOR[step.agent] }} className="shrink-0 w-20">
                    {step.agent}
                  </span>
                  <span className="text-[#8A93A0]">{step.msg}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Right: Risk dial + verdict */}
        <section className="space-y-6">
          <div className="bg-[#0E1319] border border-[#1E2530] rounded-lg p-6">
            <RiskDial score={riskScore} />
          </div>

          <div className="bg-[#0E1319] border border-[#1E2530] rounded-lg p-5">
            <label className="text-[10px] tracking-[0.2em] text-[#5A6673] uppercase mb-3 block">
              Verdict
            </label>
            {verdict ? (
              <div className="space-y-2">
                <div className="inline-block px-2.5 py-1 rounded bg-[#FF4757]/10 border border-[#FF4757]/30">
                  <span className="text-[#FF4757] text-xs font-mono font-semibold">{verdict.label}</span>
                </div>
                <p className="text-sm text-[#E8EDF2]">{verdict.type}</p>
                <p className="text-xs text-[#5A6673] font-mono">
                  confidence {(verdict.confidence * 100).toFixed(0)}%
                </p>
              </div>
            ) : (
              <p className="text-xs text-[#3A4250] font-mono">No verdict yet</p>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
