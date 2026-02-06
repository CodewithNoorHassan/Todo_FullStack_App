'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { DashboardLayout } from '@/components/dashboard/layout';
import { apiClient } from '@/lib/api/api-client';

interface Task {
  id: number;
  user_id: number;
  todo_id?: number | null;
  title: string;
  description?: string;
  status: 'TODO' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  due_date?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

interface Todo {
  id: number;
  title: string;
  description?: string;
}

const statusColors: Record<string, string> = {
  'TODO': 'bg-slate-600 text-slate-100',
  'IN_PROGRESS': 'bg-blue-600 text-blue-100',
  'COMPLETED': 'bg-green-600 text-green-100',
  'BLOCKED': 'bg-red-600 text-red-100',
};

const statusEmojis: Record<string, string> = {
  'TODO': '📝',
  'IN_PROGRESS': '⚙️',
  'COMPLETED': '✅',
  'BLOCKED': '🚫',
};

const priorityColors: Record<string, string> = {
  'LOW': 'bg-blue-500/20 text-blue-300',
  'MEDIUM': 'bg-yellow-500/20 text-yellow-300',
  'HIGH': 'bg-orange-500/20 text-orange-300',
  'URGENT': 'bg-red-500/20 text-red-300',
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [creating, setCreating] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    todoId: '',
    priority: 'MEDIUM',
    dueDate: '',
  });
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: '',
  });
  const [skip, setSkip] = useState(0);
  const limit = 20;

  useEffect(() => {
    const loadData = async () => {
      await fetchProjects();
      await fetchTasks();
    };
    loadData();
  }, [filters, skip]);

  const fetchProjects = async () => {
    try {
      const response = await apiClient.getTodos(0, 1000);
      setProjects(response.todos || []);
    } catch (err) {
      console.error('Failed to fetch projects:', err);
    }
  };

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTasks(skip, limit, {
        status: filters.status || undefined,
        priority: filters.priority || undefined,
        search: filters.search || undefined,
      });
      setTasks(response.tasks || []);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
      setError('Failed to load tasks');
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!formData.title.trim()) {
      setError('Task title is required');
      return;
    }
    // project selection is optional now

    try {
      setCreating(true);
      setError(null);
      
      const taskPayload: any = {
        title: formData.title.trim(),
        priority: formData.priority as any,
        status: 'TODO',
      };
      
      // Only add optional fields if they have values
      if (formData.description?.trim()) {
        taskPayload.description = formData.description.trim();
      }
      
      if (formData.todoId) {
        taskPayload.todo_id = parseInt(formData.todoId);
      }
      
      if (formData.dueDate) {
        taskPayload.due_date = new Date(formData.dueDate).toISOString();
      }
      
      console.log('Creating task with payload:', taskPayload);
      
      const response = await apiClient.createTask(taskPayload);
      console.log('Task created successfully:', response);
      
      // Reset form
      setFormData({ title: '', description: '', todoId: '', priority: 'MEDIUM', dueDate: '' });
      setShowForm(false);
      setSkip(0);
      
      // Fetch updated tasks list
      await fetchTasks();
      setError(null);
    } catch (err: any) {
      console.error('Failed to create task:', err);
      let errorMessage = 'Failed to create task. Please try again.';
      
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

  const handleStatusToggle = async (task: Task) => {
    try {
      const newStatus = task.status === 'COMPLETED' ? 'TODO' : 'COMPLETED';
      await apiClient.updateTask(task.id, { status: newStatus });
      await fetchTasks();
    } catch (err) {
      console.error('Failed to update task:', err);
      setError('Failed to update task');
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
      await apiClient.deleteTask(taskId);
      await fetchTasks();
    } catch (err) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete task');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-300 mb-2">
              All Tasks
            </h1>
            <p className="text-gray-400">Manage and organize your work efficiently</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl active:scale-95 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Task
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

        {/* Create Task Form Modal */}
        {showForm && (
          <div className="bg-gradient-to-br from-blue-500/5 to-indigo-500/5 rounded-2xl backdrop-blur-xl border border-blue-500/30 shadow-2xl p-8 space-y-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-300">Create New Task</h2>
              <button
                onClick={() => setShowForm(false)}
                className="text-gray-400 hover:text-gray-300 transition-colors p-2 hover:bg-slate-700/50 rounded-lg"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Task Title */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-blue-100">Task Title</label>
              <input
                type="text"
                placeholder="What needs to be done?"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
                className="w-full px-4 py-3 bg-slate-700/50 border border-blue-500/30 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              />
            </div>

            {/* Description */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-blue-100">Description (optional)</label>
              <textarea
                placeholder="Add more details..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-3 bg-slate-700/50 border border-blue-500/30 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all resize-none"
                rows={4}
              />
            </div>

            {/* Project Selection */}
            {projects.length === 0 ? (
              <div className="space-y-2">
                <label className="text-sm font-semibold text-blue-100">Project</label>
                <div className="text-sm text-gray-400">
                  No projects available.{' '}
                  <Link href="/projects" className="text-blue-300 underline">
                    Create a project
                  </Link>{' '}
                  first to assign tasks.
                </div>
              </div>
            ) : (
              <div className="space-y-2">
                <label className="text-sm font-semibold text-blue-100">Project</label>
                <select
                  value={formData.todoId}
                  onChange={(e) => setFormData({ ...formData, todoId: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-blue-500/30 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                >
                  <option value="">Select a project...</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.title}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Priority & Due Date */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-blue-100">Priority</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-purple-500/30 rounded-xl text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
                >
                  <option value="LOW">Low Priority</option>
                  <option value="MEDIUM">Medium Priority</option>
                  <option value="HIGH">High Priority</option>
                  <option value="URGENT">Urgent</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-purple-100">Due Date</label>
                <input
                  type="date"
                  value={formData.dueDate}
                  onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-purple-500/30 rounded-xl text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
                />
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={handleCreate}
                disabled={creating}
                className="flex-1 py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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
                    <span>Create Task</span>
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-6 py-3 bg-slate-700/50 hover:bg-slate-600/50 border border-blue-500/30 text-white font-semibold rounded-xl transition-all"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex gap-3 flex-wrap">
          <select
            value={filters.status}
            onChange={(e) => {
              setFilters({ ...filters, status: e.target.value });
              setSkip(0);
            }}
            className="px-4 py-2 bg-slate-700/50 border border-purple-500/30 text-white rounded-lg focus:outline-none focus:border-purple-500 text-sm"
          >
            <option value="">All Status</option>
            <option value="TODO">To Do</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="COMPLETED">Completed</option>
            <option value="BLOCKED">Blocked</option>
          </select>

          <select
            value={filters.priority}
            onChange={(e) => {
              setFilters({ ...filters, priority: e.target.value });
              setSkip(0);
            }}
            className="px-4 py-2 bg-slate-700/50 border border-purple-500/30 text-white rounded-lg focus:outline-none focus:border-purple-500 text-sm"
          >
            <option value="">All Priorities</option>
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="URGENT">Urgent</option>
          </select>

          <input
            type="text"
            placeholder="Search tasks..."
            value={filters.search}
            onChange={(e) => {
              setFilters({ ...filters, search: e.target.value });
              setSkip(0);
            }}
            className="px-4 py-2 bg-slate-700/50 border border-purple-500/30 text-white placeholder-slate-400 rounded-lg focus:outline-none focus:border-purple-500 text-sm flex-1"
          />
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-12">
            <svg className="w-12 h-12 text-purple-500 animate-spin mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <p className="text-gray-400">Loading tasks...</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && tasks.length === 0 && (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 mb-4">
              <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-gray-300 text-lg font-semibold mb-2">No tasks found</p>
            <p className="text-gray-400 text-sm">Create your first task to get started</p>
          </div>
        )}

        {/* Tasks List */}
        {!loading && tasks.length > 0 && (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="bg-gradient-to-br from-slate-800/40 to-slate-800/20 border border-purple-500/20 hover:border-purple-500/50 rounded-xl p-4 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/10"
              >
                <div className="flex items-start justify-between gap-4">
                  {/* Checkbox & Content */}
                  <div className="flex items-start gap-4 flex-1">
                    <button
                      onClick={() => handleStatusToggle(task)}
                      className={`w-6 h-6 rounded-md mt-1 flex items-center justify-center flex-shrink-0 transition-all ${
                        task.status === 'COMPLETED'
                          ? 'bg-green-600 text-white'
                          : 'bg-slate-700/50 hover:bg-slate-600/50 border border-purple-500/30'
                      }`}
                    >
                      {task.status === 'COMPLETED' && (
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </button>

                    <div className="flex-1 min-w-0">
                      <h3
                        className={`font-semibold text-lg transition-colors ${
                          task.status === 'COMPLETED'
                            ? 'line-through text-gray-500'
                            : 'text-white'
                        }`}
                      >
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-gray-400 text-sm mt-1 line-clamp-2">
                          {task.description}
                        </p>
                      )}
                      <div className="flex gap-2 mt-3 flex-wrap">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            statusColors[task.status]
                          }`}
                        >
                          {statusEmojis[task.status]} {task.status.replace('_', ' ')}
                        </span>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            priorityColors[task.priority]
                          }`}
                        >
                          {task.priority}
                        </span>
                        {task.due_date && (
                          <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-700/50 border border-purple-500/30 text-gray-300">
                            📅 {new Date(task.due_date).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 ml-4 flex-shrink-0">
                    <Link
                      href={`/tasks/${task.id}`}
                      className="px-4 py-2 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-purple-300 hover:text-purple-200 rounded-lg text-sm font-medium transition-all"
                    >
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-500/30 text-red-300 hover:text-red-200 rounded-lg text-sm font-medium transition-all"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {!loading && tasks.length > 0 && tasks.length >= limit && (
          <div className="flex justify-center items-center gap-4 mt-8">
            <button
              onClick={() => setSkip(Math.max(0, skip - limit))}
              disabled={skip === 0}
              className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 disabled:bg-slate-800/50 disabled:text-gray-600 border border-purple-500/30 text-white rounded-lg transition-all font-semibold"
            >
              ← Previous
            </button>
            <span className="px-6 py-2 text-gray-300 font-semibold">
              Page {Math.floor(skip / limit) + 1}
            </span>
            <button
              onClick={() => setSkip(skip + limit)}
              disabled={tasks.length < limit}
              className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 disabled:bg-slate-800/50 disabled:text-gray-600 border border-purple-500/30 text-white rounded-lg transition-all font-semibold"
            >
              Next →
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
