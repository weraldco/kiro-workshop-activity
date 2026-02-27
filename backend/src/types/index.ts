// Type definitions for Workshop Management System

export interface Workshop {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'ongoing' | 'completed';
  signup_enabled: boolean;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

export interface Participant {
  id: string;
  workshop_id: string;
  user_id: string;
  signed_up_at: string; // ISO 8601 timestamp
}

export interface Challenge {
  id: string;
  workshop_id: string;
  title: string; // max 200 characters
  description: string; // max 1000 characters
  html_content: string;
}

// API Response Interfaces
export interface WorkshopListResponse {
  workshops: Workshop[];
}

export interface SignupResponse {
  success: boolean;
  participant_id?: string;
  error?: string;
}

export interface ChallengeListResponse {
  challenges: Challenge[];
}

export interface ErrorResponse {
  error: string;
  code: string;
  status?: number;
}
