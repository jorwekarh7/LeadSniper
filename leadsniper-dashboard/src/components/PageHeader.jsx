/**
 * Page header with title, subtitle, and status pill
 */
export default function PageHeader({ title, subtitle, status = 'Mock Mode' }) {
  const isConnected = status === 'Connected';

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">{title}</h1>
          <p className="text-slate-400 text-lg">{subtitle}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
          isConnected
            ? 'bg-green-500/20 text-green-400 border border-green-500/30'
            : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
        }`}>
          {status}
        </div>
      </div>
    </div>
  );
}
