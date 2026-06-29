import { useEffect, useState } from 'react';
import { Search, Plus } from 'lucide-react';
import API from '../api';
import TaskCard from '../components/TaskCard';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import { Link } from 'react-router-dom';

const TaskListPage = () => {
  const [tasks, setTasks] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await API.get('/tasks');
        const items = res.data.items || [];
        setTasks(items);
        setFiltered(items);
      } catch (e) {
        setToast({ msg: 'Failed to load tasks', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  useEffect(() => {
    const lower = search.toLowerCase();
    setFiltered(tasks.filter(t => t.title.toLowerCase().includes(lower) || (t.description && t.description.toLowerCase().includes(lower))));
  }, [search, tasks]);

  const handleToggle = id => {
    setTasks(prev => prev.map(t => (t.id === id ? { ...t, completed: !t.completed } : t)));
  };

  return (
    <div className="space-y-4">
      <Toast toast={toast} />
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Tasks</h2>
        <Link to="/tasks/new" className="btn-primary flex items-center gap-1.5">
          <Plus size={16} /> Add Task
        </Link>
      </div>
      <div className="flex items-center gap-2 bg-white dark:bg-slate-800 rounded-md px-3 py-2 border border-slate-100 dark:border-slate-700">
        <Search size={16} className="text-slate-400" />
        <input
          type="text"
          placeholder="Search tasks..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="flex-1 bg-transparent focus:outline-none text-slate-900 dark:text-white"
        />
      </div>
      {loading ? (
        <LoadingSkeleton />
      ) : filtered.length === 0 ? (
        <div className="text-center py-10 text-slate-500 dark:text-slate-400">
          <Search size={48} className="mx-auto mb-4" />
          <p>No results found</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(task => (
            <TaskCard key={task.id} task={task} onToggle={handleToggle} />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskListPage;
