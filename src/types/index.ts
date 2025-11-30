export interface Resident {
  id: string;
  name: string;
  apartment: string;
  phone: string;
  email: string;
  moveInDate: string;
}

export interface Due {
  id: string;
  residentId: string;
  residentName: string;
  apartment: string;
  amount: number;
  dueDate: string;
  paidDate: string | null;
  status: 'paid' | 'pending' | 'overdue';
}

export interface Expense {
  id: string;
  description: string;
  category: string;
  amount: number;
  date: string;
  paidBy: string;
}

export interface Announcement {
  id: string;
  title: string;
  content: string;
  date: string;
  author: string;
  priority: 'low' | 'medium' | 'high';
}
