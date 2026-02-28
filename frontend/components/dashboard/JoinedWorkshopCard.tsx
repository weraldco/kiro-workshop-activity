/**
 * Joined Workshop Card Component
 * Displays a workshop the user has joined
 */
import React from 'react';
import Link from 'next/link';
import type { ParticipantWithWorkshop } from '../../types/workshop';

interface JoinedWorkshopCardProps {
  participation: ParticipantWithWorkshop;
  onLeave?: (workshopId: string, participantId: string) => void;
}

const JoinedWorkshopCard: React.FC<JoinedWorkshopCardProps> = ({ participation, onLeave }) => {
  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    joined: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    waitlisted: 'bg-orange-100 text-orange-800',
  };

  const workshopStatusColors = {
    pending: 'bg-yellow-50 text-yellow-700',
    ongoing: 'bg-green-50 text-green-700',
    completed: 'bg-gray-50 text-gray-700',
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{participation.workshop_title}</h3>
          <span className={`inline-block mt-1 px-2 py-1 text-xs font-medium rounded ${workshopStatusColors[participation.workshop_status as keyof typeof workshopStatusColors]}`}>
            {participation.workshop_status}
          </span>
        </div>
        <span className={`px-2 py-1 text-xs font-medium rounded ${statusColors[participation.status]}`}>
          {participation.status}
        </span>
      </div>
      
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">{participation.workshop_description}</p>
      
      <div className="flex items-center justify-between">
        <div className="text-xs text-gray-500">
          Joined: {new Date(participation.requested_at).toLocaleDateString()}
        </div>
        
        <div className="flex space-x-2">
          <Link
            href={`/dashboard/workshops/${participation.workshop_id}`}
            className="px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded"
          >
            View
          </Link>
          {onLeave && participation.status !== 'rejected' && (
            <button
              onClick={() => onLeave(participation.workshop_id, participation.id)}
              className="px-3 py-1 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded"
            >
              Leave
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default JoinedWorkshopCard;
