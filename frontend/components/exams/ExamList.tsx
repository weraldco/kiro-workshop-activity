/**
 * Exam List Component
 */
import React, { useEffect, useState } from 'react';
import { examApi } from '../../lib/exams';
import type { Exam } from '../../types/exam';

interface ExamListProps {
  workshopId: string;
  isOwner: boolean;
  onExamClick: (exam: Exam) => void;
  onDelete?: (examId: string) => void;
}

const ExamList: React.FC<ExamListProps> = ({
  workshopId,
  isOwner,
  onExamClick,
  onDelete,
}) => {
  const [exams, setExams] = useState<Exam[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadExams();
  }, [workshopId]);

  const loadExams = async () => {
    try {
      setLoading(true);
      const data = await examApi.getExams(workshopId);
      setExams(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load exams');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (examId: string) => {
    if (!confirm('Are you sure you want to delete this exam?')) return;

    try {
      await examApi.deleteExam(workshopId, examId);
      setExams(exams.filter(e => e.id !== examId));
      if (onDelete) onDelete(examId);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to delete exam');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (exams.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p className="mt-2 text-gray-600">No exams yet</p>
        {isOwner && (
          <p className="text-sm text-gray-500 mt-1">Create your first exam to get started</p>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {exams.map((exam) => (
        <div
          key={exam.id}
          className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900">{exam.title}</h3>
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{exam.description}</p>
              <div className="flex items-center gap-4 mt-3 text-sm">
                <span className="font-medium text-blue-600">
                  {exam.points} points
                </span>
                <span className="text-gray-500">
                  ⏱️ {exam.duration_minutes} min
                </span>
                <span className="text-gray-500">
                  📊 {exam.passing_score}% to pass
                </span>
                <span className="text-xs text-gray-500">
                  Created {new Date(exam.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-2 ml-4">
              <button
                onClick={() => onExamClick(exam)}
                className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
              >
                {isOwner ? 'Manage' : 'Take Exam'}
              </button>
              {isOwner && (
                <button
                  onClick={() => handleDelete(exam.id)}
                  className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ExamList;
