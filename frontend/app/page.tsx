import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 flex flex-col">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 border-b border-slate-700/30">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center hover:shadow-lg transition-shadow">
            <span className="text-white font-bold text-lg">TM</span>
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">
            TaskMaster
          </span>
        </div>
        <div className="flex items-center space-x-4">
          <Link href="/signin" passHref={true}>
            <Button variant="ghost" className="text-gray-300 hover:text-blue-400 hover:bg-blue-500/10">
              Sign In
            </Button>
          </Link>
          <Link href="/signup" passHref={true}>
            <Button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white">
              Get Started
            </Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl w-full text-center">
          <div className="inline-block px-4 py-1 mb-4 rounded-full bg-blue-500/10 text-sm font-medium text-blue-300 border border-blue-500/30">
            Productivity Reimagined
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-300 via-indigo-300 to-cyan-300">
              Professional Task
            </span>
            <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-300">
              Management
            </span>
          </h1>
          <p className="text-lg md:text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
            Experience enterprise-grade task management with AI-powered insights, real-time collaboration, and seamless workflow automation. Designed for modern professionals.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup" passHref={true}>
              <Button size="lg" variant="default" className="px-8 py-6 text-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl shadow-lg hover:shadow-xl transition-all">
                Start Free Trial
              </Button>
            </Link>
            <Link href="/signin" passHref={true}>
              <Button size="lg" variant="outline" className="px-8 py-6 text-lg border-2 border-indigo-500/50 text-white rounded-xl hover:bg-indigo-500/10 hover:border-indigo-500 transition-all">
                Sign In to Account
              </Button>
            </Link>
          </div>

          {/* Features Preview */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="p-6 rounded-xl bg-blue-500/5 backdrop-blur-sm border border-blue-500/20 hover:border-blue-500/40 transition-all group">
              <div className="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center mb-4 mx-auto group-hover:bg-blue-500/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="font-semibold text-lg mb-2 text-white">Smart Prioritization</h3>
              <p className="text-gray-400 text-sm">AI-powered task prioritization based on deadlines and importance</p>
            </div>

            <div className="p-6 rounded-xl bg-indigo-500/5 backdrop-blur-sm border border-indigo-500/20 hover:border-indigo-500/40 transition-all group">
              <div className="w-12 h-12 rounded-lg bg-indigo-500/20 flex items-center justify-center mb-4 mx-auto group-hover:bg-indigo-500/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-semibold text-lg mb-2 text-white">Lightning Fast</h3>
              <p className="text-gray-400 text-sm">Optimized for speed with real-time synchronization</p>
            </div>

            <div className="p-6 rounded-xl bg-cyan-500/5 backdrop-blur-sm border border-cyan-500/20 hover:border-cyan-500/40 transition-all group">
              <div className="w-12 h-12 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-4 mx-auto group-hover:bg-cyan-500/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="font-semibold text-lg mb-2 text-white">Enterprise Security</h3>
              <p className="text-gray-400 text-sm">Bank-level encryption and privacy protection</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center text-sm text-gray-500 border-t border-slate-700/30">
        <p>© {new Date().getFullYear()} TaskMaster. All rights reserved.</p>
      </footer>
    </div>
  );
}