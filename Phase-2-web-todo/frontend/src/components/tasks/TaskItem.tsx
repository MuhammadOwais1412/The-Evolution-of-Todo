"use client";

import { useState } from "react";
import type { Task } from "@/types/api";
import Link from "next/link";

interface TaskItemProps {
  task: Task;
  userId: string;
  onDelete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onToggle?: (updatedTask: Task) => void;
  isTaskToggling?: (taskId: number) => boolean;  // Function to check if task is currently toggling
  toggleCompletion?: (taskId: number) => Promise<Task>;  // Function to toggle completion from context
}

export function TaskItem({ task, userId, onDelete, onEdit, onToggle, isTaskToggling, toggleCompletion }: TaskItemProps) {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  async function handleToggle() {
    if (!toggleCompletion) return;

    try {
      await toggleCompletion(task.id);
      // The task context manages state updates, so we don't need to call onToggle
      // The UI will update automatically when the tasks array in context changes
    } catch (err) {
      console.error("Failed to toggle task:", err);
      alert(err instanceof Error ? err.message : "Failed to update task");
    }
  }

  async function handleDelete() {
    if (!onDelete) return;

    try {
      await onDelete(task.id);
      setShowDeleteConfirm(false);
    } catch (err) {
      console.error("Failed to delete task:", err);
      alert(err instanceof Error ? err.message : "Failed to delete task");
    }
  }

  function handleEditClick() {
    if (onEdit) {
      onEdit(task);
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div
      className={`bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow ${
        task.completed ? "opacity-75" : ""
      }`}
    >
      <div className="flex items-start gap-4">
        {/* Completion Toggle */}
        <button
          onClick={handleToggle}
          disabled={isTaskToggling?.(task.id) || false}
          className={`mt-1 w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 touch-manipulation min-w-[44px] min-h-[44px] transition-colors ${
            isTaskToggling?.(task.id)
              ? "opacity-50 cursor-not-allowed"
              : task.completed
                ? "bg-green-500 border-green-500 text-white hover:bg-green-600"
                : "border-gray-300 hover:border-green-500 hover:bg-green-50"
          }`}
          aria-label={isTaskToggling?.(task.id) ? "Updating..." : task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {isTaskToggling?.(task.id) ? (
            <svg
              className="w-4 h-4 animate-spin text-current"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          ) : task.completed ? (
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          ) : null}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium break-words ${
              task.completed ? "text-gray-400 line-through" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`text-sm mt-1 break-words ${
                task.completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            Created: {formatDate(task.created_at)}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col gap-2">
          {onEdit && (
            <button
              onClick={handleEditClick}
              disabled={isTaskToggling?.(task.id) || false}
              className="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors touch-manipulation min-w-[44px] min-h-[44px]"
              aria-label="Edit task"
              title="Edit task"
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
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
                />
              </svg>
            </button>
          )}

          {onDelete && (
            <button
              onClick={() => !isTaskToggling?.(task.id) && setShowDeleteConfirm(true)}
              disabled={isTaskToggling?.(task.id) || false}
              className="p-2 text-red-600 hover:bg-red-50 rounded transition-colors touch-manipulation min-w-[44px] min-h-[44px]"
              aria-label="Delete task"
              title="Delete task"
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
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Delete Confirmation */}
      {showDeleteConfirm && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-700 mb-3">
            Are you sure you want to delete this task? This action cannot be undone.
          </p>
          <div className="flex gap-2">
            <button
              onClick={handleDelete}
              disabled={isTaskToggling?.(task.id) || false}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:bg-red-300 disabled:cursor-not-allowed transition-colors min-h-[36px]"
            >
              {isTaskToggling?.(task.id) ? "Processing..." : "Delete"}
            </button>
            <button
              onClick={() => setShowDeleteConfirm(false)}
              disabled={isTaskToggling?.(task.id) || false}
              className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors min-h-[36px]"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}