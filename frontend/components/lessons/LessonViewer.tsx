/**
 * Lesson Viewer Component
 */
import React, { useState } from 'react';
import { lessonApi } from '../../lib/lessons';
import type { Lesson } from '../../types/lesson';

interface LessonViewerProps {
  lesson: Lesson;
  isOwner: boolean;
  onClose: () => void;
  onComplete?: () => void;
}

const LessonViewer: React.FC<LessonViewerProps> = ({ lesson, isOwner, onClose, onComplete }) => {
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [pointsEarned, setPointsEarned] = useState<number | null>(null);

  const handleComplete = async () => {
    if (isOwner) return;

    try {
      setCompleting(true);
      const response = await lessonApi.completeLesson(lesson.id);
      setCompleted(true);
      setPointsEarned(response.points_earned);
      if (onComplete) onComplete();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to complete lesson');
    } finally {
      setCompleting(false);
    }
  };

  const getMaterialIcon = (type: string) => {
    switch (type) {
      case 'video':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
          </svg>
        );
      case 'pdf':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clipRule="evenodd" />
          </svg>
        );
    }
  };

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    return `${minutes} min`;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between sticky top-0 bg-white">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{lesson.title}</h2>
            {lesson.description && (
              <p className="text-sm text-gray-600 mt-1">{lesson.description}</p>
            )}
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

        {/* Content */}
        <div className="px-6 py-6">
          {/* Lesson Content */}
          {lesson.content && (
            <div className="prose max-w-none mb-6">
              <div className="whitespace-pre-wrap text-gray-700">{lesson.content}</div>
            </div>
          )}

          {/* Materials */}
          {lesson.materials && lesson.materials.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Materials</h3>
              <div className="space-y-2">
                {lesson.materials.map((material) => (
                  <a
                    key={material.id}
                    href={material.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div className="text-blue-600">
                      {getMaterialIcon(material.material_type)}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{material.title}</p>
                      <div className="flex items-center space-x-2 text-xs text-gray-500">
                        <span className="capitalize">{material.material_type}</span>
                        {material.duration && <span>• {formatDuration(material.duration)}</span>}
                      </div>
                    </div>
                    <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Completion Section */}
          {!isOwner && (
            <div className="border-t border-gray-200 pt-6">
              {completed || pointsEarned !== null ? (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                  <svg className="w-12 h-12 text-green-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-green-800 font-semibold">Lesson Completed!</p>
                  <p className="text-green-700 text-sm mt-1">
                    You earned {pointsEarned || lesson.points} points
                  </p>
                </div>
              ) : (
                <button
                  onClick={handleComplete}
                  disabled={completing}
                  className="w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                  {completing ? 'Completing...' : `Complete Lesson (${lesson.points} points)`}
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LessonViewer;
