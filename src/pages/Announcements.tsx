import { useState } from 'react';
import type { Announcement } from '../types';

interface AnnouncementsProps {
  announcements: Announcement[];
  onAddAnnouncement: (announcement: Omit<Announcement, 'id'>) => void;
  onDeleteAnnouncement: (id: string) => void;
}

export function Announcements({ announcements, onAddAnnouncement, onDeleteAnnouncement }: AnnouncementsProps) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    author: '',
    priority: 'medium' as Announcement['priority'],
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddAnnouncement({
      title: formData.title,
      content: formData.content,
      date: new Date().toLocaleDateString('tr-TR'),
      author: formData.author,
      priority: formData.priority,
    });
    setFormData({ title: '', content: '', author: '', priority: 'medium' });
    setShowForm(false);
  };

  const getPriorityBadge = (priority: Announcement['priority']) => {
    const styles = {
      low: 'bg-green-100 text-green-800',
      medium: 'bg-yellow-100 text-yellow-800',
      high: 'bg-red-100 text-red-800',
    };
    const labels = {
      low: 'Düşük',
      medium: 'Orta',
      high: 'Yüksek',
    };
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${styles[priority]}`}>
        {labels[priority]}
      </span>
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">📢 Duyurular</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          {showForm ? 'İptal' : '+ Yeni Duyuru Ekle'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 gap-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Başlık</label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Yazar</label>
                <input
                  type="text"
                  required
                  value={formData.author}
                  onChange={(e) => setFormData({ ...formData, author: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Öncelik</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value as Announcement['priority'] })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="low">Düşük</option>
                  <option value="medium">Orta</option>
                  <option value="high">Yüksek</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">İçerik</label>
              <textarea
                required
                rows={4}
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Yayınla
          </button>
        </form>
      )}

      <div className="space-y-4">
        {announcements.map((announcement) => (
          <div key={announcement.id} className="bg-white rounded-xl shadow-md p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-semibold text-slate-800">{announcement.title}</h2>
                <div className="flex items-center gap-3 mt-2 text-sm text-slate-500">
                  <span>📅 {announcement.date}</span>
                  <span>✍️ {announcement.author}</span>
                  {getPriorityBadge(announcement.priority)}
                </div>
              </div>
              <button
                onClick={() => onDeleteAnnouncement(announcement.id)}
                className="text-red-500 hover:text-red-700 transition-colors text-sm"
              >
                Sil
              </button>
            </div>
            <p className="text-slate-600 whitespace-pre-wrap">{announcement.content}</p>
          </div>
        ))}
        {announcements.length === 0 && (
          <div className="bg-white rounded-xl shadow-md p-8 text-center text-slate-500">
            Henüz duyuru bulunmuyor.
          </div>
        )}
      </div>
    </div>
  );
}
