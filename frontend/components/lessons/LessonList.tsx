/**
 * Lesson List Component
 */
import React, { useEffect, useState } from 'react';
import { lessonApi } from '../../lib/lessons';
import type { Lesson } from '../../types/lesson';

interface LessonListProps {
  workshopId: string;
  isOwner: boolean;
  onLessonClick: (lesson: Lesson) => void;
}

const LessonList: React.FC<LessonListProps> = ({ workshopId, isOwner, onLessonClick }) => {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLessons();
  }, [workshopId]);

  const loadLessons = async () => {
    try {
      setLoading(true);
      const data = await lessonApi.getLessons(workshopId);
      setLessons(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load lessons');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (lessonId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this lesson?')) return;

    try {
      await lessonApi.deleteLesson(lessonId);
      setLessons(lessons.filter(l => l.id !== lessonId));
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to delete lesson');
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
        <button onClick={loadLessons} className="mt-2 text-blue-600 hover:underline">
          Retry
        </button>
      </div>
    );
  }

  if (lessons.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
        <p className="mt-2 text-gray-600">No lessons yet</p>
        {isOwner && <p className="text-sm text-gray-500 mt-1">Create your first lesson to get started</p>}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {lessons.map((lesson) => (
        <div
          key={lesson.id}
          onClick={() => onLessonClick(lesson)}
          className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer border border-gray-200"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-medium text-gray-500">#{lesson.order_index + 1}</span>
                <h3 className="font-semibold text-gray-900">{lesson.title}</h3>
              </div>
              {lesson.description && (
                <p className="text-sm text-gray-600 mt-1">{lesson.description}</p>
              )}
              <div className="flex items-center space-x-4 mt-2">
                <span className="text-xs text-blue-600 font-medium">
                  {lesson.points} points
                </span>
                {lesson.materials && lesson.materials.length > 0 && (
                  <span className="text-xs text-gray-500">
                    {lesson.materials.length} material{lesson.materials.length !== 1 ? 's' : ''}
                  </span>
                )}
              </div>
            </div>
            {isOwner && (
              <button
                onClick={(e) => handleDelete(lesson.id, e)}
                className="ml-4 text-red-600 hover:text-red-800 text-sm"
              >
                Delete
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default LessonList;
