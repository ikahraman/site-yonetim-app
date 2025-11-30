import { useState } from 'react';
import type { Resident } from '../types';

interface ResidentsProps {
  residents: Resident[];
  onAddResident: (resident: Omit<Resident, 'id'>) => void;
  onDeleteResident: (id: string) => void;
}

export function Residents({ residents, onAddResident, onDeleteResident }: ResidentsProps) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    apartment: '',
    phone: '',
    email: '',
    moveInDate: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddResident(formData);
    setFormData({ name: '', apartment: '', phone: '', email: '', moveInDate: '' });
    setShowForm(false);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">👥 Sakinler</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          {showForm ? 'İptal' : '+ Yeni Sakin Ekle'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Ad Soyad</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Daire No</label>
              <input
                type="text"
                required
                value={formData.apartment}
                onChange={(e) => setFormData({ ...formData, apartment: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Telefon</label>
              <input
                type="tel"
                required
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">E-posta</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Giriş Tarihi</label>
              <input
                type="date"
                required
                value={formData.moveInDate}
                onChange={(e) => setFormData({ ...formData, moveInDate: e.target.value })}
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
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Ad Soyad</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Daire No</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Telefon</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">E-posta</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Giriş Tarihi</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {residents.map((resident) => (
              <tr key={resident.id} className="border-t border-slate-100 hover:bg-slate-50">
                <td className="px-6 py-4 text-slate-800">{resident.name}</td>
                <td className="px-6 py-4 text-slate-800">{resident.apartment}</td>
                <td className="px-6 py-4 text-slate-600">{resident.phone}</td>
                <td className="px-6 py-4 text-slate-600">{resident.email}</td>
                <td className="px-6 py-4 text-slate-600">{resident.moveInDate}</td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => onDeleteResident(resident.id)}
                    className="text-red-600 hover:text-red-800 transition-colors"
                  >
                    Sil
                  </button>
                </td>
              </tr>
            ))}
            {residents.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                  Henüz sakin kaydı bulunmuyor.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
