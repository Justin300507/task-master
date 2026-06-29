import { CheckSquare } from 'lucide-react';

const StatCard = ({ label, value, change, icon }) => (
  <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-100 dark:border-slate-700 shadow-sm">
    <div className="flex items-center justify-between mb-3">
      <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">{label}</p>
      <div className="bg-indigo-50 dark:bg-indigo-900/30 p-2 rounded-lg">
        {icon || <CheckSquare size={18} className="text-indigo-600 dark:text-indigo-400" />}
      </div>
    </div>
    <p className="text-2xl font-bold text-slate-900 dark:text-white">{value}</p>
    {change && (
      <p className="text-xs text-indigo-600 mt-1 flex items-center gap-1">
        {change}
      </p>
    )}
  </div>
);

export default StatCard;
