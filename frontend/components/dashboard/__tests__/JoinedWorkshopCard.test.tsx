/**
 * JoinedWorkshopCard Component Tests
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import JoinedWorkshopCard from '../JoinedWorkshopCard';
import type { ParticipantWithWorkshop } from '../../../types/workshop';

// Mock Next.js Link
jest.mock('next/link', () => {
  return ({ children, href }: any) => {
    return <a href={href}>{children}</a>;
  };
});

describe('JoinedWorkshopCard', () => {
  const mockParticipation: ParticipantWithWorkshop = {
    id: 'part-123',
    workshop_id: 'workshop-123',
    user_id: 'user-123',
    status: 'joined',
    requested_at: '2024-01-01T00:00:00Z',
    approved_at: '2024-01-02T00:00:00Z',
    approved_by: 'owner-123',
    user_name: 'Test User',
    user_email: 'test@example.com',
    workshop_title: 'Test Workshop',
    workshop_description: 'This is a test workshop',
    workshop_status: 'ongoing',
    workshop_owner_id: 'owner-123',
  };

  it('renders workshop information', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    expect(screen.getByText('Test Workshop')).toBeInTheDocument();
    expect(screen.getByText('This is a test workshop')).toBeInTheDocument();
  });

  it('displays participation status badge', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    expect(screen.getByText('joined')).toBeInTheDocument();
  });

  it('displays workshop status badge', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    expect(screen.getByText('ongoing')).toBeInTheDocument();
  });

  it('shows correct status color for joined', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    const badge = screen.getByText('joined');
    expect(badge).toHaveClass('bg-green-100', 'text-green-800');
  });

  it('shows correct status color for pending', () => {
    const pendingParticipation = { ...mockParticipation, status: 'pending' as const };
    render(<JoinedWorkshopCard participation={pendingParticipation} />);
    
    const badge = screen.getByText('pending');
    expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-800');
  });

  it('shows correct status color for rejected', () => {
    const rejectedParticipation = { ...mockParticipation, status: 'rejected' as const };
    render(<JoinedWorkshopCard participation={rejectedParticipation} />);
    
    const badge = screen.getByText('rejected');
    expect(badge).toHaveClass('bg-red-100', 'text-red-800');
  });

  it('shows correct status color for waitlisted', () => {
    const waitlistedParticipation = { ...mockParticipation, status: 'waitlisted' as const };
    render(<JoinedWorkshopCard participation={waitlistedParticipation} />);
    
    const badge = screen.getByText('waitlisted');
    expect(badge).toHaveClass('bg-orange-100', 'text-orange-800');
  });

  it('displays joined date', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    expect(screen.getByText(/joined:/i)).toBeInTheDocument();
  });

  it('has view link with correct href', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    const viewLink = screen.getByText('View').closest('a');
    expect(viewLink).toHaveAttribute('href', '/dashboard/workshops/workshop-123');
  });

  it('calls onLeave when leave button is clicked', () => {
    const mockOnLeave = jest.fn();
    render(<JoinedWorkshopCard participation={mockParticipation} onLeave={mockOnLeave} />);
    
    const leaveButton = screen.getByText('Leave');
    fireEvent.click(leaveButton);
    
    expect(mockOnLeave).toHaveBeenCalledWith('workshop-123', 'part-123');
  });

  it('does not show leave button for rejected status', () => {
    const rejectedParticipation = { ...mockParticipation, status: 'rejected' as const };
    const mockOnLeave = jest.fn();
    render(<JoinedWorkshopCard participation={rejectedParticipation} onLeave={mockOnLeave} />);
    
    expect(screen.queryByText('Leave')).not.toBeInTheDocument();
  });

  it('does not render leave button when onLeave is not provided', () => {
    render(<JoinedWorkshopCard participation={mockParticipation} />);
    
    expect(screen.queryByText('Leave')).not.toBeInTheDocument();
  });
});
