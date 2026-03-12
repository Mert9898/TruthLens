import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [content, setContent] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const API_URL = import.meta.env.VITE_API_URL || '/api';

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_URL}/history`);
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!content.trim()) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      });
      if (response.ok) {
        const data = await response.json();
        setResult(data);
        fetchHistory();
      }
    } catch (error) {
      console.error('Error analyzing content:', error);
    } finally {
      setLoading(false);
    }
  };

  const getThreatColor = (label) => {
    if (label === 'Likely Reliable') return 'var(--threat-low)';
    if (label === 'Needs Verification') return 'var(--threat-mid)';
    return 'var(--threat-high)';
  };

  return (
    <>
      <div className="bg-grid"></div>
      
      <div className="container">
        <motion.header
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1>TruthLens</h1>
          <p className="description">Integrated Misinformation Analysis System</p>
        </motion.header>

        <div className="main-layout">
          {/* Input Section */}
          <motion.div 
            className="left-column"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <div className="cyber-card">
              <div className="status-bar">
                <span>[ STATUS: READY ]</span>
                <span>[ MODE: INTEL_SCAN ]</span>
              </div>
              <div style={{ position: 'relative' }}>
                <textarea
                  placeholder="INPUT STREAM: PASTE CONTENT FOR ANALYSIS..."
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                />
                {loading && <div className="scanner-line"></div>}
              </div>
              <motion.button 
                className="btn-scan" 
                onClick={handleAnalyze}
                disabled={loading || !content.trim()}
                whileHover={{ backgroundColor: "rgba(6, 182, 212, 0.1)" }}
                whileTap={{ scale: 0.98 }}
              >
                {loading ? '>>> CORE SCAN IN PROGRESS...' : 'EXECUTE CONTENT ANALYSIS'}
              </motion.button>
            </div>
          </motion.div>

          {/* Result Section */}
          <motion.div 
            className="right-column"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="cyber-card" style={{ minHeight: '430px' }}>
              <div className="status-bar">
                <span>[ DATA_UNIT: 01A ]</span>
                <span style={{ color: result ? getThreatColor(result.label) : 'var(--cyan)' }}>
                  {result ? `[ ${result.label.toUpperCase()} ]` : '[ STANDBY ]'}
                </span>
              </div>
              
              <AnimatePresence mode="wait">
                {result ? (
                  <motion.div 
                    key="result"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                  >
                    <div className="score-panel">
                      <div className="score-value" style={{ color: getThreatColor(result.label) }}>
                        {result.score}
                      </div>
                      <div className="threat-label" style={{ color: getThreatColor(result.label) }}>
                        {result.label}
                      </div>
                    </div>

                    <div className="technical-data">
                      <div className="data-row">
                        <span>THREAT_INDEX:</span>
                        <span>{100 - result.score}%</span>
                      </div>
                      <div className="data-row">
                        <span>TIMESTAMP:</span>
                        <span>{new Date().toISOString().split('T')[1].slice(0, 8)}</span>
                      </div>
                      <div className="data-row" style={{ border: 'none' }}>
                        <span>RISK_FACTORS:</span>
                        <span>{result.risky_keywords.length} DETECTED</span>
                      </div>
                      
                      <div className="tag-list">
                        {result.risky_keywords.map((kw, i) => (
                          <span key={i} className="tag">{kw}</span>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '300px', flexDirection: 'column', color: 'var(--text-dim)' }}>
                    <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⚠️</div>
                    <p style={{ textAlign: 'center', fontSize: '0.8rem' }}>WAITING FOR SYSTEM INPUT...<br/>CORE SCANNER IDLE</p>
                  </div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>

        {/* Audit Log / History */}
        <motion.div 
          className="log-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="status-bar" style={{ marginBottom: '1.5rem' }}>
            <span><span className="pulse"></span> SYSTEM_AUDIT_LOG</span>
            <span>TOTAL_ANALYSES: {history.length}</span>
          </div>
          <table className="log-table">
            <thead>
              <tr>
                <th className="log-header" style={{ width: '60%' }}>CONTENT_PREVIEW</th>
                <th className="log-header">LEVEL</th>
                <th className="log-header">SCORE</th>
                <th className="log-header">FLAGS</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id} className="log-row">
                  <td className="log-cell active" style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '300px' }}>
                    {item.content}
                  </td>
                  <td className="log-cell" style={{ color: getThreatColor(item.label) }}>
                    {item.label.toUpperCase()}
                  </td>
                  <td className="log-cell active">{item.score}</td>
                  <td className="log-cell">
                    {item.risky_keywords ? item.risky_keywords.split(',').filter(k => k).length : 0}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </div>
    </>
  );
}

export default App;
