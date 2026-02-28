/**
 * Exam Manager Component (Owner View)
 */
import React, { useState, useEffect } from 'react';
import { examApi } from '../../lib/exams';
import type { Exam, ExamQuestion } from '../../types/exam';

interface ExamManagerProps {
  exam: Exam;
  onClose: () => void;
}

const ExamManager: React.FC<ExamManagerProps> = ({ exam, onClose }) => {
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddQuestion, setShowAddQuestion] = useState(false);
  const [newQuestion, setNewQuestion] = useState({
    question_text: '',
    question_type: 'multiple_choice' as 'multiple_choice' | 'true_false' | 'short_answer',
    options: ['', '', '', ''],
    correct_answer: '',
    points: 10,
  });

  useEffect(() => {
    loadQuestions();
  }, [exam.id]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const data = await examApi.getExam(exam.workshop_id, exam.id);
      setQuestions(data.questions || []);
    } catch (err) {
      console.error('Failed to load questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await examApi.addQuestion(exam.workshop_id, exam.id, {
        ...newQuestion,
        options: newQuestion.question_type === 'multiple_choice' 
          ? newQuestion.options.filter(o => o.trim())
          : undefined,
      });
      setNewQuestion({
        question_text: '',
        question_type: 'multiple_choice',
        options: ['', '', '', ''],
        correct_answer: '',
        points: 10,
      });
      setShowAddQuestion(false);
      loadQuestions();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to add question');
    }
  };

  const handleDeleteQuestion = async (questionId: string) => {
    if (!confirm('Delete this question?')) return;
    try {
      await examApi.deleteQuestion(exam.workshop_id, exam.id, questionId);
      loadQuestions();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to delete question');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{exam.title}</h2>
              <p className="text-sm text-gray-600 mt-1">{exam.description}</p>
              <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                <span>⏱️ {exam.duration_minutes} min</span>
                <span>📊 {exam.passing_score}% to pass</span>
                <span>🎯 {exam.points} points</span>
              </div>
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Questions */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Questions ({questions.length})
              </h3>
              <button
                onClick={() => setShowAddQuestion(!showAddQuestion)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
              >
                {showAddQuestion ? 'Cancel' : 'Add Question'}
              </button>
            </div>

            {/* Add Question Form */}
            {showAddQuestion && (
              <form onSubmit={handleAddQuestion} className="mb-6 p-4 bg-gray-50 rounded-lg space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Question Text *
                  </label>
                  <textarea
                    value={newQuestion.question_text}
                    onChange={(e) => setNewQuestion({ ...newQuestion, question_text: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Type
                    </label>
                    <select
                      value={newQuestion.question_type}
                      onChange={(e) => setNewQuestion({ 
                        ...newQuestion, 
                        question_type: e.target.value as any 
                      })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="multiple_choice">Multiple Choice</option>
                      <option value="true_false">True/False</option>
                      <option value="short_answer">Short Answer</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Points
                    </label>
                    <input
                      type="number"
                      value={newQuestion.points}
                      onChange={(e) => setNewQuestion({ ...newQuestion, points: parseInt(e.target.value) })}
                      min="1"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>

                {newQuestion.question_type === 'multiple_choice' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Options
                    </label>
                    {newQuestion.options.map((opt, idx) => (
                      <input
                        key={idx}
                        type="text"
                        value={opt}
                        onChange={(e) => {
                          const newOpts = [...newQuestion.options];
                          newOpts[idx] = e.target.value;
                          setNewQuestion({ ...newQuestion, options: newOpts });
                        }}
                        placeholder={`Option ${idx + 1}`}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2"
                      />
                    ))}
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Correct Answer *
                  </label>
                  <input
                    type="text"
                    value={newQuestion.correct_answer}
                    onChange={(e) => setNewQuestion({ ...newQuestion, correct_answer: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Add Question
                </button>
              </form>
            )}

            {/* Questions List */}
            {loading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : questions.length === 0 ? (
              <p className="text-center text-gray-500 py-8">No questions yet</p>
            ) : (
              <div className="space-y-3">
                {questions.map((q, idx) => (
                  <div key={q.id} className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xs font-medium text-gray-500">Q{idx + 1}</span>
                          <span className="text-xs px-2 py-1 bg-gray-100 rounded">{q.question_type}</span>
                          <span className="text-xs text-blue-600">{q.points} pts</span>
                        </div>
                        <p className="text-gray-900 mb-2">{q.question_text}</p>
                        {q.options && (
                          <ul className="text-sm text-gray-600 space-y-1">
                            {q.options.map((opt, i) => (
                              <li key={i}>• {opt}</li>
                            ))}
                          </ul>
                        )}
                        <p className="text-sm text-green-600 mt-2">✓ {q.correct_answer}</p>
                      </div>
                      <button
                        onClick={() => handleDeleteQuestion(q.id)}
                        className="text-red-600 hover:bg-red-50 px-2 py-1 rounded text-sm"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex justify-end pt-4 border-t">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExamManager;
