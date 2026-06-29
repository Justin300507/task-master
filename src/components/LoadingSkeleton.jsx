const LoadingSkeleton = () => (
  <div className="animate-pulse space-y-3">
    {[...Array(5)].map((_, i) => (
      <div key={i} className="h-16 bg-slate-200 dark:bg-slate-700 rounded-xl" />
    ))}
  </div>
);

export default LoadingSkeleton;
