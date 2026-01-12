'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useParams } from 'next/navigation';
import Link from 'next/link';

import ScoreBadge from '@/components/ScoreBadge';
import UnlockModal from '@/components/UnlockModal';
import Tabs from '@/components/Tabs';
import { getLead } from '@/lib/leadService';

export default function LeadDetail() {
  const params = useParams();
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [showUnlockModal, setShowUnlockModal] = useState(false);

  const { data: lead, isLoading } = useQuery({
    queryKey: ['lead', params.id],
    queryFn: () => getLead(params.id),
    enabled: !!params.id,
  });

  const handleUnlock = () => {
    setIsUnlocked(true);
  };

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="animate-pulse">
          <div className="h-8 bg-slate-700 rounded w-64 mb-4"></div>
          <div className="h-4 bg-slate-700 rounded w-96 mb-8"></div>
          <div className="h-32 bg-slate-700 rounded mb-8"></div>
        </div>
      </div>
    );
  }

  if (!lead) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">❌</div>
        <h2 className="text-2xl font-bold text-white mb-4">Lead not found</h2>
        <Link
          href="/"
          className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg transition-colors"
        >
          Back to Lead Feed
        </Link>
      </div>
    );
  }

  const companyInitials = lead.company.split(' ').map(word => word[0]).join('').toUpperCase();

  const tabs = [
    {
      label: 'Email',
      content: (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Subject</label>
            <div className="bg-slate-800/50 p-3 rounded-lg text-white">
              {isUnlocked ? `Intent Signal: ${lead.intentSignal}` : '🔒 Unlock to reveal subject line'}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Body</label>
            <div className="bg-slate-800/50 p-4 rounded-lg text-white min-h-32">
              {isUnlocked ? (
                <div className="whitespace-pre-wrap">{lead.customPitch}</div>
              ) : (
                <div className="text-slate-400">
                  🔒 Unlock to reveal personalized pitch content
                </div>
              )}
            </div>
          </div>
          <div className="flex space-x-3">
            <button
              disabled={!isUnlocked}
              className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 text-white rounded-lg transition-colors"
            >
              📋 Copy
            </button>
            <button className="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg transition-colors">
              🔄 Regenerate
            </button>
          </div>
        </div>
      )
    },
    {
      label: 'LinkedIn DM',
      content: (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Message</label>
            <div className="bg-slate-800/50 p-4 rounded-lg text-white min-h-32">
              {isUnlocked ? (
                <div className="whitespace-pre-wrap">{lead.customPitch}</div>
              ) : (
                <div className="text-slate-400">
                  🔒 Unlock to reveal personalized message
                </div>
              )}
            </div>
          </div>
          <div className="flex space-x-3">
            <button
              disabled={!isUnlocked}
              className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 text-white rounded-lg transition-colors"
            >
              📋 Copy
            </button>
            <button className="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg transition-colors">
              🔄 Regenerate
            </button>
          </div>
        </div>
      )
    }
  ];

  return (
    <div className="space-y-8">
      {/* Back Button */}
      <Link
        href="/"
        className="inline-flex items-center space-x-2 text-slate-400 hover:text-white transition-colors"
      >
        <span>←</span>
        <span>Back to Lead Feed</span>
      </Link>

      {/* Lead Hero */}
      <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-8 border border-slate-800/50">
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-gradient-to-br from-slate-600 to-slate-700 rounded-xl flex items-center justify-center text-white font-bold text-2xl">
              {companyInitials}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">{lead.company}</h1>
              <div className="flex items-center space-x-4 text-sm text-slate-400">
                <span className="flex items-center space-x-2">
                  <span>🏷️</span>
                  <span>{lead.trigger}</span>
                </span>
                <span className="flex items-center space-x-2">
                  <span>🌐</span>
                  <span className="capitalize">{lead.source}</span>
                </span>
                <span className="flex items-center space-x-2">
                  <span>📅</span>
                  <span>{new Date(lead.createdAt).toLocaleDateString()}</span>
                </span>
              </div>
            </div>
          </div>

          <div className="text-right">
            <div className="text-4xl font-bold text-white mb-2">{lead.intentScore}/100</div>
            <ScoreBadge score={lead.intentScore} size="lg" />
          </div>
        </div>

        {/* Quick Actions */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => window.open(lead.evidenceUrl, '_blank')}
            className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 hover:text-white rounded-lg transition-colors"
          >
            📄 Open Evidence
          </button>
          <button
            disabled={!isUnlocked}
            onClick={() => isUnlocked && navigator.clipboard.writeText(lead.customPitch)}
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 text-white rounded-lg transition-colors"
          >
            📋 Copy Pitch
          </button>
          {!isUnlocked && (
            <button
              onClick={() => setShowUnlockModal(true)}
              className="px-6 py-2 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105"
            >
              🔓 Unlock with Nevermined
            </button>
          )}
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-6">
          {/* Inferred Pain Point */}
          <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
            <h2 className="text-xl font-semibold text-white mb-4">Inferred Pain Point</h2>
            <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-4">
              <p className="text-amber-300">{lead.inferredPain}</p>
            </div>
          </div>

          {/* Intent Signal */}
          <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
            <h2 className="text-xl font-semibold text-white mb-4">Intent Signal</h2>
            <p className="text-slate-300">{lead.intentSignal}</p>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Evidence */}
          <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
            <h2 className="text-xl font-semibold text-white mb-4">Evidence</h2>
            {lead.evidenceUrl ? (
              <div className="space-y-3">
                <a
                  href={lead.evidenceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block p-3 bg-slate-800/50 hover:bg-slate-700/50 rounded-lg transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-cyan-400">🔗</span>
                    <span className="text-slate-300 hover:text-white">View Source</span>
                  </div>
                </a>
              </div>
            ) : (
              <p className="text-slate-400">No evidence links available</p>
            )}
          </div>
        </div>
      </div>

      {/* Generate Outreach */}
      <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50">
        <h2 className="text-xl font-semibold text-white mb-6">Generate Outreach</h2>

        {isUnlocked ? (
          <Tabs tabs={tabs} />
        ) : (
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold text-white mb-2">Pitch Content Locked</h3>
            <p className="text-slate-400 mb-6">
              This pitch is generated by agents. Unlock to reveal personalized outreach content.
            </p>
            <button
              onClick={() => setShowUnlockModal(true)}
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105"
            >
              🔓 Unlock with Nevermined
            </button>
          </div>
        )}

        {/* Agent Notes */}
        <div className="mt-6 p-4 bg-slate-800/30 rounded-lg">
          <details className="group">
            <summary className="text-slate-300 cursor-pointer hover:text-white flex items-center space-x-2">
              <span>🤖</span>
              <span>Agent Notes</span>
              <span className="text-xs text-slate-500 group-open:rotate-90 transition-transform">▶</span>
            </summary>
            <div className="mt-3 text-sm text-slate-400">
              <p>This pitch was crafted based on the company's {lead.trigger.toLowerCase()} activity and {lead.inferredPain.toLowerCase()}. The messaging focuses on their specific pain points while positioning your solution as the ideal fit.</p>
            </div>
          </details>
        </div>
      </div>

      {/* Unlock Modal */}
      <UnlockModal
        isOpen={showUnlockModal}
        onClose={() => setShowUnlockModal(false)}
        onUnlock={handleUnlock}
        price="1 credit"
      />
    </div>
  );
}
