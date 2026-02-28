/**
 * Challenge Viewer Component
 */
import React, { useState, useEffect } from 'react';
import { challengeApi } from '../../lib/challenges';
import SubmitChallengeModal from './SubmitChallengeModal';
import ReviewSubmissionModal from './ReviewSubmissionModal';
import type { Challenge, ChallengeSubmission } from '../../types/challenge';

interface ChallengeViewerProps {
  challenge: Challenge;
  isOwner: boolean;
  onClose: () => void;
  onSubmit?: () => void;
}

const ChallengeViewer: React.FC<ChallengeViewerProps> = ({
  challenge,
  isOwner,
  onClose,
  onSubmit,
}) => {
  const [submissions, setSubmissions] = useState<ChallengeSubmission[]>([]);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [selectedSubmission, setSelectedSubmission] = useState<ChallengeSubmission | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOwner) {
      loadSubmissions();
    }
  }, [challenge.id, isOwner]);

  const loadSubmissions = async () => {
    try {
      setLoading(true);
      const data = await challengeApi.getSubmissions(challenge.workshop_id, challenge.id);
      setSubmissions(data);
    } catch (err) {
      console.error('Failed to load submissions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReview = (submission: ChallengeSubmission) => {
    setSelectedSubmission(submission);
    setShowReviewModal(true);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-6">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-medium text-gray-500">#{challenge.order_index}</span>
                <h2 className="text-2xl font-bold text-gray-900">{challenge.title}</h2>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-blue-600">
                  {challenge.points} points
                </span>
                <span className="text-xs text-gray-500">
                  Created {new Date(challenge.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Description */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{challenge.description}</p>
          </div>

          {/* Solution (Owner Only) */}
          {isOwner && challenge.solution && (
            <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Solution</h3>
              <p className="text-gray-700 whitespace-pre-wrap">{challenge.solution}</p>
            </div>
          )}

          {/* Submissions (Owner Only) */}
          {isOwner && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Submissions ({submissions.length})
              </h3>
              {loading ? (
                <div className="flex justify-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                </div>
              ) : submissions.length === 0 ? (
                <p className="text-gray-500 text-sm">No submissions yet</p>
              ) : (
                <div className="space-y-3">
                  {submissions.map((submission) => (
                    <div
                      key={submission.id}
                      className="p-3 border border-gray-200 rounded-lg"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-gray-900">
                            User #{submission.user_id}
                          </p>
                          <p className="text-xs text-gray-500">
                            {new Date(submission.submitted_at).toLocaleString()}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 text-xs font-medium rounded ${
                            submission.status === 'passed'
                              ? 'bg-green-100 text-green-800'
                              : submission.status === 'failed'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {submission.status}
                          </span>
                          <button
                            onClick={() => handleReview(submission)}
                            className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
                          >
                            Review
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4 border-t">
            {!isOwner && (
              <button
                onClick={() => setShowSubmitModal(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Submit Solution
              </button>
            )}
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Close
            </button>
          </div>
        </div>
      </div>

      {/* Submit Modal */}
      {!isOwner && (
        <SubmitChallengeModal
          workshopId={challenge.workshop_id}
          challengeId={challenge.id}
          isOpen={showSubmitModal}
          onClose={() => setShowSubmitModal(false)}
          onSuccess={() => {
            if (onSubmit) onSubmit();
          }}
        />
      )}

      {/* Review Modal */}
      {isOwner && selectedSubmission && (
        <ReviewSubmissionModal
          workshopId={challenge.workshop_id}
          challengeId={challenge.id}
          submission={selectedSubmission}
          isOpen={showReviewModal}
          onClose={() => {
            setShowReviewModal(false);
            setSelectedSubmission(null);
          }}
          onSuccess={() => {
            loadSubmissions();
          }}
        />
      )}
    </div>
  );
};

export default ChallengeViewer;
