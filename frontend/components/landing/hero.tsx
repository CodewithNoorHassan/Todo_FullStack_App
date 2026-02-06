'use client';

import { Button } from '@/components/ui/button';
import Link from 'next/link';

export function HeroSection() {
  return (
    <section className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-4xl md:text-6xl font-bold mb-6">
        Premium Task Management
      </h1>
      <p className="text-xl text-muted-foreground mb-8 max-w-2xl">
        Experience the most sophisticated and elegant way to manage your tasks.
        Designed for professionals who demand excellence.
      </p>
      <div className="flex gap-4">
        <Button asChild>
          <Link href="/signup">Get Started</Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href="/signin">Sign In</Link>
        </Button>
      </div>
    </section>
  );
}