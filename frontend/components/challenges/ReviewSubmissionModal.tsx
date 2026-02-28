/**
 * Review Submission Modal Component
 */
import React, { useState } from 'react';
import { challengeApi } from '../../lib/challenges';
import type { ChallengeSubmission } from '../../types/challenge';

interface ReviewSubmissionModalProps {
  workshopId: string;
  challengeId: string;
  submission: ChallengeSubmission;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const ReviewSubmissionModal: React.FC<ReviewSubmissionModalProps> = ({
  workshopId,
  challengeId,
  submission,
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [status, setStatus] = useState<'pending' | 'passed' | 'failed'>(submission.status);
  const [feedback, setFeedback] = useState(submission.feedback || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await challengeApi.reviewSubmission(workshopId, challengeId, submission.id, {
        status,
        feedback,
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to review submission');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-900">Review Submission</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          {/* Submission Info */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">User ID:</span>
                <span className="ml-2 font-medium">{submission.user_id}</span>
              </div>
              <div>
                <span className="text-gray-600">Submitted:</span>
                <span className="ml-2 font-medium">
                  {new Date(submission.submitted_at).toLocaleString()}
                </span>
              </div>
            </div>
          </div>

          {/* Submitted Solution */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Submitted Solution</h3>
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
              <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                {submission.solution}
              </pre>
            </div>
          </div>

          {/* Review Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status *
              </label>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setStatus('pending')}
                  className={`flex-1 px-4 py-2 rounded-lg border-2 transition-colors ${
                    status === 'pending'
                      ? 'border-yellow-500 bg-yellow-50 text-yellow-700'
                      : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                  }`}
                >
                  Pending
                </button>
                <button
                  type="button"
                  onClick={() => setStatus('passed')}
                  className={`flex-1 px-4 py-2 rounded-lg border-2 transition-colors ${
                    status === 'passed'
                      ? 'border-green-500 bg-green-50 text-green-700'
                      : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                  }`}
                >
                  Passed
                </button>
                <button
                  type="button"
                  onClick={() => setStatus('failed')}
                  className={`flex-1 px-4 py-2 rounded-lg border-2 transition-colors ${
                    status === 'failed'
                      ? 'border-red-500 bg-red-50 text-red-700'
                      : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                  }`}
                >
                  Failed
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Feedback
              </label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Provide feedback to the participant..."
              />
            </div>

            <div className="flex justify-end gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Saving...' : 'Save Review'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ReviewSubmissionModal;
