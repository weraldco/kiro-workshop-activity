import { render, screen } from '@testing-library/react';
import WorkshopCard from './WorkshopCard';

describe('WorkshopCard', () => {
  const baseWorkshop = {
    id: '123',
    title: 'Test Workshop',
    description: 'This is a test workshop description',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  describe('Workshop Information Display', () => {
    it('should display workshop title', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Test Workshop')).toBeInTheDocument();
    });

    it('should display workshop description', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('This is a test workshop description')).toBeInTheDocument();
    });

    it('should display workshop status', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'ongoing' as const,
        signup_enabled: false,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Ongoing')).toBeInTheDocument();
    });
  });

  describe('Status-Specific Styling', () => {
    it('should apply pending status styles', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      const statusBadge = screen.getByText('Pending');
      expect(statusBadge).toHaveClass('bg-blue-100', 'text-blue-800', 'border-blue-300');
    });

    it('should apply ongoing status styles', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'ongoing' as const,
        signup_enabled: false,
      };

      render(<WorkshopCard workshop={workshop} />);
      const statusBadge = screen.getByText('Ongoing');
      expect(statusBadge).toHaveClass('bg-green-100', 'text-green-800', 'border-green-300');
    });

    it('should apply completed status styles', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'completed' as const,
        signup_enabled: false,
      };

      render(<WorkshopCard workshop={workshop} />);
      const statusBadge = screen.getByText('Completed');
      expect(statusBadge).toHaveClass('bg-gray-100', 'text-gray-800', 'border-gray-300');
    });
  });

  describe('Signup Availability Indicator', () => {
    it('should show "Signups Open" when status is pending and signup_enabled is true', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Signups Open')).toBeInTheDocument();
      expect(screen.queryByText('Signups Closed')).not.toBeInTheDocument();
    });

    it('should show "Signups Closed" when status is pending but signup_enabled is false', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'pending' as const,
        signup_enabled: false,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Signups Closed')).toBeInTheDocument();
      expect(screen.queryByText('Signups Open')).not.toBeInTheDocument();
    });

    it('should show "Signups Closed" when status is ongoing', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'ongoing' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Signups Closed')).toBeInTheDocument();
      expect(screen.queryByText('Signups Open')).not.toBeInTheDocument();
    });

    it('should show "Signups Closed" when status is completed', () => {
      const workshop = {
        ...baseWorkshop,
        status: 'completed' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Signups Closed')).toBeInTheDocument();
      expect(screen.queryByText('Signups Open')).not.toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty description', () => {
      const workshop = {
        ...baseWorkshop,
        description: '',
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('Test Workshop')).toBeInTheDocument();
    });

    it('should handle long title', () => {
      const workshop = {
        ...baseWorkshop,
        title: 'A'.repeat(200),
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('A'.repeat(200))).toBeInTheDocument();
    });

    it('should handle long description', () => {
      const workshop = {
        ...baseWorkshop,
        description: 'B'.repeat(1000),
        status: 'pending' as const,
        signup_enabled: true,
      };

      render(<WorkshopCard workshop={workshop} />);
      expect(screen.getByText('B'.repeat(1000))).toBeInTheDocument();
    });
  });
});
