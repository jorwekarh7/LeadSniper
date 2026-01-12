import { useState } from 'react';

/**
 * Simple custom tabs component
 */
export default function Tabs({ tabs, defaultTab = 0, onTabChange }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  const handleTabClick = (index) => {
    setActiveTab(index);
    onTabChange?.(index);
  };

  return (
    <div>
      {/* Tab Headers */}
      <div className="flex space-x-1 mb-6 bg-slate-900/50 p-1 rounded-lg">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => handleTabClick(index)}
            className={`flex-1 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
              activeTab === index
                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div>
        {tabs[activeTab]?.content}
      </div>
    </div>
  );
}
