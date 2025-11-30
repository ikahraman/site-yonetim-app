import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Ana Sayfa', icon: '🏠' },
  { path: '/residents', label: 'Sakinler', icon: '👥' },
  { path: '/dues', label: 'Aidatlar', icon: '💰' },
  { path: '/expenses', label: 'Giderler', icon: '📊' },
  { path: '/announcements', label: 'Duyurular', icon: '📢' },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-slate-800 text-white min-h-screen p-4">
      <div className="mb-8">
        <h1 className="text-xl font-bold text-center">🏢 Site Yönetimi</h1>
      </div>
      <nav>
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'hover:bg-slate-700 text-slate-300'
                  }`
                }
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
