/**
 * Global Leaderboard Page
 */
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { leaderboardApi } from '../lib/leaderboard';
import type { GlobalLeaderboardResponse, LeaderboardEntry } from '../types/points';

const RankBadge: React.FC<{ rank: number }> = ({ rank }) => {
  const getBadgeColor = () => {
    if (rank === 1) return 'bg-yellow-400 text-yellow-900';
    if (rank === 2) return 'bg-gray-300 text-gray-900';
    if (rank === 3) return 'bg-orange-400 text-orange-900';
    return 'bg-blue-100 text-blue-900';
  };

  return (
    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${getBadgeColor()}`}>
      {rank}
    </div>
  );
};

const RankChangeIndicator: React.FC<{ direction: string; change: number }> = ({ direction, change }) => {
  if (direction === 'new') {
    return <span className="text-xs text-blue-600 font-medium">NEW</span>;
  }
  
  if (direction === 'same' || change === 0) {
    return <span className="text-xs text-gray-500">—</span>;
  }

  if (direction === 'up') {
    return (
      <span className="text-xs text-green-600 font-medium flex items-center">
        ↑ {change}
      </span>
    );
  }

  if (direction === 'down') {
    return (
      <span className="text-xs text-red-600 font-medium flex items-center">
        ↓ {change}
      </span>
    );
  }

  return null;
};

const LeaderboardPage: React.FC = () => {
  const { user } = useAuth();
  const [data, setData] = useState<GlobalLeaderboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await leaderboardApi.getGlobalLeaderboard(100);
      setData(response);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">{error}</p>
          <button
            onClick={loadLeaderboard}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Global Leaderboard</h1>
          <p className="text-gray-600">Top performers across all workshops</p>
        </div>

        {/* Current User Rank Card */}
        {user && data?.current_user_rank && (
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-6 mb-8 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-90 mb-1">Your Rank</p>
                <div className="flex items-center space-x-4">
                  <span className="text-4xl font-bold">#{data.current_user_rank.rank}</span>
                  <RankChangeIndicator
                    direction={data.current_user_rank.direction}
                    change={data.current_user_rank.change}
                  />
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm opacity-90 mb-1">Total Points</p>
                <p className="text-3xl font-bold">{data.current_user_rank.total_points}</p>
              </div>
            </div>
          </div>
        )}

        {/* Leaderboard Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Change
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Points
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Lessons
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Challenges
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Exams
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data?.leaderboard.map((entry: LeaderboardEntry, index: number) => {
                  const isCurrentUser = user && entry.user_id === user.id;
                  return (
                    <tr
                      key={entry.user_id}
                      className={isCurrentUser ? 'bg-blue-50' : index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <RankBadge rank={entry.rank_info.rank} />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <RankChangeIndicator
                          direction={entry.rank_info.direction}
                          change={entry.rank_info.change}
                        />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {entry.name}
                            {isCurrentUser && (
                              <span className="ml-2 text-xs text-blue-600 font-semibold">(You)</span>
                            )}
                          </div>
                          <div className="text-sm text-gray-500">{entry.email}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-bold text-gray-900">{entry.total_points}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{entry.lessons_completed}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{entry.challenges_completed}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{entry.exams_passed}</div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {data?.leaderboard.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No users on the leaderboard yet</p>
            </div>
          )}
        </div>

        {/* Legend */}
        <div className="mt-6 bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-medium text-gray-900 mb-3">Rank Change Legend</h3>
          <div className="flex flex-wrap gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <span className="text-green-600 font-medium">↑</span>
              <span className="text-gray-600">Moved up</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-red-600 font-medium">↓</span>
              <span className="text-gray-600">Moved down</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-gray-500">—</span>
              <span className="text-gray-600">No change</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-blue-600 font-medium">NEW</span>
              <span className="text-gray-600">First time on leaderboard</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeaderboardPage;
