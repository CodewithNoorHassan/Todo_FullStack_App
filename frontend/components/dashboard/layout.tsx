'use client';

import { ReactNode, useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/api/auth-context';

interface DashboardLayoutProps {
  children: ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);
  const { logout, user } = useAuth();
  
  // Load avatar from localStorage on mount
  useEffect(() => {
    setMounted(true);
    const saved = localStorage.getItem('userAvatar');
    if (saved) {
      setAvatarUrl(saved);
    }
  }, []);
  
  // Extract user info with fallbacks
  const userName = user?.name?.trim() || user?.email?.split('@')[0] || 'User';
  const userEmail = user?.email || 'user@example.com';
  const userInitials = userName
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || 'U';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 dark:from-slate-950 dark:via-blue-950 dark:to-slate-950">
      {/* Header */}
      <header className="border-b border-slate-700/30 backdrop-blur-md sticky top-0 z-40 bg-slate-900/80 dark:bg-slate-900/80">
        <div className="flex items-center justify-between px-4 md:px-8 py-4">
          {/* Logo */}
          <Link href="/dashboard" className="flex items-center space-x-2 hover:opacity-90 transition-opacity">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow">
              <span className="text-white font-bold text-lg">TM</span>
            </div>
            <span className="text-xl font-bold hidden sm:inline bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">
              TaskMaster
            </span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center space-x-1">
            <NavLink href="/dashboard">Dashboard</NavLink>
            <NavLink href="/tasks">Tasks</NavLink>
            <NavLink href="/analytics">Analytics</NavLink>
          </nav>

          {/* Right side - User Menu */}
          <div className="flex items-center space-x-4">
            {/* User Profile - Desktop */}
            <div className="hidden sm:flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-100 dark:text-gray-100 line-clamp-1">{userName}</p>
                <p className="text-xs text-gray-400 dark:text-gray-400 line-clamp-1">{userEmail}</p>
              </div>
              {mounted && avatarUrl ? (
                <img
                  src={avatarUrl}
                  alt={userName}
                  className="w-10 h-10 rounded-full flex-shrink-0 shadow-lg object-cover border-2 border-blue-500"
                  onError={() => setAvatarUrl(null)}
                />
              ) : (
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold text-sm flex-shrink-0 shadow-lg">
                  {userInitials}
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="md:hidden text-gray-400 hover:text-blue-400 transition-colors p-2 hover:bg-slate-800/50 rounded-lg dark:hover:bg-slate-800/50"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            {/* Settings Button */}
            <Link href="/settings">
              <button className="p-2 text-gray-400 hover:text-blue-400 hover:bg-slate-800/50 rounded-lg transition-all dark:hover:bg-slate-800/50">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </Link>

            {/* Logout Button */}
            <button
              onClick={logout}
              className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-red-500/20 rounded-lg transition-all border border-red-500/0 hover:border-red-500/30 dark:text-gray-300 dark:hover:text-white"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`${
          sidebarOpen ? 'block' : 'hidden'
        } md:block w-64 border-r border-slate-700/30 p-6 md:sticky md:top-20 md:h-[calc(100vh-80px)] overflow-y-auto bg-slate-900/40 backdrop-blur-sm dark:bg-slate-900/40`}>
          <nav className="space-y-2">
            <SidebarLink href="/dashboard" icon="📊">Dashboard</SidebarLink>
            <SidebarLink href="/tasks" icon="✓">My Tasks</SidebarLink>
            <SidebarLink href="/projects" icon="📁">Projects</SidebarLink>
            <SidebarLink href="/analytics" icon="📈">Analytics</SidebarLink>
            <SidebarLink href="/settings" icon="⚙️">Settings</SidebarLink>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-4 md:p-8 dark:bg-gradient-to-br dark:from-slate-950 dark:via-blue-950 dark:to-slate-950">
          {children}
        </main>
      </div>
    </div>
  );
}

function NavLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <Link
      href={href}
      className="px-4 py-2 text-gray-300 hover:text-white hover:bg-blue-500/10 rounded-lg transition-all font-medium text-sm"
    >
      {children}
    </Link>
  );
}

function SidebarLink({ href, icon, children }: { href: string; icon: string; children: ReactNode }) {
  return (
    <Link
      href={href}
      className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-blue-500/10 hover:text-white transition-all group font-medium"
    >
      <span className="text-lg group-hover:scale-110 transition-transform">{icon}</span>
      <span>{children}</span>
    </Link>
  );
}
