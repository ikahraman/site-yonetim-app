import { useState } from 'react';
import type { Due, Resident } from '../types';

interface DuesProps {
  dues: Due[];
  residents: Resident[];
  onAddDue: (due: Omit<Due, 'id'>) => void;
  onMarkAsPaid: (id: string) => void;
}

export function Dues({ dues, residents, onAddDue, onMarkAsPaid }: DuesProps) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    residentId: '',
    amount: '',
    dueDate: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const resident = residents.find((r) => r.id === formData.residentId);
    if (!resident) return;

    onAddDue({
      residentId: formData.residentId,
      residentName: resident.name,
      apartment: resident.apartment,
      amount: Number(formData.amount),
      dueDate: formData.dueDate,
      paidDate: null,
      status: 'pending',
    });
    setFormData({ residentId: '', amount: '', dueDate: '' });
    setShowForm(false);
  };

  const getStatusBadge = (status: Due['status']) => {
    const styles = {
      paid: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      overdue: 'bg-red-100 text-red-800',
    };
    const labels = {
      paid: 'Ödendi',
      pending: 'Bekliyor',
      overdue: 'Gecikmiş',
    };
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${styles[status]}`}>
        {labels[status]}
      </span>
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">💰 Aidatlar</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          {showForm ? 'İptal' : '+ Yeni Aidat Ekle'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Sakin</label>
              <select
                required
                value={formData.residentId}
                onChange={(e) => setFormData({ ...formData, residentId: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Sakin seçin...</option>
                {residents.map((resident) => (
                  <option key={resident.id} value={resident.id}>
                    {resident.name} - Daire {resident.apartment}
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
              <label className="block text-sm font-medium text-slate-700 mb-1">Son Ödeme Tarihi</label>
              <input
                type="date"
                required
                value={formData.dueDate}
                onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
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
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Sakin</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Daire No</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Tutar</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Son Ödeme</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Durum</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {dues.map((due) => (
              <tr key={due.id} className="border-t border-slate-100 hover:bg-slate-50">
                <td className="px-6 py-4 text-slate-800">{due.residentName}</td>
                <td className="px-6 py-4 text-slate-800">{due.apartment}</td>
                <td className="px-6 py-4 text-slate-800 font-semibold">₺{due.amount.toLocaleString('tr-TR')}</td>
                <td className="px-6 py-4 text-slate-600">{due.dueDate}</td>
                <td className="px-6 py-4">{getStatusBadge(due.status)}</td>
                <td className="px-6 py-4">
                  {due.status !== 'paid' && (
                    <button
                      onClick={() => onMarkAsPaid(due.id)}
                      className="text-green-600 hover:text-green-800 transition-colors font-medium"
                    >
                      Ödendi İşaretle
                    </button>
                  )}
                </td>
              </tr>
            ))}
            {dues.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                  Henüz aidat kaydı bulunmuyor.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
