'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import { useAuth } from '@/lib/api/auth-context';
import { toast } from 'sonner';

type AuthMode = 'signin' | 'signup';

interface FormData {
  email: string;
  password: string;
  confirmPassword?: string;
  name?: string;
}

export function AuthForm({ mode }: { mode: AuthMode }) {
  const router = useRouter();
  const { login, register } = useAuth();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    confirmPassword: '',
    name: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (mode === 'signup') {
        // Validate passwords match
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setIsLoading(false);
          return;
        }

        // Validate required fields
        if (!formData.name || !formData.email || !formData.password) {
          setError('Please fill in all required fields');
          setIsLoading(false);
          return;
        }

        // Call register
        await register(formData.email, formData.password, formData.name);
        toast.success('Account created successfully!');
        router.push('/dashboard');
      } else {
        // Sign in mode
        if (!formData.email || !formData.password) {
          setError('Please enter email and password');
          setIsLoading(false);
          return;
        }

        await login(formData.email, formData.password);
        toast.success('Signed in successfully!');
        router.push('/dashboard');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Authentication failed. Please try again.';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Auth error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const title = mode === 'signin' ? 'Sign In' : 'Create Account';
  const submitText = mode === 'signin' ? 'Sign In' : 'Create Account';
  const toggleText = mode === 'signin'
    ? 'Need an account? Sign up'
    : 'Already have an account? Sign in';

  const toggleLink = mode === 'signin' ? '/signup' : '/signin';

  return (
    <Card className="border-border">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {mode === 'signup' && (
            <div>
              <label htmlFor="name" className="text-sm font-medium">Full Name</label>
              <Input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleChange}
                placeholder="John Doe"
                required
              />
            </div>
          )}
          <div>
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <Input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="name@example.com"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="text-sm font-medium">Password</label>
            <Input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </div>
          {mode === 'signup' && (
            <div>
              <label htmlFor="confirmPassword" className="text-sm font-medium">Confirm Password</label>
              <Input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                required
              />
            </div>
          )}
          {error && (
            <div className="text-red-500 text-sm">{error}</div>
          )}
        </CardContent>
        <CardFooter className="flex flex-col">
          <Button
            type="submit"
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : submitText}
          </Button>
          <div className="mt-4 text-center text-sm">
            <Link href={toggleLink} className="underline">
              {toggleText}
            </Link>
          </div>
        </CardFooter>
      </form>
    </Card>
  );
}