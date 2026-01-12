'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

/**
 * Persistent left sidebar navigation
 */
export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { href: '/', label: 'Lead Feed', icon: '📊' },
    { href: '/settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-slate-950/95 backdrop-blur-md border-r border-slate-800/50 z-40">
      <div className="flex flex-col h-full">
        {/* Logo/Brand */}
        <div className="p-6 border-b border-slate-800/50">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-cyan-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
              LS
            </div>
            <div>
              <h1 className="text-white font-bold text-lg">LeadSniper</h1>
              <p className="text-slate-400 text-xs">AI Lead Detection</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                    pathname === item.href
                      ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                      : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'
                  }`}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800/50">
          <div className="text-xs text-slate-500 text-center">v1.0.0</div>
        </div>
      </div>
    </div>
  );
}
