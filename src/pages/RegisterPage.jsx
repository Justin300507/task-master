import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api';
import { Mail, Lock, User } from 'lucide-react';

const parseError = err => {
  if (!err.response) return null;
  const detail = err.response?.data?.detail;
  if (!detail) return 'Something went wrong. Please try again.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map(d => d.msg).join(', ');
  return 'Something went wrong. Please try again.';
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

const RegisterPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    setLoading(true);
    setError('');
    setStatus('');
    try {
      await API.post('/auth/signup', { email, password, full_name: fullName });
      const loginRes = await API.post('/auth/login', { email, password });
      localStorage.setItem('token', loginRes.data.access_token);
      if (loginRes.data.display_name) localStorage.setItem('display_name', loginRes.data.display_name);
      if (loginRes.data.user_id) localStorage.setItem('user_id', String(loginRes.data.user_id));
      if (loginRes.data.email) localStorage.setItem('user_email', loginRes.data.email);
      navigate('/dashboard');
    } catch (err) {
      const msg = parseError(err);
      if (msg) setError(msg);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 mx-auto mb-3 flex items-center justify-center">
            <span className="text-white font-bold text-xl">A</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Create account</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">Start managing your tasks</p>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 space-y-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1">
              <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Full Name</label>
              <div className="flex items-center border border-slate-300 dark:border-slate-600 rounded">
                <User size={16} className="ml-2 text-slate-400" />
                <input
                  type="text"
                  value={fullName}
                  onChange={e => setFullName(e.target.value)}
                  placeholder="e.g. Alex Chen"
                  className="flex-1 py-2 px-2 bg-transparent focus:outline-none"
                />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Email</label>
              <div className="flex items-center border border-slate-300 dark:border-slate-600 rounded">
                <Mail size={16} className="ml-2 text-slate-400" />
                <input
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="flex-1 py-2 px-2 bg-transparent focus:outline-none"
                />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Password</label>
              <div className="flex items-center border border-slate-300 dark:border-slate-600 rounded">
                <Lock size={16} className="ml-2 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="flex-1 py-2 px-2 bg-transparent focus:outline-none"
                />
              </div>
              <p className="text-xs text-slate-400">Must be at least 8 characters</p>
            </div>
            {status && <p className="text-xs text-indigo-600">{status}</p>}
            {error && <p className="text-xs text-red-600">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full justify-center flex items-center gap-1.5"
            >
              {loading ? 'Creating...' : 'Create Account'}
            </button>
          </form>
        </div>
        <p className="text-center text-sm text-slate-500 mt-4">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-600 font-medium hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
