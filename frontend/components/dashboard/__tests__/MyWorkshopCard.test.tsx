/**
 * MyWorkshopCard Component Tests
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MyWorkshopCard from '../MyWorkshopCard';
import type { Workshop } from '../../../types/workshop';

// Mock Next.js Link
jest.mock('next/link', () => {
  return ({ children, href }: any) => {
    return <a href={href}>{children}</a>;
  };
});

describe('MyWorkshopCard', () => {
  const mockWorkshop: Workshop = {
    id: '123',
    title: 'Test Workshop',
    description: 'This is a test workshop description',
    status: 'ongoing',
    signup_enabled: true,
    owner_id: 'user-123',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  it('renders workshop information', () => {
    render(<MyWorkshopCard workshop={mockWorkshop} />);
    
    expect(screen.getByText('Test Workshop')).toBeInTheDocument();
    expect(screen.getByText('This is a test workshop description')).toBeInTheDocument();
    expect(screen.getByText('ongoing')).toBeInTheDocument();
  });

  it('shows signup open status when enabled', () => {
    render(<MyWorkshopCard workshop={mockWorkshop} />);
    
    expect(screen.getByText(/signup open/i)).toBeInTheDocument();
  });

  it('shows signup closed status when disabled', () => {
    const closedWorkshop = { ...mockWorkshop, signup_enabled: false };
    render(<MyWorkshopCard workshop={closedWorkshop} />);
    
    expect(screen.getByText(/signup closed/i)).toBeInTheDocument();
  });

  it('displays correct status badge color for pending', () => {
    const pendingWorkshop = { ...mockWorkshop, status: 'pending' as const };
    render(<MyWorkshopCard workshop={pendingWorkshop} />);
    
    const badge = screen.getByText('pending');
    expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-800');
  });

  it('displays correct status badge color for ongoing', () => {
    render(<MyWorkshopCard workshop={mockWorkshop} />);
    
    const badge = screen.getByText('ongoing');
    expect(badge).toHaveClass('bg-green-100', 'text-green-800');
  });

  it('displays correct status badge color for completed', () => {
    const completedWorkshop = { ...mockWorkshop, status: 'completed' as const };
    render(<MyWorkshopCard workshop={completedWorkshop} />);
    
    const badge = screen.getByText('completed');
    expect(badge).toHaveClass('bg-gray-100', 'text-gray-800');
  });

  it('has manage link with correct href', () => {
    render(<MyWorkshopCard workshop={mockWorkshop} />);
    
    const manageLink = screen.getByText('Manage').closest('a');
    expect(manageLink).toHaveAttribute('href', '/dashboard/workshops/123');
  });

  it('calls onDelete when delete button is clicked', () => {
    const mockOnDelete = jest.fn();
    render(<MyWorkshopCard workshop={mockWorkshop} onDelete={mockOnDelete} />);
    
    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);
    
    expect(mockOnDelete).toHaveBeenCalledWith('123');
  });

  it('does not render delete button when onDelete is not provided', () => {
    render(<MyWorkshopCard workshop={mockWorkshop} />);
    
    expect(screen.queryByText('Delete')).not.toBeInTheDocument();
  });
});
