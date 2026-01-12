/**
 * Score badge component with color coding
 */
export default function ScoreBadge({ score, size = 'sm' }) {
  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-400 bg-green-500/20 border-green-500/30';
    if (score >= 70) return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
    if (score >= 50) return 'text-orange-400 bg-orange-500/20 border-orange-500/30';
    return 'text-red-400 bg-red-500/20 border-red-500/30';
  };

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  };

  return (
    <div className={`inline-flex items-center rounded-full font-medium border ${getScoreColor(score)} ${sizeClasses[size]}`}>
      {score}/100
    </div>
  );
}
