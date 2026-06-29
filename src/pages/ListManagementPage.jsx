import { useEffect, useState } from 'react';
import { Search, Plus, ListTodo } from 'lucide-react';
import API from '../api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import { Link } from 'react-router-dom';

const ListManagementPage = () => {
  const [lists, setLists] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const fetchLists = async () => {
      try {
        const res = await API.get('/lists');
        const items = res.data.items || [];
        setLists(items);
        setFiltered(items);
      } catch (e) {
        setToast({ msg: 'Failed to load lists', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchLists();
  }, []);

  useEffect(() => {
    const lower = search.toLowerCase();
    setFiltered(lists.filter(l => l.name.toLowerCase().includes(lower)));
  }, [search, lists]);

  return (
    <div className="space-y-4">
      <Toast toast={toast} />
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Lists</h2>
        <Link to="/lists/new" className="btn-primary flex items-center gap-1.5">
          <Plus size={16} /> Add List
        </Link>
      </div>
      <div className="flex items-center gap-2 bg-white dark:bg-slate-800 rounded-md px-3 py-2 border border-slate-100 dark:border-slate-700">
        <Search size={16} className="text-slate-400" />
        <input
          type="text"
          placeholder="Search lists..."
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
          {filtered.map(list => (
            <div key={list.id} className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
                  <ListTodo size={18} className="text-indigo-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900 dark:text-white">{list.name}</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Owner ID: {list.owner_id}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ListManagementPage;
