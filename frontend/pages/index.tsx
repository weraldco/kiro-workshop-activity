import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';

export default function Home() {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-blue-600">
              Workshop Manager
            </Link>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <span className="text-sm text-gray-700">
                    Hello, <span className="font-medium">{user?.name}</span>
                  </span>
                  <Link
                    href="/dashboard"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Dashboard
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/auth/signin"
                    className="text-sm font-medium text-gray-700 hover:text-gray-900"
                  >
                    Sign in
                  </Link>
                  <Link
                    href="/auth/signup"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Sign up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Welcome to Workshop Manager
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Create, manage, and join workshops with ease
          </p>
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => router.push('/workshops')}
              className="px-8 py-3 text-lg font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 shadow-lg"
            >
              Browse Workshops
            </button>
            {isAuthenticated ? (
              <button
                onClick={() => router.push('/dashboard')}
                className="px-8 py-3 text-lg font-medium text-blue-600 bg-white rounded-lg hover:bg-gray-50 shadow-lg"
              >
                Go to Dashboard
              </button>
            ) : (
              <button
                onClick={() => router.push('/auth/signup')}
                className="px-8 py-3 text-lg font-medium text-blue-600 bg-white rounded-lg hover:bg-gray-50 shadow-lg"
              >
                Get Started
              </button>
            )}
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-blue-600 text-3xl mb-4">📚</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Create Workshops</h3>
            <p className="text-gray-600">
              Easily create and manage your own workshops with full control over participants and settings.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-blue-600 text-3xl mb-4">👥</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Manage Participants</h3>
            <p className="text-gray-600">
              Review join requests, approve participants, and manage your workshop community.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-blue-600 text-3xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Join & Learn</h3>
            <p className="text-gray-600">
              Browse available workshops and join the ones that interest you with a single click.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
