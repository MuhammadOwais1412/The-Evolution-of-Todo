"use client";

import { createContext, useContext, useEffect, useState, ReactNode, useMemo } from "react";
import { useAuth } from "./auth-context";
import type { Task, TaskCreate, TaskUpdate } from "@/types/api";
import {
  listTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleCompletion,
} from "@/lib/api-client";

interface TaskContextType {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  loadTasks: () => Promise<void>;
  retryLoadTasks: () => Promise<void>;
  createTask: (taskData: TaskCreate) => Promise<Task>;
  updateTask: (taskId: number, taskData: TaskUpdate) => Promise<Task>;
  deleteTask: (taskId: number) => Promise<void>;
  toggleCompletion: (taskId: number) => Promise<Task>;
<<<<<<< HEAD
  isTaskToggling: (taskId: number) => boolean;  // Check if a task is currently being toggled
=======
>>>>>>> 003-frontend-better-auth
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export function TaskProvider({ children }: { children: ReactNode }) {
<<<<<<< HEAD
  const { userId, isAuthenticated, isTokenReady } = useAuth();
=======
  const { userId, isAuthenticated } = useAuth();
>>>>>>> 003-frontend-better-auth
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = async () => {
<<<<<<< HEAD
    if (!userId || !isAuthenticated || !isTokenReady) {
=======
    if (!userId || !isAuthenticated) {
>>>>>>> 003-frontend-better-auth
      setTasks([]);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const data = await listTasks(userId);
      setTasks(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load tasks";
<<<<<<< HEAD

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        setTasks([]);
        return;
      }

=======
>>>>>>> 003-frontend-better-auth
      setError(message);
      setTasks([]);
    } finally {
      setIsLoading(false);
    }
  };

  const retryLoadTasks = async () => {
    setError(null);
    await loadTasks();
  };

  const createTaskFunc = async (taskData: TaskCreate): Promise<Task> => {
<<<<<<< HEAD
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
=======
    if (!userId) {
      throw new Error("User not authenticated");
>>>>>>> 003-frontend-better-auth
    }

    try {
      setError(null);
      const newTask = await createTask(userId, taskData);
      setTasks(prev => [newTask, ...prev]);
      return newTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create task";
<<<<<<< HEAD

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

=======
>>>>>>> 003-frontend-better-auth
      setError(message);
      throw err;
    }
  };

  const updateTaskFunc = async (taskId: number, taskData: TaskUpdate): Promise<Task> => {
<<<<<<< HEAD
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
=======
    if (!userId) {
      throw new Error("User not authenticated");
>>>>>>> 003-frontend-better-auth
    }

    try {
      setError(null);
      const updatedTask = await updateTask(userId, taskId, taskData);
      setTasks(prev => prev.map(t => t.id === taskId ? updatedTask : t));
      return updatedTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update task";
<<<<<<< HEAD

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

=======
>>>>>>> 003-frontend-better-auth
      setError(message);
      throw err;
    }
  };

  const deleteTaskFunc = async (taskId: number): Promise<void> => {
<<<<<<< HEAD
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
=======
    if (!userId) {
      throw new Error("User not authenticated");
>>>>>>> 003-frontend-better-auth
    }

    try {
      setError(null);
      await deleteTask(userId, taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete task";
<<<<<<< HEAD

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

=======
>>>>>>> 003-frontend-better-auth
      setError(message);
      throw err;
    }
  };

<<<<<<< HEAD
  // Track tasks currently being toggled to prevent multiple simultaneous toggles
  const [togglingTasks, setTogglingTasks] = useState<Set<number>>(new Set());

  const toggleCompletionFunc = async (taskId: number): Promise<Task> => {
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
    }

    // Prevent multiple simultaneous toggles for the same task
    if (togglingTasks.has(taskId)) {
      throw new Error("Task is already being toggled");
    }

    setTogglingTasks(prev => new Set(prev).add(taskId));

    try {
      setError(null);

      // Get the current task state before making changes
      const currentTask = tasks.find(t => t.id === taskId);
      if (!currentTask) {
        throw new Error("Task not found");
      }

      // Optimistically update the UI to provide immediate feedback
      setTasks(prev => prev.map(t =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      ));

      const updatedTask = await toggleCompletion(userId, taskId);

      // Update with the server response to ensure consistency
      // Use the actual response from the server rather than calculating
      setTasks(prev => prev.map(t =>
        t.id === taskId ? updatedTask : t
      ));

      return updatedTask;
    } catch (err) {
      // If the operation fails, revert the optimistic update
      setTasks(prev => prev.map(t =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      ));

      const message = err instanceof Error ? err.message : "Failed to toggle task completion";

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

      setError(message);
      throw err;
    } finally {
      setTogglingTasks(prev => {
        const newSet = new Set(prev);
        newSet.delete(taskId);
        return newSet;
      });
    }
  };

  // Reload tasks when userId, isAuthenticated, or isTokenReady changes
  useEffect(() => {
    if (userId && isAuthenticated && isTokenReady) {
=======
  const toggleCompletionFunc = async (taskId: number): Promise<Task> => {
    if (!userId) {
      throw new Error("User not authenticated");
    }

    try {
      setError(null);
      const updatedTask = await toggleCompletion(userId, taskId);
      setTasks(prev => prev.map(t => t.id === taskId ? updatedTask : t));
      return updatedTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to toggle task completion";
      setError(message);
      throw err;
    }
  };

  // Reload tasks when userId changes
  useEffect(() => {
    if (userId && isAuthenticated) {
>>>>>>> 003-frontend-better-auth
      void loadTasks();
    } else {
      setTasks([]);
    }
<<<<<<< HEAD
  }, [userId, isAuthenticated, isTokenReady]);
=======
  }, [userId, isAuthenticated]);
>>>>>>> 003-frontend-better-auth

  const value = useMemo(() => ({
    tasks,
    isLoading,
    error,
    loadTasks,
    createTask: createTaskFunc,
    updateTask: updateTaskFunc,
    deleteTask: deleteTaskFunc,
    toggleCompletion: toggleCompletionFunc,
<<<<<<< HEAD
    isTaskToggling: (taskId: number) => togglingTasks.has(taskId),
    retryLoadTasks,
  }), [tasks, isLoading, error, togglingTasks]);
=======
    retryLoadTasks,
  }), [tasks, isLoading, error]);
>>>>>>> 003-frontend-better-auth

  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );
}

export function useTaskContext() {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error("useTaskContext must be used within a TaskProvider");
  }
  return context;
}