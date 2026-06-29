import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import TaskListPage from './pages/TaskListPage';
import ListManagementPage from './pages/ListManagementPage';
import SettingsPage from './pages/SettingsPage';
import Header from './components/Header';
import Sidebar from './components/Sidebar';

const PrivateRoute = ({ children }) => {
  return localStorage.getItem('token') ? children : <Navigate to="/login" replace />;
};

const Layout = ({ children }) => (
  <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
    <Sidebar />
    <div className="ml-56 flex-1 flex flex-col">
      <Header />
      <main className="flex-1 p-6 overflow-auto">{children}</main>
    </div>
  </div>
);

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Layout>
              <DashboardPage />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/tasks"
        element={
          <PrivateRoute>
            <Layout>
              <TaskListPage />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/lists"
        element={
          <PrivateRoute>
            <Layout>
              <ListManagementPage />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <PrivateRoute>
            <Layout>
              <SettingsPage />
            </Layout>
          </PrivateRoute>
        }
      />
    </Routes>
  </BrowserRouter>
);

export default App;
