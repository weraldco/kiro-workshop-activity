export interface Challenge {
  id: string;
  workshop_id: string;
  title: string;
  description: string;
  html_content?: string;
  solution?: string;
  order_index: number;
  points: number;
  created_at: string;
  updated_at: string;
  submission?: ChallengeSubmission;
}

export interface ChallengeSubmission {
  id: string;
  user_id: string;
  challenge_id: string;
  submission_text?: string;
  submission_url?: string;
  status: 'pending' | 'passed' | 'failed';
  points_earned: number;
  submitted_at: string;
  reviewed_at?: string;
  reviewed_by?: string;
  feedback?: string;
  user_name?: string;
  user_email?: string;
}

export interface CreateChallengeData {
  title: string;
  description: string;
  html_content?: string;
  solution?: string;
  order_index?: number;
  points?: number;
}

export interface UpdateChallengeData {
  title?: string;
  description?: string;
  html_content?: string;
  solution?: string;
  order_index?: number;
  points?: number;
}

export interface SubmitChallengeData {
  submission_text?: string;
  submission_url?: string;
}

export interface ReviewSubmissionData {
  status: 'passed' | 'failed';
  points_earned: number;
  feedback?: string;
}
