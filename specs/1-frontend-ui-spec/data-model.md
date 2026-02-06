# Data Model: Premium Todo Application Frontend UI

**Feature**: 1-frontend-ui-spec
**Date**: 2026-01-26

## UI State Models

### Theme State
- **Model**: ThemeConfig
- **Fields**:
  - mode: "light" | "dark" | "system" (default: "system")
  - isDark: boolean (derived from mode and system preference)
  - mounted: boolean (tracking initialization state)

### User Session State
- **Model**: UserSession
- **Fields**:
  - isAuthenticated: boolean
  - user: User | null
  - loading: boolean
  - error: string | null

### Task UI State
- **Model**: TaskUIState
- **Fields**:
  - id: string
  - title: string
  - description: string
  - completed: boolean
  - createdAt: Date
  - updatedAt: Date
  - isEditing: boolean
  - isDeleting: boolean
  - error: string | null

### Form State
- **Model**: FormState
- **Fields**:
  - isValid: boolean
  - isSubmitting: boolean
  - errors: Record<string, string[]>
  - touched: Record<string, boolean>

### Loading State
- **Model**: LoadingState
- **Fields**:
  - isLoading: boolean
  - isIdle: boolean
  - isSuccess: boolean
  - isError: boolean
  - data: any | null
  - error: Error | null

## UI Component Props

### Button Component
- **Props**:
  - variant: "primary" | "secondary" | "ghost" | "outline" | "destructive"
  - size: "sm" | "md" | "lg"
  - disabled: boolean
  - loading: boolean
  - children: ReactNode
  - className?: string

### Input Component
- **Props**:
  - id: string
  - name: string
  - value: string
  - onChange: (value: string) => void
  - error?: string
  - label?: string
  - placeholder?: string
  - type?: "text" | "email" | "password" | "tel" | "url"
  - required?: boolean

### Task Card Component
- **Props**:
  - task: TaskUIState
  - onToggle: (id: string) => void
  - onEdit: (id: string) => void
  - onDelete: (id: string) => void
  - className?: string

### Task Form Component
- **Props**:
  - task?: Partial<TaskUIState>
  - onSubmit: (task: Partial<TaskUIState>) => void
  - onCancel?: () => void
  - className?: string

## UI Validation Rules

### Task Validation
- Title must be 1-100 characters
- Description must be 0-500 characters
- Completed status must be boolean
- Created/updated dates must be valid ISO strings

### Form Validation
- Email fields must match email format
- Password fields must meet strength requirements (8+ chars, mixed case, number, symbol)
- Required fields must not be empty
- Field values must pass type validation

### User Input Validation
- Prevent XSS by sanitizing user input
- Validate and sanitize form submissions
- Implement rate limiting for form submissions

## State Transition Flows

### Theme Switching Flow
1. User selects theme preference
2. Theme context updates
3. CSS custom properties change
4. All components re-render with new theme
5. Preference saved to localStorage

### Task Creation Flow
1. User clicks "Add Task" button
2. Task form appears with empty fields
3. User fills in task details
4. Form validation runs
5. If valid, task is submitted to API
6. Loading state activates
7. On success, task appears in list
8. Form clears and hides

### Task Editing Flow
1. User clicks edit button on task
2. Task form appears pre-filled with current values
3. User modifies task details
4. Form validation runs
5. If valid, task is submitted to API
6. Loading state activates
7. On success, task updates in list
8. Edit mode exits

### Authentication Flow
1. User visits protected page
2. Auth check runs
3. If not authenticated, redirect to login
4. User enters credentials
5. Auth request sent to API
6. On success, session established
7. User redirected to intended page