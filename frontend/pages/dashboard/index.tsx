/**
 * Dashboard Page
 */
import React, { useState, useEffect } from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import DashboardLayout from '../../components/layout/DashboardLayout';
import MyWorkshopCard from '../../components/dashboard/MyWorkshopCard';
import JoinedWorkshopCard from '../../components/dashboard/JoinedWorkshopCard';
import CreateWorkshopModal from '../../components/dashboard/CreateWorkshopModal';
import { getMyWorkshops, getJoinedWorkshops, deleteWorkshop } from '../../lib/workshops';
import { authApi } from '../../lib/auth';
import type { Workshop, ParticipantWithWorkshop } from '../../types/workshop';

const DashboardPage: React.FC = () => {
  const [myWorkshops, setMyWorkshops] = useState<Workshop[]>([]);
  const [joinedWorkshops, setJoinedWorkshops] = useState<ParticipantWithWorkshop[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const fetchWorkshops = async () => {
    try {
      setLoading(true);
      setError(null);
      const [myWorkshopsData, joinedWorkshopsData] = await Promise.all([
        getMyWorkshops(),
        getJoinedWorkshops(),
      ]);
      setMyWorkshops(myWorkshopsData);
      setJoinedWorkshops(joinedWorkshopsData);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load workshops');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkshops();
  }, []);

  const handleDeleteWorkshop = async (id: string) => {
    if (!confirm('Are you sure you want to delete this workshop?')) return;

    try {
      await deleteWorkshop(id);
      setMyWorkshops(myWorkshops.filter(w => w.id !== id));
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to delete workshop');
    }
  };

  const handleLeaveWorkshop = async (workshopId: string, participantId: string) => {
    if (!confirm('Are you sure you want to leave this workshop?')) return;

    try {
      await authApi.delete(`/api/workshops/${workshopId}/participants/${participantId}`);
      setJoinedWorkshops(joinedWorkshops.filter(p => p.id !== participantId));
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to leave workshop');
    }
  };

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Create Workshop
            </button>
          </div>
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
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* My Workshops Section */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                My Workshops ({myWorkshops.length})
              </h2>
              {myWorkshops.length === 0 ? (
                <div className="bg-white shadow rounded-lg p-6 text-center">
                  <p className="text-sm text-gray-500">
                    You haven't created any workshops yet.
                  </p>
                  <button
                    onClick={() => setIsCreateModalOpen(true)}
                    className="mt-4 text-sm text-blue-600 hover:text-blue-700 font-medium"
                  >
                    Create your first workshop
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {myWorkshops.map((workshop) => (
                    <MyWorkshopCard
                      key={workshop.id}
                      workshop={workshop}
                      onDelete={handleDeleteWorkshop}
                    />
                  ))}
                </div>
              )}
            </div>

            {/* Joined Workshops Section */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Joined Workshops ({joinedWorkshops.length})
              </h2>
              {joinedWorkshops.length === 0 ? (
                <div className="bg-white shadow rounded-lg p-6 text-center">
                  <p className="text-sm text-gray-500">
                    You haven't joined any workshops yet.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {joinedWorkshops.map((participation) => (
                    <JoinedWorkshopCard
                      key={participation.id}
                      participation={participation}
                      onLeave={handleLeaveWorkshop}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        <CreateWorkshopModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          onSuccess={fetchWorkshops}
        />
      </DashboardLayout>
    </ProtectedRoute>
  );
};

export default DashboardPage;
