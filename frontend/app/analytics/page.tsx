'use client';

import { useEffect, useState } from 'react';
import { DashboardLayout } from '@/components/dashboard/layout';
import { apiClient } from '@/lib/api/api-client';

interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  completion_percentage: number;
  status_breakdown?: Record<string, number>;
  priority_breakdown?: Record<string, number>;
  overdue_tasks?: number;
  due_today?: number;
  total_todos?: number;
}

export default function AnalyticsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const dashboard = await apiClient.getDashboard();
        setStats(dashboard.stats);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch analytics:', err);
        setError('Failed to load analytics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading analytics...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !stats) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-red-400">{error || 'Failed to load analytics'}</p>
        </div>
      </DashboardLayout>
    );
  }

  const completionRate = Math.round(stats.completion_percentage);

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-300 mb-2">
            Analytics & Insights
          </h1>
          <p className="text-gray-400">Track your productivity and task management performance</p>
        </div>

        {/* Main Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Total Tasks */}
          <div className="bg-gradient-to-br from-blue-600/30 to-blue-500/10 border border-blue-500/40 rounded-xl p-6 hover:border-blue-400/60 transition-all hover:shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-300 font-medium">Total Tasks</h3>
              <span className="text-2xl">📋</span>
            </div>
            <p className="text-3xl font-bold text-blue-300">{stats.total_tasks}</p>
            <p className="text-xs text-gray-400 mt-2">Active tasks</p>
          </div>

          {/* Completed Tasks */}
          <div className="bg-gradient-to-br from-emerald-600/30 to-emerald-500/10 border border-emerald-500/40 rounded-xl p-6 hover:border-emerald-400/60 transition-all hover:shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-300 font-medium">Completed</h3>
              <span className="text-2xl">✅</span>
            </div>
            <p className="text-3xl font-bold text-emerald-300">{stats.completed_tasks}</p>
            <p className="text-xs text-gray-400 mt-2">Finished tasks</p>
          </div>

          {/* Completion Rate */}
          <div className="bg-gradient-to-br from-indigo-600/30 to-indigo-500/10 border border-indigo-500/40 rounded-xl p-6 hover:border-indigo-400/60 transition-all hover:shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-300 font-medium">Completion Rate</h3>
              <span className="text-2xl">📈</span>
            </div>
            <p className="text-3xl font-bold text-indigo-300">{completionRate}%</p>
            <div className="w-full bg-slate-700/50 rounded-full h-2 mt-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-indigo-400 to-indigo-600 h-full transition-all duration-500"
                style={{ width: `${completionRate}%` }}
              ></div>
            </div>
          </div>

          {/* Projects */}
          <div className="bg-gradient-to-br from-cyan-600/30 to-cyan-500/10 border border-cyan-500/40 rounded-xl p-6 hover:border-cyan-400/60 transition-all hover:shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-300 font-medium">Projects</h3>
              <span className="text-2xl">📁</span>
            </div>
            <p className="text-3xl font-bold text-cyan-300">{stats.total_todos || 0}</p>
            <p className="text-xs text-gray-400 mt-2">Active projects</p>
          </div>
        </div>

        {/* Secondary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Due Today */}
          <div className="bg-gradient-to-br from-amber-500/10 to-amber-500/5 border border-amber-500/30 rounded-xl p-6 hover:border-amber-500/50 transition-all">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">⏰</span>
              <h3 className="text-lg font-semibold text-white">Due Today</h3>
            </div>
            <p className="text-4xl font-bold text-amber-300">{stats.due_today || 0}</p>
            <p className="text-sm text-gray-400 mt-2">Tasks to complete today</p>
          </div>

          {/* Overdue Tasks */}
          <div className="bg-gradient-to-br from-red-500/10 to-red-500/5 border border-red-500/30 rounded-xl p-6 hover:border-red-500/50 transition-all">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">⚠️</span>
              <h3 className="text-lg font-semibold text-white">Overdue</h3>
            </div>
            <p className="text-4xl font-bold text-red-300">{stats.overdue_tasks || 0}</p>
            <p className="text-sm text-gray-400 mt-2">Past due tasks</p>
          </div>
        </div>

        {/* Detailed Breakdown */}
        {stats.status_breakdown && (
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-800/30 border border-slate-700/50 rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Task Status Breakdown</h3>
            <div className="space-y-4">
              {Object.entries(stats.status_breakdown).map(([status, count]) => (
                <div key={status} className="flex items-center justify-between">
                  <div className="flex items-center gap-3 flex-1">
                    <span className="text-sm font-medium text-gray-300 w-32 capitalize">{status}</span>
                    <div className="flex-1 bg-slate-700/50 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-400 to-blue-600 h-full transition-all duration-500"
                        style={{
                          width: `${
                            stats.total_tasks > 0
                              ? (count / stats.total_tasks) * 100
                              : 0
                          }%`,
                        }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-sm font-bold text-blue-300 ml-4 w-12 text-right">
                    {count}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Priority Breakdown */}
        {stats.priority_breakdown && (
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-800/30 border border-slate-700/50 rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Task Priority Breakdown</h3>
            <div className="space-y-4">
              {Object.entries(stats.priority_breakdown).map(([priority, count]) => {
                const priorityColors: Record<string, string> = {
                  'LOW': 'from-blue-400 to-blue-600',
                  'MEDIUM': 'from-yellow-400 to-yellow-600',
                  'HIGH': 'from-orange-400 to-orange-600',
                  'URGENT': 'from-red-400 to-red-600',
                };
                const bgColor = priorityColors[priority] || 'from-gray-400 to-gray-600';
                
                return (
                  <div key={priority} className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                      <span className="text-sm font-medium text-gray-300 w-32 capitalize">{priority}</span>
                      <div className="flex-1 bg-slate-700/50 rounded-full h-2 overflow-hidden">
                        <div
                          className={`bg-gradient-to-r ${bgColor} h-full transition-all duration-500`}
                          style={{
                            width: `${
                              stats.total_tasks > 0
                                ? (count / stats.total_tasks) * 100
                                : 0
                            }%`,
                          }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-sm font-bold text-gray-300 ml-4 w-12 text-right">
                      {count}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
