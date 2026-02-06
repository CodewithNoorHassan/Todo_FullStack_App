'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '@/lib/api/api-client';

interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'TODO' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  created_at: string;
  updated_at: string;
}

interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  completion_percentage: number;
}

export function TaskOverview() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<DashboardStats>({ total_tasks: 0, completed_tasks: 0, completion_percentage: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        const dashboard = await apiClient.getDashboard();
        setStats(dashboard.stats);
        setTasks(dashboard.recent_tasks || []);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch dashboard:', err);
        setError('Failed to load dashboard data');
        // Fallback to empty state
        setStats({ total_tasks: 0, completed_tasks: 0, completion_percentage: 0 });
        setTasks([]);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  const completionRate = Math.round(stats.completion_percentage);

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div>
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-300 mb-2">
          Welcome Back!
        </h1>
        <p className="text-gray-400">Here's what you need to focus on today</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Tasks"
          value={stats.total_tasks}
          icon="📋"
          color="from-blue-600 to-blue-500"
          subtext="All your tasks"
        />
        <StatCard
          title="Completed"
          value={stats.completed_tasks}
          icon="✅"
          color="from-emerald-600 to-emerald-500"
          subtext={`${completionRate}% complete`}
        />
        <StatCard
          title="In Progress"
          value={stats.total_tasks - stats.completed_tasks}
          icon="⏳"
          color="from-indigo-600 to-indigo-500"
          subtext="Awaiting completion"
        />
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-400">
          {error}
        </div>
      )}

      {/* Tasks Section */}
      <div>
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-white mb-1">Recent Tasks</h2>
            <p className="text-gray-400">Manage and track your tasks efficiently</p>
          </div>
          <Link
            href="/tasks"
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium rounded-lg transition-all hover:shadow-lg hover:shadow-blue-500/50"
          >
            + New Task
          </Link>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center text-gray-400 py-8">
            Loading tasks...
          </div>
        )}

        {/* Tasks Grid */}
        {!loading && tasks.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map(task => (
              <TaskCard key={task.id} task={task} />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && tasks.length === 0 && (
          <div className="text-center text-gray-400 py-12 bg-blue-500/5 rounded-lg border border-blue-500/20">
            <p>No tasks yet. Create one to get started!</p>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="bg-blue-500/5 backdrop-blur-sm border border-blue-500/20 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickActionButton icon="📝" label="New Task" href="/tasks" />
          <QuickActionButton icon="👥" label="Projects" href="/projects" />
          <QuickActionButton icon="📊" label="Analytics" href="/analytics" />
          <QuickActionButton icon="⚙️" label="Settings" href="/settings" />
        </div>
      </div>
    </div>
  );
}

function StatCard({
  title,
  value,
  icon,
  color,
  subtext
}: {
  title: string;
  value: number;
  icon: string;
  color: string;
  subtext: string;
}) {
  return (
    <div className={`bg-gradient-to-br ${color} p-0.5 rounded-xl`}>
      <div className="bg-slate-900 rounded-xl p-6 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium mb-1">{title}</p>
            <p className="text-4xl font-bold text-white">{value}</p>
            <p className="text-xs text-gray-500 mt-2">{subtext}</p>
          </div>
          <div className="text-5xl">{icon}</div>
        </div>
      </div>
    </div>
  );
}

function TaskCard({ task }: { task: Task }) {
  const isCompleted = task.status === 'COMPLETED';
  const statusLabel = {
    TODO: '📝 Todo',
    IN_PROGRESS: '⏳ In Progress',
    COMPLETED: '✅ Completed',
    BLOCKED: '🚫 Blocked'
  }[task.status] || task.status;

  return (
    <div className="group bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 hover:border-slate-600/50 transition-all hover:shadow-lg hover:shadow-purple-500/10">
      {/* Checkbox */}
      <div className="flex items-start space-x-4">
        <input
          type="checkbox"
          defaultChecked={isCompleted}
          className="w-5 h-5 mt-1 cursor-pointer accent-purple-500 rounded"
        />
        <div className="flex-1 min-w-0">
          <h3
            className={`font-semibold text-lg truncate transition-colors ${
              isCompleted ? 'text-gray-500 line-through' : 'text-white group-hover:text-blue-300'
            }`}
          >
            {task.title}
          </h3>
          <p className="text-gray-400 text-sm mt-1 line-clamp-2">{task.description}</p>

          {/* Footer */}
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-slate-700/30">
            <span className="text-xs text-gray-500">
              {new Date(task.created_at).toLocaleDateString()}
            </span>
            <span className={`inline-flex items-center space-x-1 px-2 py-1 text-xs font-medium rounded-full ${
              isCompleted
                ? 'bg-green-500/20 text-green-400'
                : task.priority === 'URGENT'
                ? 'bg-red-500/20 text-red-400'
                : task.priority === 'HIGH'
                ? 'bg-orange-500/20 text-orange-400'
                : 'bg-blue-500/20 text-blue-400'
            }`}>
              {statusLabel}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

function QuickActionButton({
  icon,
  label,
  href
}: {
  icon: string;
  label: string;
  href: string;
}) {
  return (
    <Link
      href={href}
      className="flex flex-col items-center justify-center p-4 bg-slate-700/30 hover:bg-slate-600/50 border border-slate-600/30 rounded-lg transition-all hover:border-slate-500/50 group"
    >
      <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">{icon}</div>
      <span className="text-xs font-medium text-gray-300 text-center">{label}</span>
    </Link>
  );
}
