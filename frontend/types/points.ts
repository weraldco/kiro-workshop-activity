export interface UserPoints {
  user_id: string;
  total_points: number;
  lessons_completed: number;
  challenges_completed: number;
  exams_passed: number;
  current_rank: number;
  previous_rank: number;
  last_updated: string;
  name?: string;
  email?: string;
}

export interface RankInfo {
  rank: number;
  previous_rank: number;
  change: number;
  direction: 'up' | 'down' | 'same' | 'new';
  total_points: number;
}

export interface LeaderboardEntry extends UserPoints {
  rank_info: RankInfo;
}

export interface GlobalLeaderboardResponse {
  leaderboard: LeaderboardEntry[];
  current_user_rank?: RankInfo;
}

export interface WorkshopLeaderboardEntry {
  user_id: string;
  name: string;
  email: string;
  total_points: number;
  lessons_completed: number;
  challenges_completed: number;
  exams_passed: number;
}

export interface WorkshopLeaderboardResponse {
  workshop_id: string;
  workshop_title: string;
  leaderboard: WorkshopLeaderboardEntry[];
}

export interface UserPointsResponse {
  points: UserPoints;
  rank_info: RankInfo;
}
