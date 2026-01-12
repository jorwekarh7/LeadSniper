import { useEffect } from 'react';

/**
 * Simple toast notification component
 */
export default function Toast({ message, type = 'success', isVisible, onClose, duration = 3000 }) {
  useEffect(() => {
    if (isVisible && duration > 0) {
      const timer = setTimeout(() => {
        onClose?.();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [isVisible, duration, onClose]);

  if (!isVisible) return null;

  const typeStyles = {
    success: 'bg-green-500/20 border-green-500/30 text-green-400',
    error: 'bg-red-500/20 border-red-500/30 text-red-400',
    info: 'bg-cyan-500/20 border-cyan-500/30 text-cyan-400',
    warning: 'bg-amber-500/20 border-amber-500/30 text-amber-400',
  };

  const icons = {
    success: '✅',
    error: '❌',
    info: 'ℹ️',
    warning: '⚠️',
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className={`${typeStyles[type]} backdrop-blur-md rounded-lg p-4 border flex items-center space-x-3 max-w-md shadow-lg`}>
        <span className="text-lg">{icons[type]}</span>
        <p className="text-sm font-medium flex-1">{message}</p>
        <button
          onClick={onClose}
          className="text-current hover:opacity-70 transition-opacity"
        >
          ✕
        </button>
      </div>
    </div>
  );
}
