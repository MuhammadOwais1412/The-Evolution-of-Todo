---
name: python-console-todo-app
description: Build a clean, spec-driven, in-memory Python console Todo application following professional software engineering practices.
version: "1.0.0"
---

This skill defines how to design and implement a **command-line Todo application** using **spec-driven development** with **Claude Code** and **Spec-Kit Plus**.

The project focuses on **clarity, correctness, and clean architecture**, avoiding over-engineering while maintaining professional structure and extensibility.

---

## Project Objective

Build a **working Python console application** that manages todo tasks **entirely in memory**, demonstrating core CRUD functionality and state management.

The application must:

- Run entirely in the terminal
- Store tasks in memory (no database or files)
- Follow spec-driven development
- Be readable, maintainable, and testable

---

## Core Functional Requirements (Basic Level)

The application must implement **all five required features**:

1. **Add Task**
   - Accept title and description
   - Assign a unique task ID
   - Default status: incomplete

2. **View Tasks**
   - List all tasks
   - Display:
     - Task ID
     - Title
     - Description
     - Completion status (✔ / ✖ or similar)

3. **Update Task**
   - Update title and/or description
   - Identify tasks by ID
   - Handle invalid IDs gracefully

4. **Delete Task**
   - Delete tasks by ID
   - Confirm successful deletion
   - Handle non-existent tasks safely

5. **Mark Complete / Incomplete**
   - Toggle task completion state
   - Reflect updated status in listings



## Edge Case Handling Requirements

The application **must gracefully handle the following edge cases**.

1. Empty Task Title
2. Empty Task Description
3. Duplicate Task Titles
4. Invalid Task ID
5. No Tasks Available

---

## Technical Stack

- **Python 3.13+**
- **UV** (Python package and environment manager)
- **Claude Code** (AI-assisted development)
- **Spec-Kit Plus** (spec-driven workflow)

---

## Architectural Guidelines

### Project Structure

Follow a clean, minimal Python project layout:

---

## Design Principles

- **Single Responsibility Principle**
- **Clear separation of concerns**
- **Readable function and variable names**
- **No hidden side effects**
- **Explicit user feedback in console**

Avoid:
- Global mutable state
- Hardcoded magic values
- Overly complex abstractions

---

## Spec-Driven Development Workflow

1. **Write Specification First**
   - Define behaviors, inputs, outputs, and constraints
   - No implementation details in the spec

2. **Generate Implementation Plan**
   - Break features into executable steps
   - Identify dependencies

3. **Implement Incrementally**
   - One feature at a time
   - Validate behavior after each step

4. **Verify Against Spec**
   - Ensure every requirement is satisfied
   - No extra or missing features

---

## Console UX Expectations

- Clear menu options
- Consistent prompts
- Friendly error messages
- Predictable command flow
- Colorfulness
- Attractiveness & Visual Clarity
- Accessibility Considerations


Example:

1. Add Task

2. View Tasks

3. Update Task

4. Delete Task

5. Mark Task Complete

6. Exit