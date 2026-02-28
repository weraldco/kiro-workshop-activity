/**
 * Add Material Modal Component
 */
import React, { useState } from 'react';
import { lessonApi } from '../../lib/lessons';
import type { CreateMaterialData } from '../../types/lesson';

interface AddMaterialModalProps {
  lessonId: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const AddMaterialModal: React.FC<AddMaterialModalProps> = ({ lessonId, isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState<CreateMaterialData>({
    material_type: 'video',
    title: '',
    url: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await lessonApi.addMaterial(lessonId, formData);
      setFormData({ material_type: 'video', title: '', url: '' });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to add material');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const value = e.target.type === 'number' ? parseInt(e.target.value) : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Add Material</h2>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-4">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-sm text-red-600">
              {error}
            </div>
          )}

          <div className="mb-4">
            <label htmlFor="material_type" className="block text-sm font-medium text-gray-700 mb-1">
              Material Type *
            </label>
            <select
              id="material_type"
              name="material_type"
              value={formData.material_type}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="video">Video</option>
              <option value="pdf">PDF Document</option>
              <option value="link">External Link</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              maxLength={200}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Material title"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-1">
              URL *
            </label>
            <input
              type="url"
              id="url"
              name="url"
              value={formData.url}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://..."
            />
            <p className="text-xs text-gray-500 mt-1">
              {formData.material_type === 'video' && 'YouTube, Vimeo, or direct video URL'}
              {formData.material_type === 'pdf' && 'Direct link to PDF file'}
              {formData.material_type === 'link' && 'Any external resource URL'}
            </p>
          </div>

          {formData.material_type === 'video' && (
            <div className="mb-4">
              <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-1">
                Duration (seconds)
              </label>
              <input
                type="number"
                id="duration"
                name="duration"
                value={formData.duration || ''}
                onChange={handleChange}
                min={0}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., 1800 for 30 minutes"
              />
            </div>
          )}

          {formData.material_type === 'pdf' && (
            <div className="mb-4">
              <label htmlFor="file_size" className="block text-sm font-medium text-gray-700 mb-1">
                File Size (bytes)
              </label>
              <input
                type="number"
                id="file_size"
                name="file_size"
                value={formData.file_size || ''}
                onChange={handleChange}
                min={0}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., 2048000 for 2MB"
              />
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add Material'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddMaterialModal;
