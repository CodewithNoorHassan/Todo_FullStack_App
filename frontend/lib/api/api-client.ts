// API Client for communicating with the FastAPI backend
import { toast } from 'sonner'; // Assuming we'll use sonner for notifications

// Define types for our API responses
interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
}

interface LoginResponse {
  user: User;
  token: string;
}

interface RegisterResponse {
  user: User;
  token: string;
}

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
  user_id: number;
  title: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

interface TodoListResponse {
  todos: Todo[];
  total: number;
  skip: number;
  limit: number;
}

interface TaskListResponse {
  tasks: Task[];
  total: number;
  skip: number;
  limit: number;
}

interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  completion_percentage: number;
  status_breakdown: Record<string, number>;
  priority_breakdown: Record<string, number>;
  overdue_tasks: number;
  due_today: number;
  total_todos: number;
}

interface DashboardResponse {
  stats: DashboardStats;
  recent_tasks: Task[];
  due_today: Task[];
  overdue: Task[];
}

// Base URL - in production this would come from environment variables
// During development, Next.js rewrites will proxy API calls to the backend
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = BASE_URL;
  }

  // Get stored token from localStorage
  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('auth_token');
  }

  // Store token in localStorage
  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  // Clear token from localStorage
  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add authorization header if token exists
    const token = this.getToken();
    if (token) {
      config.headers = {
        ...config.headers,
        'Authorization': `Bearer ${token}`,
      };
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      // Handle empty responses
      if (response.status === 204) {
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Authentication methods
  async login(credentials: { email: string; password: string }): Promise<LoginResponse> {
    const response = await this.request<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    // Store token on successful login
    if (response.token) {
      this.setToken(response.token);
    }
    return response;
  }

  async register(userData: { email: string; password: string; name?: string }): Promise<RegisterResponse> {
    const response = await this.request<RegisterResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    // Store token on successful registration
    if (response.token) {
      this.setToken(response.token);
    }
    return response;
  }

  async logout(): Promise<void> {
    try {
      await this.request('/api/auth/logout', {
        method: 'POST',
      });
    } finally {
      // Clear token regardless of API response
      this.clearToken();
    }
  }

  async getProfile(): Promise<User> {
    return this.request<User>('/api/auth/me');
  }

  // Task methods
  async getTasks(skip: number = 0, limit: number = 50, filters?: { todo_id?: number; status?: string; priority?: string; search?: string }): Promise<TaskListResponse> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
      ...(filters?.todo_id && { todo_id: filters.todo_id.toString() }),
      ...(filters?.status && { status: filters.status }),
      ...(filters?.priority && { priority: filters.priority }),
      ...(filters?.search && { search: filters.search }),
    });
    return this.request(`/api/tasks/?${params}`);
  }

  async getTask(id: number): Promise<Task> {
    return this.request(`/api/tasks/${id}`);
  }

  async createTask(taskData: { title: string; todo_id?: number; description?: string; status?: string; priority?: string; due_date?: string }): Promise<Task> {
    return this.request('/api/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: number, taskData: Partial<{ title: string; description?: string; status: string; priority: string; due_date?: string }>): Promise<Task> {
    return this.request(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: number): Promise<void> {
    await this.request(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  // Todo methods
  async getTodos(skip: number = 0, limit: number = 100): Promise<TodoListResponse> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    return this.request(`/api/todos?${params}`);
  }

  async getTodo(id: number): Promise<Todo> {
    return this.request(`/api/todos/${id}`);
  }

  async createTodo(todoData: { title: string; description?: string }): Promise<Todo> {
    return this.request('/api/todos', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  }

  async updateTodo(id: number, todoData: Partial<{ title: string; description: string }>): Promise<Todo> {
    return this.request(`/api/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  }

  async deleteTodo(id: number): Promise<void> {
    await this.request(`/api/todos/${id}`, {
      method: 'DELETE',
    });
  }

  // Dashboard methods
  async getDashboard(): Promise<DashboardResponse> {
    return this.request('/api/dashboard');
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request('/api/health');
  }
}

export const apiClient = new ApiClient();

// Export the class as well if needed elsewhere
export default ApiClient;