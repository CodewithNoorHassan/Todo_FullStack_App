// Theme configuration and management utilities

// Define theme constants
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system'
} as const;

export type Theme = keyof typeof THEMES;

// Spacing scale following design system (4px base unit)
export const SPACING = {
  xs: '0.25rem', // 4px
  sm: '0.5rem',  // 8px
  md: '1rem',    // 16px
  lg: '1.5rem',  // 24px
  xl: '2rem',    // 32px
  '2xl': '3rem', // 48px
  '3xl': '4rem', // 64px
} as const;

// Breakpoints for responsive design
export const BREAKPOINTS = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const;

// Transition timing for smooth animations
export const TRANSITIONS = {
  ease: 'ease',
  easeIn: 'ease-in',
  easeOut: 'ease-out',
  easeInOut: 'ease-in-out',
  durationFast: '150ms',
  durationNormal: '250ms',
  durationSlow: '350ms',
} as const;

// Reduced motion support
export const REDUCED_MOTION = '(prefers-reduced-motion: reduce)';