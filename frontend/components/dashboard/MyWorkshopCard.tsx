/**
 * My Workshop Card Component
 * Displays a workshop created by the current user
 */
import React from 'react';
import Link from 'next/link';
import type { Workshop } from '../../types/workshop';

interface MyWorkshopCardProps {
  workshop: Workshop;
  onDelete?: (id: string) => void;
}

const MyWorkshopCard: React.FC<MyWorkshopCardProps> = ({ workshop, onDelete }) => {
  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    ongoing: 'bg-green-100 text-green-800',
    completed: 'bg-gray-100 text-gray-800',
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-900">{workshop.title}</h3>
        <span className={`px-2 py-1 text-xs font-medium rounded ${statusColors[workshop.status]}`}>
          {workshop.status}
        </span>
      </div>
      
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">{workshop.description}</p>
      
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4 text-sm text-gray-500">
          <span className={workshop.signup_enabled ? 'text-green-600' : 'text-red-600'}>
            {workshop.signup_enabled ? '✓ Signup Open' : '✗ Signup Closed'}
          </span>
        </div>
        
        <div className="flex space-x-2">
          <Link
            href={`/dashboard/workshops/${workshop.id}`}
            className="px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded"
          >
            Manage
          </Link>
          {onDelete && (
            <button
              onClick={() => onDelete(workshop.id)}
              className="px-3 py-1 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded"
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default MyWorkshopCard;
