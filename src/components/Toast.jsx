const Toast = ({ toast }) => {
  if (!toast) return null;
  return (
    <div
      className={`fixed bottom-4 right-4 px-4 py-3 rounded-xl shadow-lg text-sm font-medium text-white z-50 ${
        toast.type === 'success' ? 'bg-emerald-600' : 'bg-red-600'
      }`}
    >
      {toast.msg}
    </div>
  );
};

export default Toast;
