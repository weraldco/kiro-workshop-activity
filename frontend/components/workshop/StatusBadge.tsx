/**
 * Status Badge Component
 * Displays participation status with appropriate styling
 */
import React from 'react';

interface StatusBadgeProps {
  status: 'pending' | 'joined' | 'rejected' | 'waitlisted';
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const colors = {
    pending: 'bg-yellow-100 text-yellow-800',
    joined: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    waitlisted: 'bg-orange-100 text-orange-800',
  };

  const labels = {
    pending: 'Pending',
    joined: 'Joined',
    rejected: 'Rejected',
    waitlisted: 'Waitlisted',
  };

  return (
    <span className={`inline-block px-2 py-1 text-xs font-medium rounded ${colors[status]}`}>
      {labels[status]}
    </span>
  );
};

export default StatusBadge;
