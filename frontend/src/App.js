import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [logs, setLogs] = useState("");
  const [result, setResult] = useState(null);
  const [summary, setSummary] = useState(null);
  const [ai, setAi] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!logs.trim()) {
      setError("Please paste log data before analyzing.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setSummary(null);
    setAi(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        logs,
      });

      setSummary(response.data.summary);
      setResult(response.data.final_result);
      setAi(response.data.ai_suggestion);

      setHistory([
        {
          logs,
          result: response.data.final_result,
          time: new Date().toLocaleString(),
        },
        ...history,
      ]);
    } catch (err) {
      console.error(err);
      setError("Unable to analyze logs. Please check if backend is running.");
    }

    setLoading(false);
  };

  const clearInput = () => {
    setLogs("");
    setResult(null);
    setSummary(null);
    setAi(null);
    setError("");
  };

  const severityClass = result?.severity?.toLowerCase() || "low";

  return (
    <div className="app">
      <div className="background-glow glow-one"></div>
      <div className="background-glow glow-two"></div>

      <header className="topbar">
        <div className="logo-box">⚡</div>
        <div>
          <h1>Log Diagnostic Dashboard</h1>
          <p>Human-built diagnostic engine for parsing logs, detecting issues, and recommending fixes.</p>
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <div>
            <span className="tag">Developer Debugging Tool</span>
            <h2>Turn raw logs into clear diagnostic reports</h2>
            <p>
              Paste application or server logs. The engine parses log lines,
              applies custom rules, ranks severity, calculates confidence, and
              shows actionable debugging steps.
            </p>
          </div>

          <div className="hero-card">
            <p>Engine Pipeline</p>
            <ul>
              <li>Parse logs</li>
              <li>Detect issue pattern</li>
              <li>Rank severity</li>
              <li>Recommend fixes</li>
            </ul>
          </div>
        </section>

        <section className="main-grid">
          <div className="left-panel">
            <div className="card input-card">
              <div className="section-title">
                <h3>Log Input</h3>
                <span>Ready</span>
              </div>

              <textarea
                value={logs}
                onChange={(e) => setLogs(e.target.value)}
                placeholder={`Example:
2026-05-06 10:15:23 ERROR Connection refused at port 5432
2026-05-06 10:15:26 WARN Retrying database connection
2026-05-06 10:15:30 ERROR Database not reachable`}
              />

              <div className="button-row">
                <button className="primary-btn" onClick={handleAnalyze} disabled={loading}>
                  {loading ? "Analyzing..." : "Analyze Logs"}
                </button>

                <button className="secondary-btn" onClick={clearInput}>
                  Clear
                </button>
              </div>

              {error && <div className="error">{error}</div>}
            </div>

            {summary && result && (
              <div className="stats-grid">
                <div className="stat-card">
                  <span>Total Lines</span>
                  <strong>{summary.total_lines}</strong>
                </div>

                <div className="stat-card">
                  <span>Matched Issues</span>
                  <strong>{summary.matched_issues}</strong>
                </div>

                <div className={`stat-card severity ${severityClass}`}>
                  <span>Severity</span>
                  <strong>{result.severity}</strong>
                </div>

                <div className="stat-card">
                  <span>Confidence</span>
                  <strong>{result.confidence}</strong>
                </div>
              </div>
            )}

            {result && (
              <div className="card report-card">
                <div className="report-header">
                  <div>
                    <span className="tag">Diagnostic Report</span>
                    <h3>{result.root}</h3>
                  </div>

                  <span className={`badge ${severityClass}`}>{result.severity}</span>
                </div>

                <div className="report-section">
                  <span>Category</span>
                  <p>{result.category}</p>
                </div>

                <div className="report-section danger-line">
                  <span>Detected Issue</span>
                  <p>{result.root}</p>
                </div>

                <div className="report-section">
                  <span>Why this happened</span>
                  <p>{result.explanation}</p>
                </div>

                <div className="report-section warning-line">
                  <span>Possible Impact</span>
                  <p>{result.impact}</p>
                </div>

                <div className="report-section evidence">
                  <span>Matched Evidence</span>
                  <code>{result.matched_evidence}</code>
                </div>

                <div className="report-section fixes">
                  <span>Recommended Actions</span>
                  <ol>
                    {result.fixes.map((fix, index) => (
                      <li key={index}>{fix}</li>
                    ))}
                  </ol>
                </div>
              </div>
            )}

            {ai && (
              <div className="card ai-card">
                <span>AI Enhancement</span>
                <p>{ai}</p>
              </div>
            )}
          </div>

          <aside className="right-panel">
            <div className="card history-card">
              <h3>Analysis History</h3>

              {history.length === 0 && (
                <p className="empty">No logs analyzed yet.</p>
              )}

              {history.map((item, index) => (
                <div className="history-item" key={index}>
                  <strong>{item.result.root}</strong>
                  <p>{item.time}</p>
                  <span>{item.result.severity}</span>
                </div>
              ))}
            </div>

            <div className="card explain-card">
              <h3>How it works</h3>
              <div className="step">
                <b>1</b>
                <p>Parser converts raw logs into structured records.</p>
              </div>
              <div className="step">
                <b>2</b>
                <p>Rule engine detects known failure patterns.</p>
              </div>
              <div className="step">
                <b>3</b>
                <p>Aggregator chooses the most important issue.</p>
              </div>
              <div className="step">
                <b>4</b>
                <p>AI can optionally enrich the explanation.</p>
              </div>
            </div>
          </aside>
        </section>
      </main>
    </div>
  );
}

export default App;