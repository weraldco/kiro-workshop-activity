import React from 'react';
import WorkshopList from '../components/WorkshopList';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Workshop Management System</h1>
        <WorkshopList />
      </div>
    </div>
  );
}
