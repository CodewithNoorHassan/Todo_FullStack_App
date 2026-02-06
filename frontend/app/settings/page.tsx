'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/dashboard/layout';
import { useAuth } from '@/lib/api/auth-context';

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [emailDigest, setEmailDigest] = useState('weekly');
  const [theme, setTheme] = useState('dark');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
  const [avatarLoading, setAvatarLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
    applyTheme(savedTheme);
  }, []);

  const applyTheme = (themeName: string) => {
    const html = document.documentElement;
    html.classList.remove('light', 'dark');
    if (themeName === 'auto') {
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      html.classList.add(isDark ? 'dark' : 'light');
    } else {
      html.classList.add(themeName);
    }
  };

  const handleThemeChange = (newTheme: string) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
    setSuccessMessage('Theme updated successfully!');
    setTimeout(() => setSuccessMessage(''), 3000);
  };

  const handleAvatarUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setAvatarLoading(true);
    try {
      const reader = new FileReader();
      reader.onload = (event) => {
        const result = event.target?.result as string;
        setAvatarUrl(result);
        localStorage.setItem('userAvatar', result);
        setSuccessMessage('Avatar updated successfully!');
        setTimeout(() => setSuccessMessage(''), 3000);
      };
      reader.readAsDataURL(file);
    } catch (error) {
      console.error('Failed to upload avatar:', error);
    } finally {
      setAvatarLoading(false);
    }
  };

  useEffect(() => {
    const saved = localStorage.getItem('userAvatar');
    if (saved) setAvatarUrl(saved);
  }, []);

  return (
    <DashboardLayout>
      <div className="max-w-4xl space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-300 mb-2">
            Settings
          </h1>
          <p className="text-gray-400">Manage your account and preferences</p>
        </div>

        {successMessage && (
          <div className="flex items-center gap-3 p-4 bg-green-500/20 border border-green-500/50 rounded-xl">
            <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="text-sm text-green-200">{successMessage}</span>
          </div>
        )}

        {/* Profile Section */}
        <div className="bg-gradient-to-br from-blue-500/5 to-indigo-500/5 border border-blue-500/30 rounded-xl p-8">
          <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
            <span className="text-3xl">👤</span>
            Profile Information
          </h2>

          <div className="space-y-6">
            {/* Avatar */}
            <div className="flex items-center gap-6">
              <div className="relative group">
                <div className="w-20 h-20 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center text-white text-2xl font-bold overflow-hidden">
                  {avatarUrl ? (
                    <img src={avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                  ) : (
                    user?.name?.charAt(0)?.toUpperCase() || 'U'
                  )}
                </div>
                <label className="absolute inset-0 bg-black/50 rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center cursor-pointer transition-opacity">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarUpload}
                    className="hidden"
                    disabled={avatarLoading}
                  />
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </label>
              </div>
              <div>
                <p className="text-sm text-gray-400 mb-2">Profile Picture</p>
                <label className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition cursor-pointer inline-block">
                  {avatarLoading ? 'Uploading...' : 'Change Avatar'}
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarUpload}
                    className="hidden"
                    disabled={avatarLoading}
                  />
                </label>
              </div>
            </div>

            {/* User Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-blue-500/20">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
                <input
                  type="text"
                  defaultValue={user?.name || 'User'}
                  className="w-full px-4 py-2 bg-slate-700/50 border border-blue-500/30 rounded-lg text-white focus:border-blue-500 outline-none transition"
                  disabled
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                <input
                  type="email"
                  defaultValue={user?.email || ''}
                  className="w-full px-4 py-2 bg-slate-700/50 border border-blue-500/30 rounded-lg text-white focus:border-blue-500 outline-none transition"
                  disabled
                />
              </div>
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="bg-gradient-to-br from-indigo-500/5 to-cyan-500/5 border border-indigo-500/30 rounded-xl p-8">
          <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
            <span className="text-3xl">🔔</span>
            Notifications
          </h2>

          <div className="space-y-6">
            {/* Email Notifications */}
            <div className="flex items-center justify-between p-4 bg-indigo-500/10 rounded-lg border border-indigo-500/20 hover:border-indigo-500/40 transition">
              <div>
                <p className="font-medium text-white">Email Notifications</p>
                <p className="text-sm text-gray-400">Receive notifications via email</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={notificationsEnabled}
                  onChange={(e) => {
                    setNotificationsEnabled(e.target.checked);
                    setSuccessMessage('Notification preference saved!');
                    setTimeout(() => setSuccessMessage(''), 3000);
                  }}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
              </label>
            </div>

            {/* Email Digest */}
            <div className="p-4 bg-indigo-500/10 rounded-lg border border-indigo-500/20 hover:border-indigo-500/40 transition">
              <p className="font-medium text-white mb-3">Email Digest Frequency</p>
              <select
                value={emailDigest}
                onChange={(e) => {
                  setEmailDigest(e.target.value);
                  setSuccessMessage('Email digest preference saved!');
                  setTimeout(() => setSuccessMessage(''), 3000);
                }}
                className="w-full px-4 py-2 bg-slate-700/50 border border-indigo-500/30 rounded-lg text-white focus:border-indigo-500 outline-none transition"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="never">Never</option>
              </select>
            </div>

            {/* Task Reminders */}
            <div className="flex items-center justify-between p-4 bg-indigo-500/10 rounded-lg border border-indigo-500/20 hover:border-indigo-500/40 transition">
              <div>
                <p className="font-medium text-white">Task Reminders</p>
                <p className="text-sm text-gray-400">Remind me when tasks are due</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" defaultChecked className="sr-only peer" onChange={() => {}} />
                <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Appearance Settings */}
        <div className="bg-gradient-to-br from-cyan-500/5 to-blue-500/5 border border-cyan-500/30 rounded-xl p-8">
          <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
            <span className="text-3xl">🎨</span>
            Appearance
          </h2>

          <div>
            <p className="font-medium text-white mb-4">Theme</p>
            <div className="grid grid-cols-3 gap-4">
              {['light', 'dark', 'auto'].map((t) => (
                <button
                  key={t}
                  onClick={() => handleThemeChange(t)}
                  className={`p-4 rounded-lg border-2 transition capitalize font-medium ${
                    theme === t
                      ? 'border-blue-500 bg-blue-500/20 text-blue-300'
                      : 'border-slate-600 bg-slate-800/30 text-gray-300 hover:border-slate-500 hover:bg-slate-800/50'
                  }`}
                >
                  {t === 'light' && '☀️'} {t === 'dark' && '🌙'} {t === 'auto' && '🔄'} {t}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Danger Zone */}
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-8">
          <h2 className="text-2xl font-semibold text-red-400 mb-6 flex items-center gap-3">
            <span className="text-3xl">⚠️</span>
            Danger Zone
          </h2>

          <div className="space-y-4">
            <button className="w-full px-6 py-3 bg-red-600/20 hover:bg-red-600/30 border border-red-500/50 text-red-300 rounded-lg font-medium transition">
              Export My Data
            </button>

            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="w-full px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition"
            >
              Delete Account
            </button>
          </div>
        </div>

        {/* Logout Button */}
        <button
          onClick={logout}
          className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-lg font-medium transition"
        >
          Logout
        </button>

        {/* Delete Confirmation Modal */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-md w-full">
              <h3 className="text-xl font-bold text-white mb-3">Delete Account?</h3>
              <p className="text-gray-400 mb-6">
                This action cannot be undone. All your data will be permanently deleted.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="flex-1 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition"
                >
                  Cancel
                </button>
                <button className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition">
                  Delete
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
