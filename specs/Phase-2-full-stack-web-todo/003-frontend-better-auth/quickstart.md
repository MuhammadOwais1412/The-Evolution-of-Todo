# Quickstart Guide: Frontend Application

**Feature**: 003-frontend-better-auth
**Date**: 2026-01-03

## Overview

This guide provides step-by-step instructions for implementing the Next.js frontend with Better Auth and REST API integration. Follow the ordered steps to build the frontend application from scratch.

---

## Prerequisites

1. **Node.js 20+** installed
2. **Backend API** running at `http://localhost:8000`
3. **Environment variables** configured for backend (see `Phase-2-web-todo/backend/.env`)
4. **Better Auth secret** shared between frontend and backend (`BETTER_AUTH_SECRET`)

---

## Step 1: Initialize Next.js Project

```bash
cd Phase-2-web-todo
npx create-next-app@16 frontend --typescript --tailwind --eslint --app --no-src --import-alias "@/*"
```

**Options Explanation**:
- `--typescript`: Enable TypeScript
- `--tailwind`: Enable Tailwind CSS
- `--eslint`: Enable ESLint
- `--app`: Use App Router (Next.js 16+)
- `--no-src`: Use `app/` at root (not `src/app/`)
- `--import-alias "@/*"`: Set import alias

**After creation**:
```bash
cd frontend
npm install
```

---

## Step 2: Install Dependencies

```bash
npm install better-auth zustand
npm install --save-dev @types/node
```

**Dependencies**:
- `better-auth`: Authentication library
- `zustand`: Lightweight state management (optional, or use React Context)
- `@types/node`: TypeScript types for Node.js

---

## Step 3: Configure Environment Variables

Create `Phase-2-web-todo/frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-shared-secret-here
BETTER_AUTH_URL=http://localhost:3000

# Better Auth JWT Configuration
NEXT_PUBLIC_BETTER_AUTH_JWT_ALGORITHM=HS256
NEXT_PUBLIC_BETTER_AUTH_JWT_EXPIRES_IN=7d
```

**Important**:
- `BETTER_AUTH_SECRET` must match backend `better_auth_secret` from `backend/.env`
- Backend API URL must be accessible from frontend (same origin or CORS enabled)

---

## Step 4: Configure TypeScript

Update `Phase-2-web-todo/frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

---

## Step 5: Configure Better Auth

Create `Phase-2-web-todo/frontend/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
  // Enable JWT token issuance
  session: {
    jwt: {
      enabled: true,
      expiresIn: process.env.NEXT_PUBLIC_BETTER_AUTH_JWT_EXPIRES_IN,
    },
  },
  // Token format must match backend expectations
  jwt: {
    algorithm: "HS256",
  },
});

export type Session = typeof auth.$Infer.Session;
```

---

## Step 6: Create API Types

Create `Phase-2-web-todo/frontend/types/api.ts`:

```typescript
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, unknown>;
}
```

---

## Step 7: Create API Client

Create `Phase-2-web-todo/frontend/lib/api-client.ts`:

```typescript
import type { Task, TaskCreate, TaskUpdate, ErrorResponse } from "@/types/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Fetch wrapper that injects JWT token and handles errors
 */
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get session from Better Auth
  const session = await auth.api.getSession();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add JWT token if available
  if (session?.token) {
    headers["Authorization"] = `Bearer ${session.token}`;
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.message || "API request failed");
    }

    // Handle 204 No Content (DELETE)
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/**
 * Health check
 */
export async function getHealth(): Promise<{ status: string }> {
  return apiFetch("/health");
}

/**
 * Create a new task
 */
export async function createTask(
  userId: string,
  taskData: TaskCreate
): Promise<Task> {
  return apiFetch(`/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify(taskData),
  });
}

/**
 * List all tasks for a user
 */
export async function listTasks(userId: string): Promise<Task[]> {
  return apiFetch(`/${userId}/tasks`);
}

/**
 * Get a single task
 */
export async function getTask(userId: string, taskId: number): Promise<Task> {
  return apiFetch(`/${userId}/tasks/${taskId}`);
}

/**
 * Update a task
 */
export async function updateTask(
  userId: string,
  taskId: number,
  taskData: TaskUpdate
): Promise<Task> {
  return apiFetch(`/${userId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(taskData),
  });
}

/**
 * Delete a task
 */
export async function deleteTask(userId: string, taskId: number): Promise<void> {
  return apiFetch(`/${userId}/tasks/${taskId}`, {
    method: "DELETE",
  });
}

/**
 * Toggle task completion
 */
export async function toggleCompletion(
  userId: string,
  taskId: number
): Promise<Task> {
  return apiFetch(`/${userId}/tasks/${taskId}/complete`, {
    method: "PATCH",
  });
}
```

---

## Step 8: Create Auth Context

Create `Phase-2-web-todo/frontend/context/auth-context.tsx`:

```typescript
"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { auth, type Session } from "@/lib/auth";

interface AuthContextType {
  isAuthenticated: boolean;
  userId: string | null;
  isLoading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function checkSession() {
      try {
        const session = await auth.api.getSession();
        if (session?.user) {
          setIsAuthenticated(true);
          setUserId(session.user.id);
        } else {
          setIsAuthenticated(false);
          setUserId(null);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Authentication error");
        setIsAuthenticated(false);
        setUserId(null);
      } finally {
        setIsLoading(false);
      }
    }

    checkSession();
  }, []);

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, userId, isLoading, error }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
```

---

## Step 9: Create Auth Pages

### Signup Page

Create `Phase-2-web-todo/frontend/app/(auth)/signup/page.tsx`:

```typescript
"use client";

import { useState } from "react";
import { auth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await auth.api.signUp.email({ email, password });
      // Redirect to login after signup
      router.push("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6">Create Account</h1>
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}
        <form onSubmit={handleSignup}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border rounded"
              required
              minLength={8}
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isLoading ? "Creating..." : "Sign Up"}
          </button>
        </form>
        <p className="mt-4 text-center text-sm">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 hover:underline">
            Log in
          </a>
        </p>
      </div>
    </div>
  );
}
```

### Login Page

Create `Phase-2-web-todo/frontend/app/(auth)/login/page.tsx`:

```typescript
"use client";

import { useState } from "react";
import { auth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await auth.api.signIn.email({ email, password });
      // Redirect to tasks dashboard
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6">Log In</h1>
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isLoading ? "Logging in..." : "Log In"}
          </button>
        </form>
        <p className="mt-4 text-center text-sm">
          Don't have an account?{" "}
          <a href="/signup" className="text-blue-600 hover:underline">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
}
```

---

## Step 10: Create Task Dashboard

Create `Phase-2-web-todo/frontend/app/(dashboard)/tasks/page.tsx`:

```typescript
"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import type { Task, TaskCreate } from "@/types/api";
import {
  listTasks,
  createTask,
  toggleCompletion,
  deleteTask,
} from "@/lib/api-client";
import { auth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function TasksPage() {
  const router = useRouter();
  const { isAuthenticated, userId, isLoading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [newTaskTitle, setNewTaskTitle] = useState("");

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  // Load tasks
  useEffect(() => {
    async function loadTasks() {
      if (!userId) return;

      try {
        setIsLoading(true);
        const data = await listTasks(userId);
        setTasks(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load tasks");
      } finally {
        setIsLoading(false);
      }
    }

    if (userId) {
      loadTasks();
    }
  }, [userId]);

  async function handleCreateTask(e: React.FormEvent) {
    e.preventDefault();
    if (!userId || !newTaskTitle.trim()) return;

    try {
      const taskData: TaskCreate = { title: newTaskTitle };
      const newTask = await createTask(userId, taskData);
      setTasks([newTask, ...tasks]);
      setNewTaskTitle("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    }
  }

  async function handleToggle(task: Task) {
    if (!userId) return;

    try {
      const updated = await toggleCompletion(userId, task.id);
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to toggle task");
    }
  }

  async function handleDelete(task: Task) {
    if (!userId) return;
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      await deleteTask(userId, task.id);
      setTasks(tasks.filter((t) => t.id !== task.id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
    }
  }

  async function handleLogout() {
    await auth.api.signOut();
    router.push("/login");
  }

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">My Tasks</h1>
          <button
            onClick={handleLogout}
            className="text-red-600 hover:text-red-700"
          >
            Log Out
          </button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Create Task Form */}
        <form onSubmit={handleCreateTask} className="mb-8">
          <div className="flex gap-2">
            <input
              type="text"
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              placeholder="Add a new task..."
              className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              maxLength={200}
            />
            <button
              type="submit"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Add Task
            </button>
          </div>
        </form>

        {/* Task List */}
        {tasks.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <p className="text-lg">No tasks yet</p>
            <p>Create your first task above to get started</p>
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="bg-white p-4 rounded-lg shadow-sm flex items-center gap-4"
              >
                <button
                  onClick={() => handleToggle(task)}
                  className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    task.completed
                      ? "bg-green-500 border-green-500 text-white"
                      : "border-gray-300 hover:border-green-500"
                  }`}
                >
                  {task.completed && <span className="text-sm">✓</span>}
                </button>

                <div className="flex-1">
                  <h3
                    className={`text-lg ${
                      task.completed ? "text-gray-400 line-through" : ""
                    }`}
                  >
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-gray-600 text-sm mt-1">
                      {task.description}
                    </p>
                  )}
                </div>

                <button
                  onClick={() => handleDelete(task)}
                  className="text-red-600 hover:text-red-700 px-3 py-1"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## Step 11: Update Root Layout

Update `Phase-2-web-todo/frontend/app/layout.tsx`:

```typescript
import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/auth-context";

export const metadata: Metadata = {
  title: "Todo App",
  description: "Manage your tasks",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
```

---

## Step 12: Run the Application

```bash
cd Phase-2-web-todo/frontend
npm run dev
```

**Access**: Open `http://localhost:3000` in your browser

---

## Testing the Application

### 1. Test Authentication
- Navigate to `/signup`
- Create an account with email and password
- Verify you can log in at `/login`
- Verify logout redirects to login page

### 2. Test Task Management
- Create a new task
- Verify it appears in the task list
- Toggle completion status
- Verify visual state change
- Delete the task
- Verify it's removed from the list

### 3. Test API Communication
- Open browser DevTools Network tab
- Verify API requests include `Authorization: Bearer <token>` header
- Verify correct HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Verify response formats match API contracts

---

## Troubleshooting

### CORS Issues
**Problem**: Backend rejects requests due to CORS
**Solution**: Ensure backend CORS middleware allows frontend origin (`http://localhost:3000`)

### JWT Token Issues
**Problem**: Backend returns 401 Unauthorized
**Solution**: Ensure `BETTER_AUTH_SECRET` matches between frontend and backend

### Better Auth Session Issues
**Problem**: Session not persisting
**Solution**: Check Better Auth configuration, ensure cookies or localStorage is enabled

---

## Summary

**Implementation Steps Completed**:
1. ✅ Initialize Next.js 16+ project with TypeScript and Tailwind
2. ✅ Install dependencies (Better Auth, Zustand)
3. ✅ Configure environment variables
4. ✅ Set up Better Auth for JWT authentication
5. ✅ Create TypeScript API types
6. ✅ Build API client with JWT injection
7. ✅ Create Auth Context for session management
8. ✅ Build signup and login pages
9. ✅ Build task dashboard with CRUD operations
10. ✅ Test authentication and task management

**Next Steps**:
- Run `/sp.tasks` to generate detailed implementation tasks
- Follow tasks to implement remaining features (edit task, improved UI, error handling)
- Add E2E tests with Playwright
- Deploy to production environment
