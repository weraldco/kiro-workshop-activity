/**
 * JoinButton Component Tests
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import JoinButton from '../JoinButton';
import * as workshopsLib from '../../../lib/workshops';

// Mock the workshops library
jest.mock('../../../lib/workshops');
const mockedWorkshopsLib = workshopsLib as jest.Mocked<typeof workshopsLib>;

// Mock window.alert
global.alert = jest.fn();

describe('JoinButton', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders join button when no participation status', () => {
    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus={null}
      />
    );
    
    expect(screen.getByRole('button', { name: /join/i })).toBeInTheDocument();
  });

  it('renders joined button when status is joined', () => {
    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus="joined"
      />
    );
    
    const button = screen.getByRole('button', { name: /joined/i });
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it('renders pending button when status is pending', () => {
    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus="pending"
      />
    );
    
    const button = screen.getByRole('button', { name: /pending/i });
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it('renders rejected button when status is rejected', () => {
    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus="rejected"
      />
    );
    
    const button = screen.getByRole('button', { name: /rejected/i });
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it('renders waitlisted button when status is waitlisted', () => {
    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus="waitlisted"
      />
    );
    
    const button = screen.getByRole('button', { name: /waitlisted/i });
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it('renders signup closed button when signup is disabled', () => {
    render(
      <JoinButton
        workshopId="123"
        signupEnabled={false}
        participationStatus={null}
      />
    );
    
    const button = screen.getByRole('button', { name: /signup closed/i });
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it('calls joinWorkshop when join button is clicked', async () => {
    mockedWorkshopsLib.joinWorkshop.mockResolvedValue({
      id: 'part-123',
      workshop_id: '123',
      user_id: 'user-123',
      status: 'pending',
      requested_at: new Date().toISOString(),
      approved_at: null,
      approved_by: null,
      user_name: 'Test User',
      user_email: 'test@example.com',
    });

    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus={null}
      />
    );
    
    const joinButton = screen.getByRole('button', { name: /join/i });
    fireEvent.click(joinButton);

    await waitFor(() => {
      expect(mockedWorkshopsLib.joinWorkshop).toHaveBeenCalledWith('123');
    });
  });

  it('calls onSuccess callback after successful join', async () => {
    const mockOnSuccess = jest.fn();
    mockedWorkshopsLib.joinWorkshop.mockResolvedValue({
      id: 'part-123',
      workshop_id: '123',
      user_id: 'user-123',
      status: 'pending',
      requested_at: new Date().toISOString(),
      approved_at: null,
      approved_by: null,
      user_name: 'Test User',
      user_email: 'test@example.com',
    });

    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus={null}
        onSuccess={mockOnSuccess}
      />
    );
    
    const joinButton = screen.getByRole('button', { name: /join/i });
    fireEvent.click(joinButton);

    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  it('shows alert on join failure', async () => {
    mockedWorkshopsLib.joinWorkshop.mockRejectedValue({
      response: {
        data: {
          error: 'Already joined',
        },
      },
    });

    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus={null}
      />
    );
    
    const joinButton = screen.getByRole('button', { name: /join/i });
    fireEvent.click(joinButton);

    await waitFor(() => {
      expect(global.alert).toHaveBeenCalledWith('Already joined');
    });
  });

  it('disables button while loading', async () => {
    mockedWorkshopsLib.joinWorkshop.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(
      <JoinButton
        workshopId="123"
        signupEnabled={true}
        participationStatus={null}
      />
    );
    
    const joinButton = screen.getByRole('button', { name: /join/i });
    fireEvent.click(joinButton);

    await waitFor(() => {
      expect(joinButton).toBeDisabled();
      expect(screen.getByText(/joining/i)).toBeInTheDocument();
    });
  });
});
