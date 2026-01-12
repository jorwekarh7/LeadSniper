'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import PageHeader from '../components/PageHeader';
import StatCard from '../components/StatCard';
import FiltersBar from '../components/FiltersBar';
import LeadCard from '../components/LeadCard';
import AgentActivityLog from '../components/AgentActivityLog';
import Skeleton from '../components/Skeleton';
import Toast from '../components/Toast';
import { listLeads } from '../lib/leadService';
import { startRun } from '../lib/agentRunService';

export default function LeadFeed() {
  const [runId, setRunId] = useState(null);
  const [showRunLog, setShowRunLog] = useState(false);
  const [toast, setToast] = useState({ visible: false, message: '', type: 'success' });

  // Fetch leads
  const { data: leads, isLoading, refetch } = useQuery({
    queryKey: ['leads'],
    queryFn: listLeads,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Mock stats - in real app these would come from API
  const stats = [
    { icon: '🎯', value: '24', label: 'Leads Today', trend: '+12%', color: 'cyan' },
    { icon: '📊', value: '76', label: 'Avg Intent Score', trend: '+5%', color: 'green' },
    { icon: '⚡', value: 'Job Posting', label: 'Hot Trigger', color: 'purple' },
    { icon: '🌐', value: 'Reddit', label: 'Top Source', color: 'amber' },
  ];

  const handleRunScrape = async (trigger, source) => {
    try {
      const newRunId = startRun(trigger, source);
      setRunId(newRunId);
      setShowRunLog(true);

      // Show success toast when run completes (mock)
      setTimeout(() => {
        setToast({ visible: true, message: 'Run complete! New leads available.', type: 'success' });
        setShowRunLog(false);
        refetch(); // Refresh leads
      }, 35000); // Match simulation duration
    } catch (error) {
      setToast({ visible: true, message: 'Failed to start run', type: 'error' });
    }
  };

  const handleCloseRunLog = () => {
    setShowRunLog(false);
  };

  const handleCloseToast = () => {
    setToast({ ...toast, visible: false });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <PageHeader
        title="Lead Feed"
        subtitle="Real-time intent signals with agent-driven scoring"
        status="Mock Mode"
      />

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatCard
            key={index}
            icon={stat.icon}
            value={stat.value}
            label={stat.label}
            trend={stat.trend}
            color={stat.color}
          />
        ))}
      </div>

      {/* Filters */}
      <FiltersBar onRunScrape={handleRunScrape} />

      {/* Leads Grid */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-6">Recent Leads</h2>
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} variant="card" />
            ))}
          </div>
        ) : leads && leads.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {leads.map((lead) => (
              <LeadCard key={lead.id} lead={lead} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-white mb-2">No leads found</h3>
            <p className="text-slate-400 mb-6">Run a scrape to discover new leads</p>
            <button
              onClick={() => handleRunScrape('All', 'all')}
              className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-cyan-600 hover:from-cyan-600 hover:to-cyan-700 text-white font-semibold rounded-lg transition-all duration-200"
            >
              🚀 Run Scrape
            </button>
          </div>
        )}
      </div>

      {/* Agent Run Log */}
      <AgentActivityLog
        runId={runId}
        isOpen={showRunLog}
        onClose={handleCloseRunLog}
      />

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
