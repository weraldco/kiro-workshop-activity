/**
 * Workshop Content Management Page (Owner)
 */
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../../../../contexts/AuthContext';
import { getWorkshopById } from '../../../../lib/workshops';
import CreateLessonModal from '../../../../components/lessons/CreateLessonModal';
import LessonList from '../../../../components/lessons/LessonList';
import LessonViewer from '../../../../components/lessons/LessonViewer';
import AddMaterialModal from '../../../../components/lessons/AddMaterialModal';
import CreateChallengeModal from '../../../../components/challenges/CreateChallengeModal';
import ChallengeList from '../../../../components/challenges/ChallengeList';
import ChallengeViewer from '../../../../components/challenges/ChallengeViewer';
import CreateExamModal from '../../../../components/exams/CreateExamModal';
import ExamList from '../../../../components/exams/ExamList';
import ExamManager from '../../../../components/exams/ExamManager';
import type { Workshop } from '../../../../types/workshop';
import type { Lesson } from '../../../../types/lesson';
import type { Challenge } from '../../../../types/challenge';
import type { Exam } from '../../../../types/exam';

const WorkshopContentPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const { user } = useAuth();
  
  const [workshop, setWorkshop] = useState<Workshop | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'lessons' | 'challenges' | 'exams'>('lessons');
  
  // Lesson modals
  const [showCreateLesson, setShowCreateLesson] = useState(false);
  const [showAddMaterial, setShowAddMaterial] = useState(false);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [selectedLessonForMaterial, setSelectedLessonForMaterial] = useState<string | null>(null);
  
  // Challenge modals
  const [showCreateChallenge, setShowCreateChallenge] = useState(false);
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);
  
  // Exam modals
  const [showCreateExam, setShowCreateExam] = useState(false);
  const [selectedExam, setSelectedExam] = useState<Exam | null>(null);
  
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (id) {
      loadWorkshop();
    }
  }, [id]);

  const loadWorkshop = async () => {
    try {
      setLoading(true);
      const data = await getWorkshopById(id as string);
      setWorkshop(data);
      
      // Check if user is owner
      if (user && data.owner_id !== user.id) {
        router.push(`/workshops/${id}`);
      }
    } catch (error) {
      console.error('Failed to load workshop:', error);
      router.push('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleLessonClick = (lesson: Lesson) => {
    setSelectedLesson(lesson);
  };

  const handleAddMaterial = (lessonId: string) => {
    setSelectedLessonForMaterial(lessonId);
    setShowAddMaterial(true);
  };

  const handleChallengeClick = (challenge: Challenge) => {
    setSelectedChallenge(challenge);
  };

  const handleExamClick = (exam: Exam) => {
    setSelectedExam(exam);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!workshop) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Workshop not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => router.push(`/dashboard/workshops/${id}`)}
            className="text-blue-600 hover:text-blue-800 mb-2 flex items-center"
          >
            <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Workshop
          </button>
          <h1 className="text-3xl font-bold text-gray-900">{workshop.title}</h1>
          <p className="text-gray-600 mt-1">Manage workshop content</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('lessons')}
                className={`px-6 py-3 text-sm font-medium border-b-2 ${
                  activeTab === 'lessons'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Lessons
              </button>
              <button
                onClick={() => setActiveTab('challenges')}
                className={`px-6 py-3 text-sm font-medium border-b-2 ${
                  activeTab === 'challenges'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Challenges
              </button>
              <button
                onClick={() => setActiveTab('exams')}
                className={`px-6 py-3 text-sm font-medium border-b-2 ${
                  activeTab === 'exams'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Exams
              </button>
            </nav>
          </div>

          <div className="p-6">
            {/* Lessons Tab */}
            {activeTab === 'lessons' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Lessons</h2>
                  <button
                    onClick={() => setShowCreateLesson(true)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Create Lesson
                  </button>
                </div>
                <LessonList
                  key={refreshKey}
                  workshopId={id as string}
                  isOwner={true}
                  onLessonClick={handleLessonClick}
                />
              </div>
            )}

            {/* Challenges Tab */}
            {activeTab === 'challenges' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Challenges</h2>
                  <button
                    onClick={() => setShowCreateChallenge(true)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Create Challenge
                  </button>
                </div>
                <ChallengeList
                  key={refreshKey}
                  workshopId={id as string}
                  isOwner={true}
                  onChallengeClick={handleChallengeClick}
                />
              </div>
            )}

            {/* Exams Tab */}
            {activeTab === 'exams' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Exams</h2>
                  <button
                    onClick={() => setShowCreateExam(true)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Create Exam
                  </button>
                </div>
                <ExamList
                  key={refreshKey}
                  workshopId={id as string}
                  isOwner={true}
                  onExamClick={handleExamClick}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modals */}
      <CreateLessonModal
        workshopId={id as string}
        isOpen={showCreateLesson}
        onClose={() => setShowCreateLesson(false)}
        onSuccess={() => {
          setRefreshKey(prev => prev + 1);
        }}
      />

      <CreateChallengeModal
        workshopId={id as string}
        isOpen={showCreateChallenge}
        onClose={() => setShowCreateChallenge(false)}
        onSuccess={() => {
          setRefreshKey(prev => prev + 1);
        }}
      />

      <CreateExamModal
        workshopId={id as string}
        isOpen={showCreateExam}
        onClose={() => setShowCreateExam(false)}
        onSuccess={() => {
          setRefreshKey(prev => prev + 1);
        }}
      />

      {selectedLesson && (
        <LessonViewer
          lesson={selectedLesson}
          isOwner={true}
          onClose={() => setSelectedLesson(null)}
        />
      )}

      {selectedChallenge && (
        <ChallengeViewer
          challenge={selectedChallenge}
          isOwner={true}
          onClose={() => setSelectedChallenge(null)}
        />
      )}

      {selectedExam && (
        <ExamManager
          exam={selectedExam}
          onClose={() => setSelectedExam(null)}
        />
      )}

      {selectedLessonForMaterial && (
        <AddMaterialModal
          lessonId={selectedLessonForMaterial}
          isOpen={showAddMaterial}
          onClose={() => {
            setShowAddMaterial(false);
            setSelectedLessonForMaterial(null);
          }}
          onSuccess={() => {
            setRefreshKey(prev => prev + 1);
          }}
        />
      )}
    </div>
  );
};

export default WorkshopContentPage;
