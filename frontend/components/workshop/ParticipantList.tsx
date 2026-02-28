/**
 * Participant List Component
 * Displays list of joined participants
 */
import React from 'react';
import type { Participant } from '../../types/workshop';

interface ParticipantListProps {
  participants: Participant[];
  onRemove?: (participantId: string) => void;
}

const ParticipantList: React.FC<ParticipantListProps> = ({ participants, onRemove }) => {
  return (
    <div className="bg-white shadow rounded-lg divide-y divide-gray-200">
      {participants.map((participant) => (
        <div key={participant.id} className="p-4 flex justify-between items-center hover:bg-gray-50">
          <div>
            <p className="text-sm font-medium text-gray-900">{participant.user_name}</p>
            <p className="text-sm text-gray-500">{participant.user_email}</p>
            <p className="text-xs text-gray-400 mt-1">
              Joined: {new Date(participant.requested_at).toLocaleDateString()}
            </p>
          </div>
          {onRemove && (
            <button
              onClick={() => onRemove(participant.id)}
              className="px-3 py-1 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded"
            >
              Remove
            </button>
          )}
        </div>
      ))}
    </div>
  );
};

export default ParticipantList;
