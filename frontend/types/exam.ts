export interface Exam {
  id: string;
  workshop_id: string;
  title: string;
  description?: string;
  duration_minutes: number;
  passing_score: number;
  points: number;
  created_at: string;
  updated_at: string;
  questions?: ExamQuestion[];
  best_attempt?: ExamAttempt;
}

export interface ExamQuestion {
  id: string;
  exam_id: string;
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'short_answer';
  options?: string[];
  correct_answer?: string;
  points: number;
  order_index: number;
  created_at: string;
}

export interface ExamAttempt {
  id: string;
  user_id: string;
  exam_id: string;
  answers: Record<string, string>;
  score: number;
  points_earned: number;
  passed: boolean;
  started_at: string;
  submitted_at?: string;
  exam?: Exam;
}

export interface CreateExamData {
  title: string;
  description?: string;
  duration_minutes?: number;
  passing_score?: number;
  points?: number;
}

export interface UpdateExamData {
  title?: string;
  description?: string;
  duration_minutes?: number;
  passing_score?: number;
  points?: number;
}

export interface CreateQuestionData {
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'short_answer';
  options?: string[];
  correct_answer: string;
  points?: number;
  order_index?: number;
}

export interface UpdateQuestionData {
  question_text?: string;
  question_type?: 'multiple_choice' | 'true_false' | 'short_answer';
  options?: string[];
  correct_answer?: string;
  points?: number;
  order_index?: number;
}

export interface SubmitExamData {
  answers: Record<string, string>;
}
