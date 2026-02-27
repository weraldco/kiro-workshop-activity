interface Workshop {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'ongoing' | 'completed';
  signup_enabled: boolean;
  created_at: string;
  updated_at: string;
}

interface WorkshopCardProps {
  workshop: Workshop;
}

/**
 * WorkshopCard component displays individual workshop information
 * with status-specific styling and signup availability indicator
 */
export default function WorkshopCard({ workshop }: WorkshopCardProps) {
  // Determine status-specific styling
  const getStatusStyles = (status: Workshop['status']) => {
    switch (status) {
      case 'pending':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'ongoing':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'completed':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const statusStyles = getStatusStyles(workshop.status);

  return (
    <div className="border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      {/* Workshop Title */}
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        {workshop.title}
      </h3>

      {/* Workshop Description */}
      <p className="text-gray-600 mb-4">
        {workshop.description}
      </p>

      {/* Status and Signup Availability */}
      <div className="flex items-center gap-3">
        {/* Status Badge */}
        <span
          className={`px-3 py-1 rounded-full text-sm font-medium border ${statusStyles}`}
        >
          {workshop.status.charAt(0).toUpperCase() + workshop.status.slice(1)}
        </span>

        {/* Signup Availability Indicator */}
        {workshop.signup_enabled && workshop.status === 'pending' && (
          <span className="text-sm text-green-600 font-medium flex items-center gap-1">
            <svg
              className="w-4 h-4"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            Signups Open
          </span>
        )}

        {(!workshop.signup_enabled || workshop.status !== 'pending') && (
          <span className="text-sm text-gray-500 font-medium flex items-center gap-1">
            <svg
              className="w-4 h-4"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            Signups Closed
          </span>
        )}
      </div>
    </div>
  );
}
