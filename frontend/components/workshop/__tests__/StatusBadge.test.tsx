/**
 * StatusBadge Component Tests
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import StatusBadge from '../StatusBadge';

describe('StatusBadge', () => {
  it('renders pending status with correct styling', () => {
    render(<StatusBadge status="pending" />);
    
    const badge = screen.getByText('Pending');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-800');
  });

  it('renders joined status with correct styling', () => {
    render(<StatusBadge status="joined" />);
    
    const badge = screen.getByText('Joined');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-green-100', 'text-green-800');
  });

  it('renders rejected status with correct styling', () => {
    render(<StatusBadge status="rejected" />);
    
    const badge = screen.getByText('Rejected');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-red-100', 'text-red-800');
  });

  it('renders waitlisted status with correct styling', () => {
    render(<StatusBadge status="waitlisted" />);
    
    const badge = screen.getByText('Waitlisted');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-orange-100', 'text-orange-800');
  });

  it('has correct base classes', () => {
    render(<StatusBadge status="joined" />);
    
    const badge = screen.getByText('Joined');
    expect(badge).toHaveClass('inline-block', 'px-2', 'py-1', 'text-xs', 'font-medium', 'rounded');
  });
});
