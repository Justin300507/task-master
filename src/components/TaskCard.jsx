import { CheckSquare } from 'lucide-react';
import { useState } from 'react';
import API from '../api';

const TaskCard = ({ task, onToggle }) => {
  const [loading, setLoading] = useState(false);
  const handleToggle = async () => {
    setLoading(true);
    try {
      await API.patch(`/tasks/${task.id}/complete`);
      onToggle && onToggle(task.id);
    } catch (e) {}
    setLoading(false);
  };
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
      <div className="flex items-center gap-3">
        <button onClick={handleToggle} disabled={loading} className="w-6 h-6 flex items-center justify-center">
          <CheckSquare size={16} className={task.completed ? 'text-indigo-600' : 'text-slate-400'} />
        </button>
        <div>
          <p className="text-sm font-semibold text-slate-900 dark:text-white">{task.title}</p>
          {task.description && <p className="text-xs text-slate-500 dark:text-slate-400">{task.description}</p>}
          {task.due_date && (
            <p className="text-xs text-slate-400 dark:text-slate-500">
              {new Date(task.due_date).toLocaleDateString()}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
