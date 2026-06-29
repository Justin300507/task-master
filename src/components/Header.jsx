import { Sun, Moon } from 'lucide-react';
import { useState, useEffect } from 'react';

const Header = () => {
  const [dark, setDark] = useState(document.documentElement.classList.contains('dark'));
  const displayName = localStorage.getItem('display_name') || 'User';
  const today = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);
  return (
    <header className="flex justify-between items-center px-4 py-2 border-b border-slate-100 dark:border-slate-700">
      <h1 className="text-xl font-semibold text-slate-900 dark:text-white">Hello, {displayName}</h1>
      <div className="flex items-center gap-4">
        <span className="text-slate-500 dark:text-slate-400">{today}</span>
        <button
          onClick={() => setDark(d => !d)}
          className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
        >
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>
    </header>
  );
};

export default Header;
