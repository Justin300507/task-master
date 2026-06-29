import { useEffect, useState } from 'react';
import API from '../api';
import StatCard from '../components/StatCard';
import { Users, ListTodo, CheckSquare, Layers } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import TaskCard from '../components/TaskCard';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';

const DashboardPage = () => {
  const [summary, setSummary] = useState({ users: 0, lists: 0, tasks: 0, tags: 0 });
  const [recentTasks, setRecentTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await API.get('/stats/summary');
        setSummary(res.data);
        const tasksRes = await API.get('/tasks', { params: { limit: 5, sort: '-created_at' } });
        setRecentTasks(tasksRes.data.items || []);
      } catch (e) {
        setToast({ msg: 'Failed to load dashboard data', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const chartData = [
    { month: 'Jan', total: 840 },
    { month: 'Feb', total: 720 },
    { month: 'Mar', total: 1100 },
    { month: 'Apr', total: 890 },
    { month: 'May', total: 1240 },
    { month: 'Jun', total: 980 },
  ];

  return (
    <div className="space-y-6">
      <Toast toast={toast} />
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Dashboard</h2>
        <p className="text-slate-500 dark:text-slate-400">{new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' })}</p>
      </div>
      {loading ? (
        <LoadingSkeleton />
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              label="Users"
              value={summary.users}
              icon={<Users size={18} className="text-indigo-600 dark:text-indigo-400" />}
            />
            <StatCard
              label="Lists"
              value={summary.lists}
              icon={<Layers size={18} className="text-indigo-600 dark:text-indigo-400" />}
            />
            <StatCard
              label="Tasks"
              value={summary.tasks}
              icon={<CheckSquare size={18} className="text-indigo-600 dark:text-indigo-400" />}
            />
            <StatCard
              label="Tags"
              value={summary.tags}
              icon={<ListTodo size={18} className="text-indigo-600 dark:text-indigo-400" />}
            />
          </div>
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-5">
            <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Monthly Overview</h3>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '8px', color: '#f1f5f9' }} />
                <Area type="monotone" dataKey="total" stroke="#6366f1" strokeWidth={2} fill="url(#colorTotal)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Recent Tasks</h3>
            {recentTasks.length === 0 ? (
              <p className="text-slate-500 dark:text-slate-400">No recent tasks.</p>
            ) : (
              <div className="space-y-3">
                {recentTasks.map(task => (
                  <TaskCard key={task.id} task={task} onToggle={() => {}} />
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default DashboardPage;
