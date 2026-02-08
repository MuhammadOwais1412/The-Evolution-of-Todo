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
  isTaskToggling: (taskId: number) => boolean;  // Check if a task is currently being toggled
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export function TaskProvider({ children }: { children: ReactNode }) {
  const { userId, isAuthenticated, isTokenReady } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = async () => {
    if (!userId || !isAuthenticated || !isTokenReady) {
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

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        setTasks([]);
        return;
      }

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
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
    }

    try {
      setError(null);
      const newTask = await createTask(userId, taskData);
      setTasks(prev => [newTask, ...prev]);
      return newTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create task";

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

      setError(message);
      throw err;
    }
  };

  const updateTaskFunc = async (taskId: number, taskData: TaskUpdate): Promise<Task> => {
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
    }

    try {
      setError(null);
      const updatedTask = await updateTask(userId, taskId, taskData);
      setTasks(prev => prev.map(t => t.id === taskId ? updatedTask : t));
      return updatedTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update task";

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

      setError(message);
      throw err;
    }
  };

  const deleteTaskFunc = async (taskId: number): Promise<void> => {
    if (!userId || !isAuthenticated || !isTokenReady) {
      throw new Error("User not authenticated or token not ready");
    }

    try {
      setError(null);
      await deleteTask(userId, taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete task";

      // Handle unauthorized error specifically
      if (message.includes("Unauthorized") || message.includes("401")) {
        // Don't set error state for unauthorized, let auth context handle it
        throw err;
      }

      setError(message);
      throw err;
    }
  };

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
      void loadTasks();
    } else {
      setTasks([]);
    }
  }, [userId, isAuthenticated, isTokenReady]);

  const value = useMemo(() => ({
    tasks,
    isLoading,
    error,
    loadTasks,
    createTask: createTaskFunc,
    updateTask: updateTaskFunc,
    deleteTask: deleteTaskFunc,
    toggleCompletion: toggleCompletionFunc,
    isTaskToggling: (taskId: number) => togglingTasks.has(taskId),
    retryLoadTasks,
  }), [tasks, isLoading, error, togglingTasks]);

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