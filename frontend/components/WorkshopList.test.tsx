import { render, screen, waitFor } from '@testing-library/react';
import WorkshopList from './WorkshopList';
import * as api from '../lib/api';

// Mock the API module
jest.mock('../lib/api');

describe('WorkshopList', () => {
  const mockWorkshops = [
    {
      id: '1',
      title: 'Workshop 1',
      description: 'Description 1',
      status: 'pending' as const,
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
    {
      id: '2',
      title: 'Workshop 2',
      description: 'Description 2',
      status: 'ongoing' as const,
      signup_enabled: false,
      created_at: '2024-01-02T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
    },
    {
      id: '3',
      title: 'Workshop 3',
      description: 'Description 3',
      status: 'completed' as const,
      signup_enabled: false,
      created_at: '2024-01-03T00:00:00Z',
      updated_at: '2024-01-03T00:00:00Z',
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Loading State', () => {
    it('should display loading message while fetching workshops', () => {
      // Mock API to never resolve
      (api.fetchWorkshops as jest.Mock).mockImplementation(
        () => new Promise(() => {})
      );

      render(<WorkshopList />);
      expect(screen.getByText('Loading workshops...')).toBeInTheDocument();
    });
  });

  describe('Successful Data Fetching', () => {
    it('should fetch and display workshops on mount', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue(mockWorkshops);

      render(<WorkshopList />);

      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.queryByText('Loading workshops...')).not.toBeInTheDocument();
      });

      // Verify all workshops are displayed
      expect(screen.getByText('Workshop 1')).toBeInTheDocument();
      expect(screen.getByText('Workshop 2')).toBeInTheDocument();
      expect(screen.getByText('Workshop 3')).toBeInTheDocument();
    });

    it('should render WorkshopCard for each workshop', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue(mockWorkshops);

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.queryByText('Loading workshops...')).not.toBeInTheDocument();
      });

      // Verify descriptions are displayed (WorkshopCard renders them)
      expect(screen.getByText('Description 1')).toBeInTheDocument();
      expect(screen.getByText('Description 2')).toBeInTheDocument();
      expect(screen.getByText('Description 3')).toBeInTheDocument();
    });

    it('should call fetchWorkshops once on mount', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue(mockWorkshops);

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.queryByText('Loading workshops...')).not.toBeInTheDocument();
      });

      expect(api.fetchWorkshops).toHaveBeenCalledTimes(1);
    });
  });

  describe('Error Handling', () => {
    it('should display error message when API fails', async () => {
      const errorMessage = 'Failed to fetch workshops';
      (api.fetchWorkshops as jest.Mock).mockRejectedValue(new Error(errorMessage));

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText(errorMessage)).toBeInTheDocument();
      });

      // Verify loading is no longer displayed
      expect(screen.queryByText('Loading workshops...')).not.toBeInTheDocument();
    });

    it('should display generic error message for non-Error objects', async () => {
      (api.fetchWorkshops as jest.Mock).mockRejectedValue('String error');

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('An error occurred while fetching workshops')).toBeInTheDocument();
      });
    });

    it('should not display workshops when error occurs', async () => {
      (api.fetchWorkshops as jest.Mock).mockRejectedValue(new Error('API Error'));

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('API Error')).toBeInTheDocument();
      });

      // Verify no workshop titles are displayed
      expect(screen.queryByText('Workshop 1')).not.toBeInTheDocument();
      expect(screen.queryByText('Workshop 2')).not.toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('should display empty message when no workshops are returned', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue([]);

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('No workshops available')).toBeInTheDocument();
      });

      // Verify loading is no longer displayed
      expect(screen.queryByText('Loading workshops...')).not.toBeInTheDocument();
    });
  });

  describe('Component State Management', () => {
    it('should clear error state when successfully fetching after error', async () => {
      // First render with error
      (api.fetchWorkshops as jest.Mock).mockRejectedValue(new Error('Initial error'));

      const { rerender } = render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('Initial error')).toBeInTheDocument();
      });

      // Mock successful response for rerender
      (api.fetchWorkshops as jest.Mock).mockResolvedValue(mockWorkshops);

      // Force re-mount to trigger useEffect again
      rerender(<WorkshopList key="new" />);

      await waitFor(() => {
        expect(screen.queryByText('Initial error')).not.toBeInTheDocument();
        expect(screen.getByText('Workshop 1')).toBeInTheDocument();
      });
    });

    it('should maintain workshops state after successful fetch', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue(mockWorkshops);

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('Workshop 1')).toBeInTheDocument();
      });

      // Verify all workshops remain displayed
      expect(screen.getByText('Workshop 1')).toBeInTheDocument();
      expect(screen.getByText('Workshop 2')).toBeInTheDocument();
      expect(screen.getByText('Workshop 3')).toBeInTheDocument();
    });
  });

  describe('Grid Layout', () => {
    it('should render workshops in a grid layout', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue(mockWorkshops);

      const { container } = render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.queryByText('Loading workshops...')).not.toBeInTheDocument();
      });

      // Verify grid container exists
      const gridContainer = container.querySelector('.grid');
      expect(gridContainer).toBeInTheDocument();
      expect(gridContainer).toHaveClass('grid-cols-1', 'md:grid-cols-2', 'lg:grid-cols-3');
    });
  });

  describe('Edge Cases', () => {
    it('should handle single workshop', async () => {
      (api.fetchWorkshops as jest.Mock).mockResolvedValue([mockWorkshops[0]]);

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('Workshop 1')).toBeInTheDocument();
      });

      expect(screen.queryByText('Workshop 2')).not.toBeInTheDocument();
    });

    it('should handle large number of workshops', async () => {
      const manyWorkshops = Array.from({ length: 50 }, (_, i) => ({
        id: `${i}`,
        title: `Workshop ${i}`,
        description: `Description ${i}`,
        status: 'pending' as const,
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      }));

      (api.fetchWorkshops as jest.Mock).mockResolvedValue(manyWorkshops);

      render(<WorkshopList />);

      await waitFor(() => {
        expect(screen.getByText('Workshop 0')).toBeInTheDocument();
      });

      // Verify first and last workshops are rendered
      expect(screen.getByText('Workshop 0')).toBeInTheDocument();
      expect(screen.getByText('Workshop 49')).toBeInTheDocument();
    });
  });
});
