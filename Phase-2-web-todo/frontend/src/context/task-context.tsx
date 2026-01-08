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
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export function TaskProvider({ children }: { children: ReactNode }) {
  const { userId, isAuthenticated } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = async () => {
    if (!userId || !isAuthenticated) {
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
    if (!userId) {
      throw new Error("User not authenticated");
    }

    try {
      setError(null);
      const newTask = await createTask(userId, taskData);
      setTasks(prev => [newTask, ...prev]);
      return newTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create task";
      setError(message);
      throw err;
    }
  };

  const updateTaskFunc = async (taskId: number, taskData: TaskUpdate): Promise<Task> => {
    if (!userId) {
      throw new Error("User not authenticated");
    }

    try {
      setError(null);
      const updatedTask = await updateTask(userId, taskId, taskData);
      setTasks(prev => prev.map(t => t.id === taskId ? updatedTask : t));
      return updatedTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update task";
      setError(message);
      throw err;
    }
  };

  const deleteTaskFunc = async (taskId: number): Promise<void> => {
    if (!userId) {
      throw new Error("User not authenticated");
    }

    try {
      setError(null);
      await deleteTask(userId, taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete task";
      setError(message);
      throw err;
    }
  };

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
      void loadTasks();
    } else {
      setTasks([]);
    }
  }, [userId, isAuthenticated]);

  const value = useMemo(() => ({
    tasks,
    isLoading,
    error,
    loadTasks,
    createTask: createTaskFunc,
    updateTask: updateTaskFunc,
    deleteTask: deleteTaskFunc,
    toggleCompletion: toggleCompletionFunc,
    retryLoadTasks,
  }), [tasks, isLoading, error]);

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