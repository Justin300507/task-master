import { useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { useState } from 'react';
import Toast from '../components/Toast';

const SettingsPage = () => {
  const navigate = useNavigate();
  const [toast, setToast] = useState(null);

  const handleLogout = () => {
    ['token','display_name','user_id','user_email'].forEach(k => localStorage.removeItem(k));
    setToast({ msg: 'Logged out', type: 'success' });
    setTimeout(() => navigate('/login'), 500);
  };

  return (
    <div className="space-y-6">
      <Toast toast={toast} />
      <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Settings</h2>
      <button onClick={handleLogout} className="btn-primary flex items-center gap-1.5">
        <LogOut size={16} /> Log Out
      </button>
    </div>
  );
};

export default SettingsPage;
