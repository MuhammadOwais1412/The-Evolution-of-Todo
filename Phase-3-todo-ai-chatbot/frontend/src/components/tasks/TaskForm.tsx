"use client";

import { useState } from "react";

interface TaskFormProps {
  onSubmit: (title: string, description: string) => Promise<void>;
  isLoading?: boolean;
  onCancel?: () => void;
  initialTitle?: string;
  initialDescription?: string;
  submitLabel?: string;
}

export function TaskForm({
  onSubmit,
  isLoading = false,
  onCancel,
  initialTitle = "",
  initialDescription = "",
  submitLabel = "Add Task",
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [error, setError] = useState("");

  function validateForm(): boolean {
    // Title validation: required, 1-200 characters
    if (!title.trim()) {
      setError("Title is required");
      return false;
    }
    if (title.trim().length > 200) {
      setError("Title must be 200 characters or less");
      return false;
    }

    // Description validation: optional, max 5000 characters
    if (description.length > 5000) {
      setError("Description must be 5000 characters or less");
      return false;
    }

    return true;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!validateForm()) {
      return;
    }

    try {
      await onSubmit(title.trim(), description.trim());
      // Clear form on success if no onCancel (meaning it's a new task form)
      if (!onCancel) {
        setTitle("");
        setDescription("");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    }
  }

  const remainingTitleChars = 200 - title.length;
  const remainingDescChars = 5000 - description.length;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded border border-red-200">
          {error}
        </div>
      )}

      <div>
        <label
          htmlFor="task-title"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter task title..."
          maxLength={200}
          required
          disabled={isLoading}
        />
        <div className="flex justify-between mt-1">
          <span className={`text-xs ${remainingTitleChars < 0 ? "text-red-500" : "text-gray-500"}`}>
            {remainingTitleChars >= 0 ? `${remainingTitleChars} characters remaining` : `${Math.abs(remainingTitleChars)} characters over limit`}
          </span>
        </div>
      </div>

      <div>
        <label
          htmlFor="task-description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description <span className="text-gray-400">(optional)</span>
        </label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[100px]"
          placeholder="Add a description..."
          maxLength={5000}
          rows={3}
          disabled={isLoading}
        />
        <div className="flex justify-between mt-1">
          <span className={`text-xs ${remainingDescChars < 0 ? "text-red-500" : "text-gray-500"}`}>
            {remainingDescChars >= 0 ? `${remainingDescChars} characters remaining` : `${Math.abs(remainingDescChars)} characters over limit`}
          </span>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={isLoading}
          className="flex-1 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors min-h-[44px] touch-manipulation"
        >
          {isLoading ? "Saving..." : submitLabel}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="px-6 p-3 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors min-h-[44px] touch-manipulation"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
