# Site Yönetim Uygulaması (Site Management App)

A modern, Turkish-language site/building management application built with React, TypeScript, and Tailwind CSS.

## Features

- 🏠 **Dashboard (Ana Sayfa)**: Overview of key metrics including total residents, pending/overdue dues, and recent activities
- 👥 **Residents (Sakinler)**: Manage resident information including name, apartment number, contact details
- 💰 **Dues (Aidatlar)**: Track monthly dues, payment status, and mark payments as complete
- 📊 **Expenses (Giderler)**: Record and categorize building expenses (electricity, water, maintenance, etc.)
- 📢 **Announcements (Duyurular)**: Create and manage announcements for residents with priority levels

## Tech Stack

- React 19
- TypeScript
- Vite
- Tailwind CSS
- React Router

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/        # Reusable UI components
│   ├── Layout.tsx    # Main layout with sidebar
│   └── Sidebar.tsx   # Navigation sidebar
├── pages/            # Page components
│   ├── Dashboard.tsx
│   ├── Residents.tsx
│   ├── Dues.tsx
│   ├── Expenses.tsx
│   └── Announcements.tsx
├── types/            # TypeScript type definitions
│   └── index.ts
├── App.tsx           # Main application component
├── main.tsx          # Entry point
└── index.css         # Global styles with Tailwind
```

## License

MIT
