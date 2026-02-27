import { useEffect, useState } from 'react';
import { fetchWorkshops } from '../lib/api';
import WorkshopCard from './WorkshopCard';

interface Workshop {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'ongoing' | 'completed';
  signup_enabled: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * WorkshopList component displays all workshops from the API
 * Handles loading and error states
 */
export default function WorkshopList() {
  const [workshops, setWorkshops] = useState<Workshop[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const loadWorkshops = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await fetchWorkshops();
        setWorkshops(data);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'An error occurred while fetching workshops';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    loadWorkshops();
  }, []);

  // Loading state
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="text-gray-600">Loading workshops...</div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="text-red-600 bg-red-50 border border-red-200 rounded-lg p-4">
          {error}
        </div>
      </div>
    );
  }

  // Empty state
  if (workshops.length === 0) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="text-gray-500">No workshops available</div>
      </div>
    );
  }

  // Workshop list
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {workshops.map((workshop) => (
        <WorkshopCard key={workshop.id} workshop={workshop} />
      ))}
    </div>
  );
}
