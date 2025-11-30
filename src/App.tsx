import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components';
import { Dashboard, Residents, Dues, Expenses, Announcements } from './pages';
import type { Resident, Due, Expense, Announcement } from './types';

// Sample data
const initialResidents: Resident[] = [
  { id: '1', name: 'Ahmet Yılmaz', apartment: '1', phone: '0532 123 4567', email: 'ahmet@email.com', moveInDate: '2020-01-15' },
  { id: '2', name: 'Fatma Demir', apartment: '2', phone: '0533 234 5678', email: 'fatma@email.com', moveInDate: '2019-06-20' },
  { id: '3', name: 'Mehmet Kaya', apartment: '3', phone: '0534 345 6789', email: 'mehmet@email.com', moveInDate: '2021-03-10' },
];

const initialDues: Due[] = [
  { id: '1', residentId: '1', residentName: 'Ahmet Yılmaz', apartment: '1', amount: 500, dueDate: '2024-01-15', paidDate: '2024-01-10', status: 'paid' },
  { id: '2', residentId: '2', residentName: 'Fatma Demir', apartment: '2', amount: 500, dueDate: '2024-01-15', paidDate: null, status: 'pending' },
  { id: '3', residentId: '3', residentName: 'Mehmet Kaya', apartment: '3', amount: 500, dueDate: '2023-12-15', paidDate: null, status: 'overdue' },
];

const initialExpenses: Expense[] = [
  { id: '1', description: 'Ortak alan elektrik faturası', category: 'Elektrik', amount: 1200, date: '2024-01-05', paidBy: 'Yönetim' },
  { id: '2', description: 'Asansör bakımı', category: 'Asansör', amount: 800, date: '2024-01-10', paidBy: 'Yönetim' },
  { id: '3', description: 'Bahçe düzenlemesi', category: 'Bahçe', amount: 1500, date: '2024-01-12', paidBy: 'Yönetim' },
];

const initialAnnouncements: Announcement[] = [
  { id: '1', title: 'Su Kesintisi Bildirimi', content: 'Yarın saat 10:00-14:00 arası bakım çalışması nedeniyle su kesintisi olacaktır. Lütfen tedbirinizi alınız.', date: '15.01.2024', author: 'Site Yönetimi', priority: 'high' },
  { id: '2', title: 'Aylık Toplantı', content: 'Bu ayın site toplantısı 20 Ocak Cumartesi günü saat 15:00\'te toplantı salonunda gerçekleştirilecektir.', date: '12.01.2024', author: 'Site Yönetimi', priority: 'medium' },
];

function App() {
  const [residents, setResidents] = useState<Resident[]>(initialResidents);
  const [dues, setDues] = useState<Due[]>(initialDues);
  const [expenses, setExpenses] = useState<Expense[]>(initialExpenses);
  const [announcements, setAnnouncements] = useState<Announcement[]>(initialAnnouncements);

  const generateId = () => Math.random().toString(36).substr(2, 9);

  // Resident handlers
  const handleAddResident = (resident: Omit<Resident, 'id'>) => {
    setResidents([...residents, { ...resident, id: generateId() }]);
  };

  const handleDeleteResident = (id: string) => {
    setResidents(residents.filter((r) => r.id !== id));
  };

  // Due handlers
  const handleAddDue = (due: Omit<Due, 'id'>) => {
    setDues([...dues, { ...due, id: generateId() }]);
  };

  const handleMarkAsPaid = (id: string) => {
    setDues(
      dues.map((due) =>
        due.id === id
          ? { ...due, status: 'paid' as const, paidDate: new Date().toISOString().split('T')[0] }
          : due
      )
    );
  };

  // Expense handlers
  const handleAddExpense = (expense: Omit<Expense, 'id'>) => {
    setExpenses([...expenses, { ...expense, id: generateId() }]);
  };

  const handleDeleteExpense = (id: string) => {
    setExpenses(expenses.filter((e) => e.id !== id));
  };

  // Announcement handlers
  const handleAddAnnouncement = (announcement: Omit<Announcement, 'id'>) => {
    setAnnouncements([{ ...announcement, id: generateId() }, ...announcements]);
  };

  const handleDeleteAnnouncement = (id: string) => {
    setAnnouncements(announcements.filter((a) => a.id !== id));
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route
            index
            element={
              <Dashboard
                residents={residents}
                dues={dues}
                expenses={expenses}
                announcements={announcements}
              />
            }
          />
          <Route
            path="residents"
            element={
              <Residents
                residents={residents}
                onAddResident={handleAddResident}
                onDeleteResident={handleDeleteResident}
              />
            }
          />
          <Route
            path="dues"
            element={
              <Dues
                dues={dues}
                residents={residents}
                onAddDue={handleAddDue}
                onMarkAsPaid={handleMarkAsPaid}
              />
            }
          />
          <Route
            path="expenses"
            element={
              <Expenses
                expenses={expenses}
                onAddExpense={handleAddExpense}
                onDeleteExpense={handleDeleteExpense}
              />
            }
          />
          <Route
            path="announcements"
            element={
              <Announcements
                announcements={announcements}
                onAddAnnouncement={handleAddAnnouncement}
                onDeleteAnnouncement={handleDeleteAnnouncement}
              />
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
