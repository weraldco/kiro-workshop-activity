/**
 * Rank Change Indicator Component
 */
import React from 'react';

interface RankChangeIndicatorProps {
  direction: 'up' | 'down' | 'same' | 'new';
  change: number;
  size?: 'sm' | 'md' | 'lg';
}

const RankChangeIndicator: React.FC<RankChangeIndicatorProps> = ({ direction, change, size = 'md' }) => {
  const getSizeClass = () => {
    switch (size) {
      case 'sm':
        return 'text-xs';
      case 'lg':
        return 'text-base';
      default:
        return 'text-sm';
    }
  };

  if (direction === 'new') {
    return (
      <span className={`${getSizeClass()} text-blue-600 font-medium px-2 py-1 bg-blue-50 rounded`}>
        NEW
      </span>
    );
  }

  if (direction === 'same' || change === 0) {
    return <span className={`${getSizeClass()} text-gray-500`}>—</span>;
  }

  if (direction === 'up') {
    return (
      <span className={`${getSizeClass()} text-green-600 font-medium flex items-center space-x-1`}>
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
            clipRule="evenodd"
          />
        </svg>
        <span>{change}</span>
      </span>
    );
  }

  if (direction === 'down') {
    return (
      <span className={`${getSizeClass()} text-red-600 font-medium flex items-center space-x-1`}>
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z"
            clipRule="evenodd"
          />
        </svg>
        <span>{change}</span>
      </span>
    );
  }

  return null;
};

export default RankChangeIndicator;
