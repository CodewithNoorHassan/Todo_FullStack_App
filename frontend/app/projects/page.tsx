'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { DashboardLayout } from '@/components/dashboard/layout';
import { apiClient } from '@/lib/api/api-client';

interface Todo {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

interface TodoWithCount extends Todo {
  task_count?: number;
}

export default function ProjectsPage() {
  const [todos, setTodos] = useState<TodoWithCount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [skip, setSkip] = useState(0);
  const [totalTodos, setTotalTodos] = useState(0);
  const [formData, setFormData] = useState({ title: '', description: '' });
  const [creating, setCreating] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null);
  const limit = 20;

  useEffect(() => {
    fetchTodos();
  }, [skip]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTodos(skip, limit);
      setTodos(response.todos || []);
      setTotalTodos(response.total || 0);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch todos:', err);
      setError('Failed to load projects');
      setTodos([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!formData.title.trim()) {
      setError('Project title is required');
      return;
    }

    try {
      setCreating(true);
      setError(null);
      
      const todoPayload: any = {
        title: formData.title.trim(),
      };
      
      // Only add description if it has a value
      if (formData.description?.trim()) {
        todoPayload.description = formData.description.trim();
      }
      
      console.log('Creating project with payload:', todoPayload);
      
      const response = await apiClient.createTodo(todoPayload);
      console.log('Project created successfully:', response);
      
      setFormData({ title: '', description: '' });
      setShowForm(false);
      setSkip(0);
      await fetchTodos();
      setError(null);
    } catch (err: any) {
      console.error('Failed to create project:', err);
      let errorMessage = 'Failed to create project. Please try again.';
      
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (err?.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (typeof err === 'string') {
        errorMessage = err;
      }
      
      setError(errorMessage);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (todoId: number) => {
    try {
      await apiClient.deleteTodo(todoId);
      setDeleteConfirm(null);
      await fetchTodos();
    } catch (err) {
      console.error('Failed to delete todo:', err);
      setError('Failed to delete project');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-300 to-pink-300 mb-2">
              Projects
            </h1>
            <p className="text-gray-400">Organize and manage your projects</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl active:scale-95 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Project
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
            <svg className="w-5 h-5 text-red-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-sm text-red-200">{error}</span>
          </div>
        )}

        {/* Create Project Form Modal */}
        {showForm && (
          <div className="bg-gradient-to-br from-slate-800/40 to-slate-800/20 rounded-2xl backdrop-blur-xl border border-purple-500/20 shadow-2xl p-8 space-y-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Create New Project</h2>
              <button
                onClick={() => setShowForm(false)}
                className="text-gray-400 hover:text-gray-300 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Project Title */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-purple-100">Project Title</label>
              <input
                type="text"
                placeholder="My new project..."
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
                className="w-full px-4 py-3 bg-slate-700/50 border border-purple-500/30 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
              />
            </div>

            {/* Project Description */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-purple-100">Description (optional)</label>
              <textarea
                placeholder="Project description..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-3 bg-slate-700/50 border border-purple-500/30 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all resize-none"
                rows={4}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <button
                onClick={handleCreate}
                disabled={creating}
                className="flex-1 py-3 px-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {creating ? (
                  <>
                    <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>Creating...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    <span>Create Project</span>
                  </>
                )}
              </button>
              <button
                onClick={() => setShowForm(false)}
                className="px-6 py-3 bg-slate-700/50 hover:bg-slate-600/50 border border-purple-500/30 text-white font-semibold rounded-xl transition-all"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-12">
            <svg className="w-12 h-12 text-purple-500 animate-spin mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <p className="text-gray-400">Loading projects...</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && todos.length === 0 && (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 mb-4">
              <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-gray-300 text-lg font-semibold mb-2">No projects yet</p>
            <p className="text-gray-400 text-sm">Create your first project to get started</p>
          </div>
        )}

        {/* Projects Grid */}
        {!loading && todos.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {todos.map((todo) => (
              <div key={todo.id} className="group">
                <Link href={`/projects/${todo.id}`}>
                  <div className="bg-gradient-to-br from-slate-800/40 to-slate-800/20 border border-purple-500/20 hover:border-purple-500/50 rounded-2xl p-6 transition-all duration-300 cursor-pointer h-full hover:shadow-lg hover:shadow-purple-500/10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold text-white group-hover:text-purple-300 transition-colors line-clamp-2">
                          {todo.title}
                        </h3>
                        {todo.description && (
                          <p className="text-gray-400 text-sm mt-2 line-clamp-2">
                            {todo.description}
                          </p>
                        )}
                      </div>
                      <div className="ml-2 w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center flex-shrink-0">
                        <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="space-y-2 py-4 border-t border-purple-500/10">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Tasks</span>
                        <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full font-semibold text-xs">
                          {todo.task_count || 0}
                        </span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Created</span>
                        <span className="text-gray-300 text-xs">
                          {new Date(todo.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>

                {/* Delete Button */}
                <button
                  onClick={() => setDeleteConfirm(todo.id)}
                  className="mt-2 w-full px-3 py-2 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-300 hover:text-red-200 rounded-xl transition-all text-sm font-medium"
                >
                  Delete Project
                </button>

                {/* Delete Confirmation Modal */}
                {deleteConfirm === todo.id && (
                  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-slate-800 border border-purple-500/20 rounded-2xl p-8 max-w-sm mx-4 shadow-2xl">
                      <h3 className="text-xl font-bold text-white mb-2">Delete Project?</h3>
                      <p className="text-gray-400 text-sm mb-6">
                        This will permanently delete "{todo.title}" and all its tasks. This action cannot be undone.
                      </p>
                      <div className="flex gap-3">
                        <button
                          onClick={() => handleDelete(todo.id)}
                          className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition-all"
                        >
                          Delete
                        </button>
                        <button
                          onClick={() => setDeleteConfirm(null)}
                          className="flex-1 px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 border border-purple-500/30 text-white rounded-lg font-semibold transition-all"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {!loading && todos.length > 0 && totalTodos > limit && (
          <div className="flex justify-center items-center gap-4 mt-8">
            <button
              onClick={() => setSkip(Math.max(0, skip - limit))}
              disabled={skip === 0}
              className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 disabled:bg-slate-800/50 disabled:text-gray-600 border border-purple-500/30 text-white rounded-xl transition-all font-semibold"
            >
              ← Previous
            </button>
            <span className="px-6 py-2 text-gray-300 font-semibold">
              Page {Math.floor(skip / limit) + 1} of {Math.ceil(totalTodos / limit)}
            </span>
            <button
              onClick={() => setSkip(skip + limit)}
              disabled={skip + limit >= totalTodos}
              className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 disabled:bg-slate-800/50 disabled:text-gray-600 border border-purple-500/30 text-white rounded-xl transition-all font-semibold"
            >
              Next →
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
