/**
 * Workshop Detail Page
 */
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import ProtectedRoute from '../../../components/ProtectedRoute';
import DashboardLayout from '../../../components/layout/DashboardLayout';
import ParticipantList from '../../../components/workshop/ParticipantList';
import PendingRequestCard from '../../../components/workshop/PendingRequestCard';
import { getWorkshopById, updateWorkshop } from '../../../lib/workshops';
import { authApi } from '../../../lib/auth';
import { useAuth } from '../../../contexts/AuthContext';
import type { Workshop, ParticipantsByStatus, Participant } from '../../../types/workshop';

const WorkshopDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const { user } = useAuth();
  
  const [workshop, setWorkshop] = useState<Workshop | null>(null);
  const [participants, setParticipants] = useState<ParticipantsByStatus>({
    pending: [],
    joined: [],
    rejected: [],
    waitlisted: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({ title: '', description: '' });

  const isOwner = workshop && user && workshop.owner_id === user.id;

  const fetchWorkshopData = async () => {
    if (!id || typeof id !== 'string') return;

    try {
      setLoading(true);
      setError(null);
      const workshopData = await getWorkshopById(id);
      setWorkshop(workshopData);
      setEditData({ title: workshopData.title, description: workshopData.description });

      // Fetch participants if owner
      if (workshopData.owner_id === user?.id) {
        const response = await authApi.get<ParticipantsByStatus>(`/api/workshops/${id}/participants`);
        setParticipants(response.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load workshop');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkshopData();
  }, [id, user]);

  const handleApprove = async (participantId: string) => {
    if (!id || typeof id !== 'string') return;

    try {
      await authApi.patch(`/api/workshops/${id}/participants/${participantId}`, {
        status: 'joined',
      });
      await fetchWorkshopData();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to approve participant');
    }
  };

  const handleReject = async (participantId: string) => {
    if (!id || typeof id !== 'string') return;

    if (!confirm('Are you sure you want to reject this request?')) return;

    try {
      await authApi.patch(`/api/workshops/${id}/participants/${participantId}`, {
        status: 'rejected',
      });
      await fetchWorkshopData();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to reject participant');
    }
  };

  const handleRemove = async (participantId: string) => {
    if (!id || typeof id !== 'string') return;

    if (!confirm('Are you sure you want to remove this participant?')) return;

    try {
      await authApi.delete(`/api/workshops/${id}/participants/${participantId}`);
      await fetchWorkshopData();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to remove participant');
    }
  };

  const handleToggleSignup = async () => {
    if (!workshop || !id || typeof id !== 'string') return;

    try {
      const updated = await updateWorkshop(id, {
        signup_enabled: !workshop.signup_enabled,
      });
      setWorkshop(updated);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to update workshop');
    }
  };

  const handleUpdateStatus = async (newStatus: 'pending' | 'ongoing' | 'completed') => {
    if (!id || typeof id !== 'string') return;

    try {
      const updated = await updateWorkshop(id, { status: newStatus });
      setWorkshop(updated);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to update status');
    }
  };

  const handleSaveEdit = async () => {
    if (!id || typeof id !== 'string') return;

    try {
      const updated = await updateWorkshop(id, editData);
      setWorkshop(updated);
      setIsEditing(false);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to update workshop');
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <DashboardLayout>
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-sm text-gray-500">Loading workshop...</p>
          </div>
        </DashboardLayout>
      </ProtectedRoute>
    );
  }

  if (error || !workshop) {
    return (
      <ProtectedRoute>
        <DashboardLayout>
          <div className="text-center py-12">
            <p className="text-red-600">{error || 'Workshop not found'}</p>
            <button
              onClick={() => router.push('/dashboard')}
              className="mt-4 text-blue-600 hover:text-blue-700"
            >
              Back to Dashboard
            </button>
          </div>
        </DashboardLayout>
      </ProtectedRoute>
    );
  }

  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    ongoing: 'bg-green-100 text-green-800',
    completed: 'bg-gray-100 text-gray-800',
  };

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="mb-6">
          <button
            onClick={() => router.push('/dashboard')}
            className="text-sm text-gray-600 hover:text-gray-900 mb-4"
          >
            ← Back to Dashboard
          </button>

          <div className="bg-white shadow rounded-lg p-6">
            {isEditing ? (
              <div>
                <input
                  type="text"
                  value={editData.title}
                  onChange={(e) => setEditData({ ...editData, title: e.target.value })}
                  className="w-full text-2xl font-bold text-gray-900 mb-4 px-3 py-2 border border-gray-300 rounded"
                />
                <textarea
                  value={editData.description}
                  onChange={(e) => setEditData({ ...editData, description: e.target.value })}
                  rows={4}
                  className="w-full text-gray-700 mb-4 px-3 py-2 border border-gray-300 rounded"
                />
                <div className="flex space-x-2">
                  <button
                    onClick={handleSaveEdit}
                    className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                  >
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setEditData({ title: workshop.title, description: workshop.description });
                    }}
                    className="px-4 py-2 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <div className="flex justify-between items-start mb-4">
                  <h1 className="text-2xl font-bold text-gray-900">{workshop.title}</h1>
                  <span className={`px-3 py-1 text-sm font-medium rounded ${statusColors[workshop.status]}`}>
                    {workshop.status}
                  </span>
                </div>
                <p className="text-gray-700 mb-6">{workshop.description}</p>

                {isOwner && (
                  <div className="flex flex-wrap gap-2 pt-4 border-t border-gray-200">
                    <button
                      onClick={() => router.push(`/dashboard/workshops/${id}/content`)}
                      className="px-3 py-1 text-sm bg-purple-50 text-purple-600 rounded hover:bg-purple-100 font-medium"
                    >
                      📚 Manage Content
                    </button>
                    <button
                      onClick={() => setIsEditing(true)}
                      className="px-3 py-1 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100"
                    >
                      Edit
                    </button>
                    <button
                      onClick={handleToggleSignup}
                      className={`px-3 py-1 text-sm rounded ${
                        workshop.signup_enabled
                          ? 'bg-red-50 text-red-600 hover:bg-red-100'
                          : 'bg-green-50 text-green-600 hover:bg-green-100'
                      }`}
                    >
                      {workshop.signup_enabled ? 'Close Signup' : 'Open Signup'}
                    </button>
                    <select
                      value={workshop.status}
                      onChange={(e) => handleUpdateStatus(e.target.value as any)}
                      className="px-3 py-1 text-sm border border-gray-300 rounded"
                    >
                      <option value="pending">Pending</option>
                      <option value="ongoing">Ongoing</option>
                      <option value="completed">Completed</option>
                    </select>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {isOwner && (
          <div className="space-y-6">
            {/* Pending Requests */}
            {participants.pending.length > 0 && (
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Pending Requests ({participants.pending.length})
                </h2>
                <div className="space-y-3">
                  {participants.pending.map((participant) => (
                    <PendingRequestCard
                      key={participant.id}
                      participant={participant}
                      onApprove={handleApprove}
                      onReject={handleReject}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Joined Participants */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Participants ({participants.joined.length})
              </h2>
              {participants.joined.length === 0 ? (
                <div className="bg-white shadow rounded-lg p-6 text-center text-sm text-gray-500">
                  No participants yet
                </div>
              ) : (
                <ParticipantList
                  participants={participants.joined}
                  onRemove={handleRemove}
                />
              )}
            </div>

            {/* Rejected/Waitlisted (collapsed) */}
            {(participants.rejected.length > 0 || participants.waitlisted.length > 0) && (
              <details className="bg-white shadow rounded-lg p-6">
                <summary className="cursor-pointer font-medium text-gray-900">
                  Other Requests ({participants.rejected.length + participants.waitlisted.length})
                </summary>
                <div className="mt-4 space-y-4">
                  {participants.rejected.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-gray-700 mb-2">Rejected</h3>
                      <div className="space-y-2">
                        {participants.rejected.map((p) => (
                          <div key={p.id} className="text-sm text-gray-600 bg-red-50 p-2 rounded">
                            {p.user_name} ({p.user_email})
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {participants.waitlisted.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-gray-700 mb-2">Waitlisted</h3>
                      <div className="space-y-2">
                        {participants.waitlisted.map((p) => (
                          <div key={p.id} className="text-sm text-gray-600 bg-orange-50 p-2 rounded">
                            {p.user_name} ({p.user_email})
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </details>
            )}
          </div>
        )}
      </DashboardLayout>
    </ProtectedRoute>
  );
};

export default WorkshopDetailPage;
