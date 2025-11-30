import { useState } from 'react';
import type { Expense } from '../types';

interface ExpensesProps {
  expenses: Expense[];
  onAddExpense: (expense: Omit<Expense, 'id'>) => void;
  onDeleteExpense: (id: string) => void;
}

const categories = [
  'Elektrik',
  'Su',
  'Doğalgaz',
  'Temizlik',
  'Güvenlik',
  'Bakım/Onarım',
  'Asansör',
  'Bahçe',
  'Personel',
  'Diğer',
];

export function Expenses({ expenses, onAddExpense, onDeleteExpense }: ExpensesProps) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    description: '',
    category: '',
    amount: '',
    date: '',
    paidBy: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddExpense({
      description: formData.description,
      category: formData.category,
      amount: Number(formData.amount),
      date: formData.date,
      paidBy: formData.paidBy,
    });
    setFormData({ description: '', category: '', amount: '', date: '', paidBy: '' });
    setShowForm(false);
  };

  const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">📊 Giderler</h1>
          <p className="text-slate-500 mt-1">
            Toplam: <span className="font-semibold text-red-600">₺{totalExpenses.toLocaleString('tr-TR')}</span>
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          {showForm ? 'İptal' : '+ Yeni Gider Ekle'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Açıklama</label>
              <input
                type="text"
                required
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Kategori</label>
              <select
                required
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Kategori seçin...</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Tutar (₺)</label>
              <input
                type="number"
                required
                min="0"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Tarih</label>
              <input
                type="date"
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Ödeyen</label>
              <input
                type="text"
                required
                value={formData.paidBy}
                onChange={(e) => setFormData({ ...formData, paidBy: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Kaydet
          </button>
        </form>
      )}

      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Açıklama</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Kategori</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Tutar</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Tarih</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Ödeyen</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((expense) => (
              <tr key={expense.id} className="border-t border-slate-100 hover:bg-slate-50">
                <td className="px-6 py-4 text-slate-800">{expense.description}</td>
                <td className="px-6 py-4">
                  <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm">
                    {expense.category}
                  </span>
                </td>
                <td className="px-6 py-4 text-red-600 font-semibold">₺{expense.amount.toLocaleString('tr-TR')}</td>
                <td className="px-6 py-4 text-slate-600">{expense.date}</td>
                <td className="px-6 py-4 text-slate-600">{expense.paidBy}</td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => onDeleteExpense(expense.id)}
                    className="text-red-600 hover:text-red-800 transition-colors"
                  >
                    Sil
                  </button>
                </td>
              </tr>
            ))}
            {expenses.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                  Henüz gider kaydı bulunmuyor.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
