/**
 * Public Workshops Page
 * Browse all available workshops
 */
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../contexts/AuthContext';
import WorkshopCard from '../../components/workshop/WorkshopCard';
import { getAllWorkshops, getJoinedWorkshops } from '../../lib/workshops';
import type { Workshop, ParticipantWithWorkshop } from '../../types/workshop';

const WorkshopsPage: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const [workshops, setWorkshops] = useState<Workshop[]>([]);
  const [participations, setParticipations] = useState<Map<string, string>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWorkshops = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const workshopsData = await getAllWorkshops();
      setWorkshops(workshopsData);

      // Fetch user's participations if authenticated
      if (isAuthenticated) {
        try {
          const joinedData = await getJoinedWorkshops();
          const participationMap = new Map<string, string>();
          joinedData.forEach((p: ParticipantWithWorkshop) => {
            participationMap.set(p.workshop_id, p.status);
          });
          setParticipations(participationMap);
        } catch (err) {
          // Ignore errors fetching participations
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load workshops');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkshops();
  }, [isAuthenticated]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-8">
              <Link href="/" className="text-xl font-bold text-blue-600">
                Workshop Manager
              </Link>
              <nav className="hidden md:flex space-x-4">
                <Link href="/workshops" className="px-3 py-2 rounded-md text-sm font-medium bg-blue-100 text-blue-700">
                  All Workshops
                </Link>
                {isAuthenticated && (
                  <Link href="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
                    Dashboard
                  </Link>
                )}
              </nav>
            </div>

            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <span className="text-sm text-gray-700">
                    {user?.name}
                  </span>
                  <Link
                    href="/dashboard"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Dashboard
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/auth/signin"
                    className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/auth/signup"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">All Workshops</h1>
          <p className="mt-2 text-sm text-gray-600">
            Browse and join available workshops
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded text-sm text-red-600">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-sm text-gray-500">Loading workshops...</p>
          </div>
        ) : workshops.length === 0 ? (
          <div className="text-center py-12 bg-white shadow rounded-lg">
            <p className="text-gray-500">No workshops available yet.</p>
            {isAuthenticated && (
              <Link
                href="/dashboard"
                className="mt-4 inline-block text-blue-600 hover:text-blue-700 font-medium"
              >
                Create the first workshop
              </Link>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {workshops.map((workshop) => (
              <WorkshopCard
                key={workshop.id}
                workshop={workshop}
                currentUserId={user?.id}
                participationStatus={participations.get(workshop.id) as any}
                onJoinSuccess={fetchWorkshops}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default WorkshopsPage;
