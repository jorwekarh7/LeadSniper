import Link from 'next/link';

/**
 * Premium lead card with hover effects
 */
export default function LeadCard({ lead }) {
  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-400 bg-green-500/20 border-green-500/30';
    if (score >= 70) return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
    if (score >= 50) return 'text-orange-400 bg-orange-500/20 border-orange-500/30';
    return 'text-red-400 bg-red-500/20 border-red-500/30';
  };

  const getSourceIcon = (source) => {
    switch (source) {
      case 'reddit': return '🟠';
      case 'linkedin': return '💼';
      case 'jobs': return '💼';
      default: return '🌐';
    }
  };

  const companyInitials = lead.company.split(' ').map(word => word[0]).join('').toUpperCase();

  return (
    <Link href={`/leads/${lead.id}`}>
      <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50 hover:border-cyan-500/30 hover:shadow-lg hover:shadow-cyan-500/10 transition-all duration-300 transform hover:scale-105 cursor-pointer group">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-slate-600 to-slate-700 rounded-lg flex items-center justify-center text-white font-bold text-sm">
              {companyInitials}
            </div>
            <div>
              <h3 className="text-white font-semibold text-lg">{lead.company}</h3>
              <div className="flex items-center space-x-2 text-sm text-slate-400">
                <span>{lead.trigger}</span>
                <span>•</span>
                <span className="flex items-center space-x-1">
                  <span>{getSourceIcon(lead.source)}</span>
                  <span className="capitalize">{lead.source}</span>
                </span>
              </div>
            </div>
          </div>

          {/* Score Badge */}
          <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getScoreColor(lead.intentScore)}`}>
            {lead.intentScore}/100
          </div>
        </div>

        {/* Intent Signal */}
        <p className="text-slate-300 text-sm mb-4 line-clamp-2">
          {lead.intentSignal}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {lead.evidenceUrl && (
              <span className="text-xs text-slate-400 hover:text-cyan-400 cursor-pointer">
                📄 Evidence
              </span>
            )}
          </div>

          <div className="flex items-center space-x-2 text-slate-400 group-hover:text-cyan-400 transition-colors">
            <span className="text-sm">View details</span>
            <span className="text-lg transform group-hover:translate-x-1 transition-transform">→</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
