/**
 * Pending Request Card Component
 * Displays a pending join request with approve/reject actions
 */
import React from 'react';
import type { Participant } from '../../types/workshop';

interface PendingRequestCardProps {
  participant: Participant;
  onApprove: (participantId: string) => void;
  onReject: (participantId: string) => void;
}

const PendingRequestCard: React.FC<PendingRequestCardProps> = ({
  participant,
  onApprove,
  onReject,
}) => {
  return (
    <div className="bg-white shadow rounded-lg p-4 flex justify-between items-center">
      <div>
        <p className="text-sm font-medium text-gray-900">{participant.user_name}</p>
        <p className="text-sm text-gray-500">{participant.user_email}</p>
        <p className="text-xs text-gray-400 mt-1">
          Requested: {new Date(participant.requested_at).toLocaleDateString()}
        </p>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={() => onApprove(participant.id)}
          className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          Approve
        </button>
        <button
          onClick={() => onReject(participant.id)}
          className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Reject
        </button>
      </div>
    </div>
  );
};

export default PendingRequestCard;
