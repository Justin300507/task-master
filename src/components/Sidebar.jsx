import { NavLink } from 'react-router-dom';
import { LayoutDashboard, ListTodo, CheckSquare, Settings } from 'lucide-react';

const Sidebar = () => (
  <aside className="w-56 bg-slate-900 text-slate-200 flex flex-col px-3 py-4 fixed h-full">
    <div className="flex items-center gap-2 px-2 mb-6">
      <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
        <span className="text-white text-sm font-bold">A</span>
      </div>
      <span className="font-bold text-white text-sm">AppName</span>
    </div>
    <nav className="flex-1 space-y-0.5">
      <NavLink
        to="/dashboard"
        className={({ isActive }) =>
          `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
            isActive ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
          }`
        }
      >
        <LayoutDashboard size={16} /> Dashboard
      </NavLink>
      <NavLink
        to="/tasks"
        className={({ isActive }) =>
          `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
            isActive ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
          }`
        }
      >
        <CheckSquare size={16} /> Tasks
      </NavLink>
      <NavLink
        to="/lists"
        className={({ isActive }) =>
          `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
            isActive ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
          }`
        }
      >
        <ListTodo size={16} /> Lists
      </NavLink>
      <NavLink
        to="/settings"
        className={({ isActive }) =>
          `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
            isActive ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
          }`
        }
      >
        <Settings size={16} /> Settings
      </NavLink>
    </nav>
  </aside>
);

export default Sidebar;
