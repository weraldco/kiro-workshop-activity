/**
 * Public Workshop Detail Page
 */
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useAuth } from '../../contexts/AuthContext';
import JoinButton from '../../components/workshop/JoinButton';
import StatusBadge from '../../components/workshop/StatusBadge';
import { getWorkshopById, getJoinedWorkshops } from '../../lib/workshops';
import type { Workshop } from '../../types/workshop';

const PublicWorkshopDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const { user, isAuthenticated } = useAuth();
  
  const [workshop, setWorkshop] = useState<Workshop | null>(null);
  const [participationStatus, setParticipationStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWorkshopData = async () => {
    if (!id || typeof id !== 'string') return;

    try {
      setLoading(true);
      setError(null);
      
      const workshopData = await getWorkshopById(id);
      setWorkshop(workshopData);

      // Check participation status if authenticated
      if (isAuthenticated) {
        try {
          const joinedData = await getJoinedWorkshops();
          const participation = joinedData.find(p => p.workshop_id === id);
          if (participation) {
            setParticipationStatus(participation.status);
          }
        } catch (err) {
          // Ignore errors
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load workshop');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkshopData();
  }, [id, isAuthenticated]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-sm text-gray-500">Loading workshop...</p>
        </div>
      </div>
    );
  }

  if (error || !workshop) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">{error || 'Workshop not found'}</p>
          <Link href="/workshops" className="mt-4 inline-block text-blue-600 hover:text-blue-700">
            Back to Workshops
          </Link>
        </div>
      </div>
    );
  }

  const isOwner = user && workshop.owner_id === user.id;

  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    ongoing: 'bg-green-100 text-green-800',
    completed: 'bg-gray-100 text-gray-800',
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Link href="/workshops" className="text-sm text-gray-600 hover:text-gray-900">
              ← Back to Workshops
            </Link>
            {isAuthenticated && (
              <Link
                href="/dashboard"
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
              >
                Dashboard
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white shadow rounded-lg p-8">
          <div className="flex justify-between items-start mb-6">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-3">{workshop.title}</h1>
              <div className="flex items-center space-x-2">
                <span className={`px-3 py-1 text-sm font-medium rounded ${statusColors[workshop.status]}`}>
                  {workshop.status}
                </span>
                {isOwner && (
                  <span className="px-3 py-1 text-sm font-medium rounded bg-blue-100 text-blue-800">
                    You own this workshop
                  </span>
                )}
                {participationStatus && (
                  <StatusBadge status={participationStatus as any} />
                )}
              </div>
            </div>
          </div>

          <div className="prose max-w-none mb-8">
            <p className="text-gray-700 text-lg">{workshop.description}</p>
          </div>

          <div className="border-t border-gray-200 pt-6">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                {workshop.signup_enabled ? (
                  <span className="text-green-600 font-medium">✓ Signup is open</span>
                ) : (
                  <span className="text-red-600 font-medium">✗ Signup is closed</span>
                )}
              </div>

              <div className="flex space-x-3">
                {isOwner ? (
                  <Link
                    href={`/dashboard/workshops/${workshop.id}`}
                    className="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Manage Workshop
                  </Link>
                ) : isAuthenticated ? (
                  <JoinButton
                    workshopId={workshop.id}
                    signupEnabled={workshop.signup_enabled}
                    participationStatus={participationStatus as any}
                    onSuccess={fetchWorkshopData}
                  />
                ) : (
                  <Link
                    href="/auth/signin"
                    className="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Sign in to Join
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PublicWorkshopDetailPage;
