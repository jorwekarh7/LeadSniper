/**
 * Loading skeleton component
 */
export default function Skeleton({ className = '', variant = 'card' }) {
  const variants = {
    card: 'bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-slate-800/50',
    text: 'bg-slate-700/50 rounded',
    circle: 'bg-slate-700/50 rounded-full',
  };

  if (variant === 'card') {
    return (
      <div className={`${variants.card} ${className} animate-pulse`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`${variants.circle} w-10 h-10`}></div>
            <div className="space-y-2">
              <div className={`${variants.text} h-4 w-32`}></div>
              <div className={`${variants.text} h-3 w-24`}></div>
            </div>
          </div>
          <div className={`${variants.text} h-6 w-16 rounded-full`}></div>
        </div>
        <div className={`${variants.text} h-3 w-full mb-2`}></div>
        <div className={`${variants.text} h-3 w-3/4 mb-4`}></div>
        <div className="flex justify-between items-center">
          <div className={`${variants.text} h-3 w-16`}></div>
          <div className={`${variants.text} h-3 w-20`}></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`${variants[variant] || variants.text} ${className} animate-pulse`}></div>
  );
}
