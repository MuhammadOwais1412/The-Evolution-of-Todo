"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/auth-context";
import { useTaskContext } from "@/context/task-context";
import type { Task, TaskCreate } from "@/types/api";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskItem } from "@/components/tasks/TaskItem";
import { EditTaskModal } from "@/components/tasks/EditTaskModal";

export default function TasksPage() {
  const router = useRouter();
  const { isAuthenticated, userId, isLoading: authLoading, isTokenReady, logout } = useAuth();
  const { tasks, isLoading, error, createTask, deleteTask, toggleCompletion, isTaskToggling, retryLoadTasks } = useTaskContext();
  const [isCreating, setIsCreating] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Redirect if not authenticated - moved to useEffect to avoid state update during render
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading state while checking authentication or synchronizing token
  if (authLoading || !isTokenReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  // Redirect if not authenticated (after useEffect has run)
  if (!isAuthenticated) {
    return null; // Render nothing while redirecting
  }

  async function handleCreateTask(title: string, description: string) {
    if (!userId || !isTokenReady) return;

    setIsCreating(true);
    try {
      const taskData: TaskCreate = { title, description };
      await createTask(taskData);
    } catch (err) {
      // Error is handled in the context
    } finally {
      setIsCreating(false);
    }
  }

  function handleDeleteTask(taskId: number) {
    if (!isTokenReady) return;
    void deleteTask(taskId);
  }

  async function handleLogout() {
    await logout();
    router.push("/login");
  }

  // Empty state for no tasks
  const hasNoTasks = !isLoading && tasks.length === 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <nav className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Link
              href="/"
              className="text-xl font-bold text-blue-600 hover:text-blue-700"
            >
              Todo App
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600 hidden sm:block">
              {tasks.length} {tasks.length === 1 ? "task" : "tasks"}
            </span>
            <button
              onClick={handleLogout}
              className="text-red-600 hover:text-red-700 hover:bg-red-50 px-3 py-2 rounded transition-colors min-h-[36px] touch-manipulation"
              aria-label="Log out"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 16l4-4m0 0l-4 4m4-4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
              <span className="hidden md:inline ml-1">Log Out</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded border border-red-200">
            <p>{error}</p>
            {(error.toLowerCase().includes("timeout") || error.toLowerCase().includes("network")) && (
              <button
                type="button"
                onClick={() => {
                  // Retry loading tasks using the context function
                  void retryLoadTasks();
                }}
                aria-label="Retry loading tasks"
                className="mt-2 text-sm underline hover:no-underline"
              >
                Retry
              </button>
            )}
          </div>
        )}

        {/* Create Task Form */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-medium mb-4">Add a new task</h2>
          <TaskForm
            onSubmit={handleCreateTask}
            isLoading={isCreating}
          />
        </div>

        {/* Task List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading tasks...</p>
          </div>
        ) : hasNoTasks ? (
          <div className="text-center py-12">
            <svg
              className="w-16 h-16 mx-auto text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
              />
            </svg>
            <h3 className="text-xl font-medium text-gray-700 mb-2">No tasks yet</h3>
            <p className="text-gray-600">
              Create your first task above to get started!
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {/* Tasks ordered by creation date (newest first) */}
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                userId={userId || ""}
                onDelete={handleDeleteTask}
                onEdit={setEditingTask}
                isTaskToggling={isTokenReady ? (id) => isTaskToggling(id) : undefined}
                toggleCompletion={isTokenReady ? (id) => toggleCompletion(id) : undefined}
              />
            ))}
          </div>
        )}
      </main>

      {/* Edit Modal */}
      {editingTask && userId && (
        <EditTaskModal
          task={editingTask}
          userId={userId}
          onClose={() => setEditingTask(null)}
        />
      )}
    </div>
  );
}