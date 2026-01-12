'use client';

import { useState } from 'react';
import PageHeader from '../../components/PageHeader';
import Toast from '../../components/Toast';
import { setMockMode } from '../../lib/leadService';

export default function Settings() {
  const [backendUrl, setBackendUrl] = useState('http://localhost:8000');
  const [mockMode, setMockModeState] = useState(true);
  const [accentTheme, setAccentTheme] = useState('cyan');
  const [toast, setToast] = useState({ visible: false, message: '', type: 'success' });

  const handleTestConnection = async () => {
    try {
      // Mock connection test
      setToast({ visible: true, message: 'Connection test successful (mock)', type: 'success' });
    } catch (error) {
      setToast({ visible: true, message: 'Connection failed', type: 'error' });
    }
  };

  const handleMockModeChange = (enabled) => {
    setMockModeState(enabled);
    setMockMode(enabled);
    setToast({
      visible: true,
      message: enabled ? 'Mock mode enabled' : 'Mock mode disabled',
      type: 'info'
    });
  };

  const handleCloseToast = () => {
    setToast({ ...toast, visible: false });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <PageHeader
        title="Settings"
        subtitle="Configure your LeadSniper dashboard"
        status="Mock Mode"
      />

      {/* Settings Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Backend Configuration */}
        <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
          <h2 className="text-xl font-semibold text-white mb-6">Backend Configuration</h2>

          <div className="space-y-6">
            {/* Backend URL */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Backend URL
              </label>
              <input
                type="text"
                value={backendUrl}
                onChange={(e) => setBackendUrl(e.target.value)}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                placeholder="http://localhost:8000"
              />
              <p className="text-xs text-slate-400 mt-1">
                URL of your LeadSniper backend API
              </p>
            </div>

            {/* Test Connection */}
            <button
              onClick={handleTestConnection}
              className="w-full px-4 py-3 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold rounded-lg transition-colors"
            >
              🔗 Test Connection
            </button>
          </div>
        </div>

        {/* Mode Settings */}
        <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
          <h2 className="text-xl font-semibold text-white mb-6">Mode Settings</h2>

          <div className="space-y-6">
            {/* Mock Mode Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-white font-medium">Mock Mode</h3>
                <p className="text-sm text-slate-400">
                  Use mock data instead of real API calls
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={mockMode}
                  onChange={(e) => handleMockModeChange(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-cyan-500/25 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-500"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Theme Settings */}
        <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
          <h2 className="text-xl font-semibold text-white mb-6">Theme Settings</h2>

          <div className="space-y-6">
            {/* Accent Theme */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-3">
                Accent Theme
              </label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { value: 'cyan', label: 'Cyan', color: 'from-cyan-500 to-cyan-600' },
                  { value: 'purple', label: 'Purple', color: 'from-purple-500 to-purple-600' },
                ].map((theme) => (
                  <button
                    key={theme.value}
                    onClick={() => setAccentTheme(theme.value)}
                    className={`p-4 rounded-lg border transition-all ${
                      accentTheme === theme.value
                        ? `bg-gradient-to-r ${theme.color} border-white/30`
                        : 'bg-slate-800/50 border-slate-700/50 hover:bg-slate-700/50'
                    }`}
                  >
                    <div className={`w-full h-8 rounded bg-gradient-to-r ${theme.color} mb-2`}></div>
                    <span className={`text-sm font-medium ${
                      accentTheme === theme.value ? 'text-white' : 'text-slate-300'
                    }`}>
                      {theme.label}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
          <h2 className="text-xl font-semibold text-white mb-6">System Info</h2>

          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-slate-400">Version</span>
              <span className="text-white">v1.0.0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">React Query</span>
              <span className="text-white">v5.x</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Next.js</span>
              <span className="text-white">16.x</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Tailwind CSS</span>
              <span className="text-white">v4.x</span>
            </div>
          </div>
        </div>
      </div>

      {/* Toast */}
      <Toast
        message={toast.message}
        type={toast.type}
        isVisible={toast.visible}
        onClose={handleCloseToast}
      />
    </div>
  );
}
