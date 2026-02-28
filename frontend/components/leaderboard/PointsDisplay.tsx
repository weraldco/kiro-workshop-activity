/**
 * Points Display Component
 */
import React from 'react';
import type { UserPoints } from '../../types/points';

interface PointsDisplayProps {
  points: UserPoints;
  showDetails?: boolean;
}

const PointsDisplay: React.FC<PointsDisplayProps> = ({ points, showDetails = true }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="text-center mb-6">
        <p className="text-sm text-gray-600 mb-2">Total Points</p>
        <p className="text-5xl font-bold text-blue-600">{points.total_points}</p>
      </div>

      {showDetails && (
        <div className="grid grid-cols-3 gap-4 pt-6 border-t border-gray-200">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{points.lessons_completed}</p>
            <p className="text-xs text-gray-600 mt-1">Lessons</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{points.challenges_completed}</p>
            <p className="text-xs text-gray-600 mt-1">Challenges</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{points.exams_passed}</p>
            <p className="text-xs text-gray-600 mt-1">Exams</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PointsDisplay;
