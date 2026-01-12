/**
 * Premium stat card with icon, value, label, and trend
 */
export default function StatCard({ icon, value, label, trend, color = 'cyan' }) {
  const colorClasses = {
    cyan: 'from-cyan-500/20 to-cyan-600/20 border-cyan-500/30 text-cyan-400',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30 text-purple-400',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30 text-green-400',
    amber: 'from-amber-500/20 to-amber-600/20 border-amber-500/30 text-amber-400',
  };

  const trendColor = trend?.startsWith('+') ? 'text-green-400' : 'text-red-400';

  return (
    <div className={`bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border ${colorClasses[color]} hover:scale-105 transition-transform duration-200`}>
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center text-2xl`}>
          {icon}
        </div>
        {trend && (
          <span className={`text-sm font-medium ${trendColor}`}>
            {trend}
          </span>
        )}
      </div>

      <div className="space-y-1">
        <div className="text-3xl font-bold text-white">{value}</div>
        <div className="text-slate-400 text-sm">{label}</div>
      </div>

      {/* Mini chart hint */}
      <div className="mt-4 flex space-x-1">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className={`h-2 w-2 rounded-sm ${colorClasses[color]}`}
            style={{ opacity: 0.3 + (i * 0.15) }}
          />
        ))}
      </div>
    </div>
  );
}
