"use client";

import { useState, useEffect } from "react";
import { useTaskContext } from "@/context/task-context";
import type { Task } from "@/types/api";
import { TaskForm } from "./TaskForm";

interface EditTaskModalProps {
  task: Task | null;
  userId: string;
  onClose: () => void;
}

export function EditTaskModal({ task, userId, onClose }: EditTaskModalProps) {
  const { updateTask } = useTaskContext();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  // Close on escape key
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") {
        onClose();
      }
    }
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (task) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [task]);

  async function handleSubmit(title: string, description: string) {
    if (!task) return;

    setIsSubmitting(true);
    setError("");

    try {
      await updateTask(task.id, {
        title,
        description,
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (!task) return null;

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="edit-task-title"
    >
      <div
        className="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 id="edit-task-title" className="text-xl font-bold">
              Edit Task
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 touch-manipulation min-w-[44px] min-h-[44px] p-2"
              aria-label="Close modal"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded border border-red-200">
              {error}
            </div>
          )}

          <TaskForm
            onSubmit={handleSubmit}
            isLoading={isSubmitting}
            onCancel={onClose}
            initialTitle={task.title}
            initialDescription={task.description || ""}
            submitLabel="Save Changes"
          />
        </div>
      </div>
    </div>
  );
}
