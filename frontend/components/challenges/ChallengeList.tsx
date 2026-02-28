/**
 * Challenge List Component
 */
import React, { useEffect, useState } from 'react';
import { challengeApi } from '../../lib/challenges';
import type { Challenge } from '../../types/challenge';

interface ChallengeListProps {
  workshopId: string;
  isOwner: boolean;
  onChallengeClick: (challenge: Challenge) => void;
  onDelete?: (challengeId: string) => void;
}

const ChallengeList: React.FC<ChallengeListProps> = ({
  workshopId,
  isOwner,
  onChallengeClick,
  onDelete,
}) => {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadChallenges();
  }, [workshopId]);

  const loadChallenges = async () => {
    try {
      setLoading(true);
      const data = await challengeApi.getChallenges(workshopId);
      setChallenges(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load challenges');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (challengeId: string) => {
    if (!confirm('Are you sure you want to delete this challenge?')) return;

    try {
      await challengeApi.deleteChallenge(workshopId, challengeId);
      setChallenges(challenges.filter(c => c.id !== challengeId));
      if (onDelete) onDelete(challengeId);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to delete challenge');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (challenges.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p className="mt-2 text-gray-600">No challenges yet</p>
        {isOwner && (
          <p className="text-sm text-gray-500 mt-1">Create your first challenge to get started</p>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {challenges.map((challenge) => (
        <div
          key={challenge.id}
          className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-gray-500">#{challenge.order_index}</span>
                <h3 className="text-lg font-semibold text-gray-900">{challenge.title}</h3>
              </div>
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{challenge.description}</p>
              <div className="flex items-center gap-4 mt-3">
                <span className="text-sm font-medium text-blue-600">
                  {challenge.points} points
                </span>
                <span className="text-xs text-gray-500">
                  Created {new Date(challenge.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-2 ml-4">
              <button
                onClick={() => onChallengeClick(challenge)}
                className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
              >
                View
              </button>
              {isOwner && (
                <button
                  onClick={() => handleDelete(challenge.id)}
                  className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChallengeList;
