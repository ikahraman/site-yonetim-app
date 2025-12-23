import type { Resident, Due, Expense, Announcement } from '../types';

interface DashboardProps {
  residents: Resident[];
  dues: Due[];
  expenses: Expense[];
  announcements: Announcement[];
}

export function Dashboard({ residents, dues, expenses, announcements }: DashboardProps) {
  const totalResidents = residents.length;
  const pendingDues = dues.filter((d) => d.status === 'pending').length;
  const overdueDues = dues.filter((d) => d.status === 'overdue').length;
  const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);
  const recentAnnouncements = announcements.slice(0, 3);

  const stats = [
    { label: 'Toplam Sakin', value: totalResidents, icon: '👥', color: 'bg-blue-500' },
    { label: 'Bekleyen Aidat', value: pendingDues, icon: '⏳', color: 'bg-yellow-500' },
    { label: 'Gecikmiş Aidat', value: overdueDues, icon: '⚠️', color: 'bg-red-500' },
    { label: 'Toplam Gider', value: `₺${totalExpenses.toLocaleString('tr-TR')}`, icon: '💸', color: 'bg-green-500' },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800 mb-8">Ana Sayfa</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center gap-4">
              <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center text-2xl`}>
                {stat.icon}
              </div>
              <div>
                <p className="text-slate-500 text-sm">{stat.label}</p>
                <p className="text-2xl font-bold text-slate-800">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">📢 Son Duyurular</h2>
          {recentAnnouncements.length > 0 ? (
            <ul className="space-y-4">
              {recentAnnouncements.map((announcement) => (
                <li key={announcement.id} className="border-l-4 border-blue-500 pl-4 py-2">
                  <h3 className="font-medium text-slate-800">{announcement.title}</h3>
                  <p className="text-slate-500 text-sm">{announcement.date}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-500">Henüz duyuru bulunmuyor.</p>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">💰 Son Giderler</h2>
          {expenses.length > 0 ? (
            <ul className="space-y-4">
              {expenses.slice(0, 5).map((expense) => (
                <li key={expense.id} className="flex justify-between items-center py-2 border-b border-slate-100">
                  <div>
                    <p className="font-medium text-slate-800">{expense.description}</p>
                    <p className="text-slate-500 text-sm">{expense.category}</p>
                  </div>
                  <span className="font-semibold text-red-600">-₺{expense.amount.toLocaleString('tr-TR')}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-500">Henüz gider kaydı bulunmuyor.</p>
          )}
        </div>
      </div>
    </div>
  );
}
