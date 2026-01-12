import { useState } from 'react';

/**
 * Controls toolbar with search, filters, and Run Scrape button
 */
export default function FiltersBar({ onRunScrape }) {
  const [search, setSearch] = useState('');
  const [trigger, setTrigger] = useState('All');
  const [source, setSource] = useState('all');
  const [scoreFilter, setScoreFilter] = useState('0+');
  const [dateRange, setDateRange] = useState('Last 24h');

  const handleRunScrape = () => {
    onRunScrape?.(trigger, source);
  };

  return (
    <div className="bg-slate-900/30 backdrop-blur-md rounded-xl p-6 border border-slate-800/50 mb-8">
      <div className="flex flex-wrap gap-4 items-center">
        {/* Search */}
        <div className="flex-1 min-w-64">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span className="text-slate-400">🔍</span>
            </div>
            <input
              type="text"
              placeholder="Search company, trigger, pain..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
            />
          </div>
        </div>

        {/* Trigger Dropdown */}
        <select
          value={trigger}
          onChange={(e) => setTrigger(e.target.value)}
          className="px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
        >
          <option value="All">All Triggers</option>
          <option value="Job Posting">Job Posting</option>
          <option value="Reddit Intent">Reddit Intent</option>
          <option value="Tech Change">Tech Change</option>
          <option value="LinkedIn Signal">LinkedIn Signal</option>
        </select>

        {/* Source Dropdown */}
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
        >
          <option value="all">All Sources</option>
          <option value="reddit">Reddit</option>
          <option value="linkedin">LinkedIn</option>
          <option value="jobs">Jobs</option>
          <option value="other">Other</option>
        </select>

        {/* Score Filter */}
        <select
          value={scoreFilter}
          onChange={(e) => setScoreFilter(e.target.value)}
          className="px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
        >
          <option value="0+">Score: 0+</option>
          <option value="50+">Score: 50+</option>
          <option value="70+">Score: 70+</option>
          <option value="85+">Score: 85+</option>
        </select>

        {/* Date Range */}
        <select
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
        >
          <option value="Last 24h">Last 24h</option>
          <option value="Last 7d">Last 7d</option>
          <option value="Last 30d">Last 30d</option>
        </select>

        {/* Run Scrape Button */}
        <button
          onClick={handleRunScrape}
          className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-cyan-600 hover:from-cyan-600 hover:to-cyan-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/25"
        >
          🚀 Run Scrape
        </button>
      </div>
    </div>
  );
}
