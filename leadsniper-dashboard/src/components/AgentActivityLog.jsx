import { useEffect, useState } from 'react';

/**
 * Terminal-style agent run console with progress and logs
 */
export default function AgentActivityLog({ runId, onClose }) {
  const [runStatus, setRunStatus] = useState(null);
  const [dots, setDots] = useState('');

  // Simulate dots animation
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 500);
    return () => clearInterval(interval);
  }, []);

  // Poll for status updates
  useEffect(() => {
    if (!runId) return;

    const pollStatus = () => {
      // In real app, this would call getRunStatus(runId)
      // For now, we'll simulate with a timeout
      setTimeout(() => {
        // Mock status update - in real app this would be from the service
        setRunStatus({
          status: 'running',
          progress: 50,
          steps: [
            { name: 'Signal Scout', status: 'done', log: 'completed - found 12 signals' },
            { name: 'Job Monitor', status: 'done', log: 'completed - found 8 signals' },
            { name: 'Stack Watch', status: 'running', log: `processing data${dots}` },
            { name: 'Intent Ranker', status: 'queued', log: '' },
            { name: 'Pitch Agent', status: 'queued', log: '' }
          ],
          logs: [
            'Agent run started...',
            'Signal Scout completed - found 12 signals',
            'Job Monitor completed - found 8 signals'
          ]
        });
      }, 1000);
    };

    pollStatus();
    const interval = setInterval(pollStatus, 2000);

    return () => clearInterval(interval);
  }, [runId, dots]);

  if (!runStatus) return null;

  const getStatusColor = (status) => {
    switch (status) {
      case 'done': return 'text-green-400';
      case 'running': return 'text-cyan-400';
      case 'queued': return 'text-slate-400';
      default: return 'text-slate-400';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'done': return '✅';
      case 'running': return '⚡';
      case 'queued': return '⏳';
      default: return '⏳';
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-950/95 backdrop-blur-md rounded-xl border border-slate-800/50 w-full max-w-4xl max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-800/50">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center">
              <span className="text-cyan-400">🤖</span>
            </div>
            <div>
              <h3 className="text-white font-semibold text-lg">Agent Run Console</h3>
              <p className="text-slate-400 text-sm">Real-time lead detection in progress</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Progress Bar */}
        <div className="px-6 py-4 border-b border-slate-800/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-white text-sm font-medium">Progress</span>
            <span className="text-cyan-400 text-sm">{runStatus.progress}%</span>
          </div>
          <div className="w-full bg-slate-800/50 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-cyan-500 to-cyan-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${runStatus.progress}%` }}
            />
          </div>
        </div>

        {/* Steps */}
        <div className="px-6 py-4 border-b border-slate-800/50 max-h-64 overflow-y-auto">
          <h4 className="text-white font-medium mb-4">Steps</h4>
          <div className="space-y-3">
            {runStatus.steps.map((step, index) => (
              <div key={index} className="flex items-center space-x-3">
                <span className="text-lg">{getStatusIcon(step.status)}</span>
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-white text-sm font-medium">{step.name}</span>
                    <span className={`text-xs ${getStatusColor(step.status)}`}>
                      {step.status}
                    </span>
                  </div>
                  {step.log && (
                    <p className="text-slate-400 text-xs mt-1">{step.log}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Logs */}
        <div className="px-6 py-4 max-h-48 overflow-y-auto">
          <h4 className="text-white font-medium mb-4">Activity Log</h4>
          <div className="space-y-2 font-mono text-xs">
            {runStatus.logs.map((log, index) => (
              <div key={index} className="text-slate-300">
                <span className="text-slate-500 mr-2">[{new Date().toLocaleTimeString()}]</span>
                {log}
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="px-6 py-4 border-t border-slate-800/50 flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 hover:text-white rounded-lg transition-colors"
          >
            Cancel Run
          </button>
        </div>
      </div>
    </div>
  );
}
