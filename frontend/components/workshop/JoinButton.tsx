/**
 * Join Button Component
 * Handles workshop join requests
 */
import React, { useState } from 'react';
import { joinWorkshop } from '../../lib/workshops';

interface JoinButtonProps {
  workshopId: string;
  signupEnabled: boolean;
  participationStatus?: 'pending' | 'joined' | 'rejected' | 'waitlisted' | null;
  onSuccess?: () => void;
}

const JoinButton: React.FC<JoinButtonProps> = ({
  workshopId,
  signupEnabled,
  participationStatus,
  onSuccess,
}) => {
  const [loading, setLoading] = useState(false);

  const handleJoin = async () => {
    setLoading(true);
    try {
      await joinWorkshop(workshopId);
      if (onSuccess) onSuccess();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to join workshop');
    } finally {
      setLoading(false);
    }
  };

  // Already joined or pending
  if (participationStatus === 'joined') {
    return (
      <button
        disabled
        className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded cursor-not-allowed opacity-75"
      >
        Joined
      </button>
    );
  }

  if (participationStatus === 'pending') {
    return (
      <button
        disabled
        className="px-4 py-2 text-sm font-medium text-white bg-yellow-600 rounded cursor-not-allowed opacity-75"
      >
        Pending
      </button>
    );
  }

  if (participationStatus === 'rejected') {
    return (
      <button
        disabled
        className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded cursor-not-allowed opacity-75"
      >
        Rejected
      </button>
    );
  }

  if (participationStatus === 'waitlisted') {
    return (
      <button
        disabled
        className="px-4 py-2 text-sm font-medium text-white bg-orange-600 rounded cursor-not-allowed opacity-75"
      >
        Waitlisted
      </button>
    );
  }

  // Signup closed
  if (!signupEnabled) {
    return (
      <button
        disabled
        className="px-4 py-2 text-sm font-medium text-gray-400 bg-gray-200 rounded cursor-not-allowed"
      >
        Signup Closed
      </button>
    );
  }

  // Can join
  return (
    <button
      onClick={handleJoin}
      disabled={loading}
      className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
    >
      {loading ? 'Joining...' : 'Join'}
    </button>
  );
};

export default JoinButton;
