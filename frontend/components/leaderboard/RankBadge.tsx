/**
 * Rank Badge Component
 */
import React from 'react';

interface RankBadgeProps {
  rank: number;
  size?: 'sm' | 'md' | 'lg';
}

const RankBadge: React.FC<RankBadgeProps> = ({ rank, size = 'md' }) => {
  const getBadgeColor = () => {
    if (rank === 1) return 'bg-yellow-400 text-yellow-900 ring-yellow-500';
    if (rank === 2) return 'bg-gray-300 text-gray-900 ring-gray-400';
    if (rank === 3) return 'bg-orange-400 text-orange-900 ring-orange-500';
    return 'bg-blue-100 text-blue-900 ring-blue-300';
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'w-8 h-8 text-xs';
      case 'lg':
        return 'w-14 h-14 text-xl';
      default:
        return 'w-10 h-10 text-sm';
    }
  };

  return (
    <div
      className={`${getSizeClasses()} rounded-full flex items-center justify-center font-bold ${getBadgeColor()} ring-2`}
    >
      {rank}
    </div>
  );
};

export default RankBadge;
