/**
 * Workshop Card Component
 * Displays a workshop with join functionality
 */
import React from 'react';
import Link from 'next/link';
import type { Workshop } from '../../types/workshop';
import JoinButton from './JoinButton';

interface WorkshopCardProps {
  workshop: Workshop;
  currentUserId?: string;
  participationStatus?: 'pending' | 'joined' | 'rejected' | 'waitlisted' | null;
  onJoinSuccess?: () => void;
}

const WorkshopCard: React.FC<WorkshopCardProps> = ({
  workshop,
  currentUserId,
  participationStatus,
  onJoinSuccess,
}) => {
  const isOwner = currentUserId === workshop.owner_id;

  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    ongoing: 'bg-green-100 text-green-800',
    completed: 'bg-gray-100 text-gray-800',
  };

  const participationColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    joined: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    waitlisted: 'bg-orange-100 text-orange-800',
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">{workshop.title}</h3>
          <div className="flex items-center space-x-2">
            <span className={`inline-block px-2 py-1 text-xs font-medium rounded ${statusColors[workshop.status]}`}>
              {workshop.status}
            </span>
            {isOwner && (
              <span className="inline-block px-2 py-1 text-xs font-medium rounded bg-blue-100 text-blue-800">
                Owner
              </span>
            )}
            {participationStatus && (
              <span className={`inline-block px-2 py-1 text-xs font-medium rounded ${participationColors[participationStatus]}`}>
                {participationStatus}
              </span>
            )}
          </div>
        </div>
      </div>

      <p className="text-sm text-gray-600 mb-4 line-clamp-3">{workshop.description}</p>

      <div className="flex items-center justify-between">
        <div className="text-xs text-gray-500">
          {workshop.signup_enabled ? (
            <span className="text-green-600">✓ Signup Open</span>
          ) : (
            <span className="text-red-600">✗ Signup Closed</span>
          )}
        </div>

        <div className="flex space-x-2">
          {isOwner ? (
            <Link
              href={`/dashboard/workshops/${workshop.id}`}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
            >
              Manage
            </Link>
          ) : (
            <>
              <Link
                href={`/workshops/${workshop.id}`}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200"
              >
                View
              </Link>
              {currentUserId && (
                <JoinButton
                  workshopId={workshop.id}
                  signupEnabled={workshop.signup_enabled}
                  participationStatus={participationStatus}
                  onSuccess={onJoinSuccess}
                />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default WorkshopCard;
