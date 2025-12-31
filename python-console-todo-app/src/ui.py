"""Console UI for the Todo application."""

from typing import Optional
from datetime import datetime
import re


# ============================================================================
# ANSI COLOR PALETTE - Modern, Accessible Color Scheme
# ============================================================================

# Primary Colors
CYAN = "\033[96m"      # Primary accent - structural elements
MAGENTA = "\033[95m"   # Secondary accent - special highlights
BLUE = "\033[94m"      # Info elements
GREEN = "\033[92m"     # Success/completed states
YELLOW = "\033[93m"    # Warning/pending states
RED = "\033[91m"       # Error/destructive states
WHITE = "\033[97m"     # Primary content
BRIGHT_WHITE = "\033[37m\033[1m"  # High emphasis
DIM_WHITE = "\033[37m\033[90m"    # Low emphasis

# Style Modifiers
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# ============================================================================
# SEMANTIC COLOR ROLES - Consistent theming throughout UI
# ============================================================================

# Structural elements (borders, boxes, dividers)
ROLE_STRUCTURE = CYAN

# Primary content (menu items, table data, main text)
ROLE_CONTENT = WHITE

# Accent elements (headers, dates, stats, prompts)
ROLE_ACCENT = BLUE

# Success states (completed tasks, confirmations)
ROLE_SUCCESS = GREEN

# Warning states (pending tasks, alerts)
ROLE_WARNING = YELLOW

# Error states (errors, confirmations, destructive actions)
ROLE_ERROR = RED

# Title emphasis
ROLE_TITLE = MAGENTA


# ============================================================================
# UI CONSTANTS
# ============================================================================

BOX_WIDTH = 80
TITLE = "TODO APPLICATION"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# Column widths for task table (total must be <= BOX_WIDTH - overhead)
COL_ID = 5
COL_STATUS = 12
COL_TITLE = 30
COL_DESC = 30

# Progress bar settings
PROGRESS_BAR_LENGTH = 30


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _color(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{color}{text}{RESET}"


def _bold(text: str) -> str:
    """Apply bold to text."""
    return f"{BOLD}{text}{RESET}"


def _color_bold(text: str, color: str) -> str:
    """Apply color and bold to text."""
    return f"{BOLD}{color}{text}{RESET}"


def _underline(text: str) -> str:
    """Apply underline to text."""
    return f"{UNDERLINE}{text}{RESET}"


def _color_bold_underline(text: str, color: str) -> str:
    """Apply color, bold, and underline to text."""
    return f"{BOLD}{UNDERLINE}{color}{text}{RESET}"


def _center(text: str, width: int) -> str:
    """Center text within specified width."""
    text_len = _get_text_length(text)
    if text_len >= width:
        return text[:width]
    padding = width - text_len
    left = padding // 2
    right = padding - left
    return " " * left + text + " " * right


def _left_align(text: str, width: int) -> str:
    """Left-align text within specified width."""
    text_len = _get_text_length(text)
    if text_len >= width:
        return text[:width]
    return text + " " * (width - text_len)


def _right_align(text: str, width: int) -> str:
    """Right-align text within specified width."""
    text_len = _get_text_length(text)
    if text_len >= width:
        return text[:width]
    return " " * (width - text_len) + text


def _get_text_length(text: str) -> int:
    """Get text length excluding ANSI codes."""
    return len(re.sub(r'\033\[[0-9;]*m', '', text))


def _truncate(text: str, width: int) -> str:
    """Truncate text with ellipsis if it exceeds width."""
    if len(text) > width:
        return text[:width - 3] + "..."
    return text


# ============================================================================
# BORDER AND DECORATION FUNCTIONS
# ============================================================================

def _box_top() -> None:
    """Print top border of a box."""
    print(f"{_color('+' + '-' * (BOX_WIDTH - 2) + '+', ROLE_STRUCTURE)}")


def _box_bottom() -> None:
    """Print bottom border of a box."""
    print(f"{_color('+' + '-' * (BOX_WIDTH - 2) + '+', ROLE_STRUCTURE)}")


def _box_line(text: str = "", align: str = "center") -> None:
    """Print a line within a box with proper borders."""
    content_width = BOX_WIDTH - 4
    if align == "center":
        content = _center(text, content_width)
    elif align == "left":
        content = _left_align(text, content_width)
    elif align == "right":
        content = _right_align(text, content_width)
    else:
        content = _center(text, content_width)
    print(f"{_color('|', ROLE_STRUCTURE)}{content}{_color('|', ROLE_STRUCTURE)}")


def _solid_line(char: str = "-") -> None:
    """Print a solid divider line."""
    print(f"{_color(char * BOX_WIDTH, ROLE_STRUCTURE)}")


def _divider() -> None:
    """Print a divider line."""
    _solid_line("-")


# ============================================================================
# MESSAGE FUNCTIONS
# ============================================================================

def header(text: str) -> None:
    """Display a section header."""
    print()
    print(f"{_color_bold(text, ROLE_TITLE)}")


def success(text: str) -> None:
    """Display a success message."""
    print(f"  {_color('[OK]', ROLE_SUCCESS)}  {_color(text, ROLE_SUCCESS)}")


def error(text: str) -> None:
    """Display an error message."""
    print(f"  {_color('[ERROR]', ROLE_ERROR)}  {_color(text, ROLE_ERROR)}")


def info(text: str) -> None:
    """Display an info message."""
    print(f"  {_color('[INFO]', ROLE_ACCENT)}  {_color(text, ROLE_ACCENT)}")


def warning(text: str) -> None:
    """Display a warning message."""
    print(f"  {_color('[WARNING]', ROLE_WARNING)}  {_color(text, ROLE_WARNING)}")


# ============================================================================
# MENU FUNCTIONS
# ============================================================================

def show_menu() -> None:
    """Display the main menu with enhanced visuals."""
    print()
    _box_top()

    # Title centered
    _box_line(_bold(TITLE), "center")

    # Subtitle with date and task count
    _solid_line()
    _box_line(f"{CURRENT_DATE}", "center")

    _box_bottom()
    print()

    # Menu section
    _box_top()
    _box_line(_bold("ACTIONS"), "center")
    _solid_line()

    menu_items = [
        ("1", "Add Task", "Create a new task"),
        ("2", "View Tasks", "Display all tasks"),
        ("3", "Update Task", "Modify an existing task"),
        ("4", "Delete Task", "Remove a task"),
        ("5", "Mark Complete", "Mark task as done"),
        ("6", "Mark Incomplete", "Mark task as pending"),
        ("7", "Exit", "Close the application"),
    ]

    for num, action, desc in menu_items:
        num_display = _color(f"[{num}]", ROLE_ACCENT)
        action_display = _color(action, ROLE_CONTENT)
        desc_display = _color(f"- {desc}", DIM_WHITE)
        row = f"  {num_display}  {action_display:<20} {desc_display}"
        _box_line(row, "left")

    _box_bottom()
    print()


# ============================================================================
# PROMPT FUNCTIONS
# ============================================================================

def get_choice() -> int:
    """Get and validate the user's menu choice."""
    while True:
        try:
            choice = int(input(f"{_color('->', ROLE_ACCENT)} Enter choice: ").strip())
            if 1 <= choice <= 7:
                return choice
            error("Invalid choice. Please enter 1-7.")
        except ValueError:
            error("Invalid input. Please enter a number.")


def prompt_task_data() -> tuple[str, str]:
    """Prompt for task title and description."""
    print()

    while True:
        title = input(f"{_color('->', ROLE_ACCENT)} Enter task title: ").strip()
        if title:
            break
        error("Title cannot be empty.")

    description = input(f"{_color('->', ROLE_ACCENT)} Enter task description (optional): ").strip()
    print()

    return title, description


def prompt_task_id() -> int:
    """Prompt for a valid task ID."""
    print()
    while True:
        try:
            task_id = int(input(f"{_color('->', ROLE_ACCENT)} Enter task ID: ").strip())
            if task_id > 0:
                return task_id
            error("Invalid ID. Please enter a positive number.")
        except ValueError:
            error("Invalid input. Please enter a number.")


def prompt_update_data() -> tuple[Optional[str], Optional[str]]:
    """Prompt for updated title and description (both optional)."""
    print()

    title = input(f"{_color('->', ROLE_ACCENT)} Enter new title (leave empty to keep): ").strip()
    description = input(f"{_color('->', ROLE_ACCENT)} Enter new description (leave empty to keep): ").strip()

    print()

    return title or None, description or None


def confirm_action(action: str, task_id: int) -> bool:
    """Confirm a destructive action."""
    print()
    confirm = input(f"{_color('[CONFIRM]', ROLE_WARNING)} {action} task #{task_id}? (y/n): ").strip().lower()
    return confirm == "y"


# ============================================================================
# TASK DISPLAY FUNCTIONS
# ============================================================================

def _format_status(completed: bool) -> str:
    """Format task status with appropriate styling."""
    if completed:
        return f"{_color('[X]', ROLE_SUCCESS)} {_color('DONE', ROLE_SUCCESS)}"
    else:
        return f"{_color('[ ]', ROLE_WARNING)} {_color('PENDING', ROLE_WARNING)}"


def _create_table_header() -> None:
    """Create the table header row with proper column alignment."""
    print(f"{_color('+' + '-' * (COL_ID + 2) + '+' + '-' * (COL_STATUS + 2) + '+' + '-' * (COL_TITLE + 2) + '+' + '-' * (COL_DESC + 2) + '+', ROLE_STRUCTURE)}")

    header_parts = [
        (_center(_bold("ID"), COL_ID + 2), COL_ID + 2),
        (_center(_bold("STATUS"), COL_STATUS + 2), COL_STATUS + 2),
        (_center(_bold("TITLE"), COL_TITLE + 2), COL_TITLE + 2),
        (_center(_bold("DESCRIPTION"), COL_DESC + 2), COL_DESC + 2),
    ]

    line = ""
    for content, width in header_parts:
        line += f"{_color('|', ROLE_STRUCTURE)}{content}"
    line += f"{_color('|', ROLE_STRUCTURE)}"
    print(line)

    print(f"{_color('+' + '-' * (COL_ID + 2) + '+' + '-' * (COL_STATUS + 2) + '+' + '-' * (COL_TITLE + 2) + '+' + '-' * (COL_DESC + 2) + '+', ROLE_STRUCTURE)}")


def _create_table_row(task_id: int, status: str, title: str, description: str, is_alternate: bool) -> None:
    """Create a table row with proper column alignment and zebra striping."""
    row_color = DIM_WHITE if is_alternate else ROLE_CONTENT

    col_values = [
        (_right_align(str(task_id), COL_ID), COL_ID),
        (status, COL_STATUS),
        (_center(_truncate(title, COL_TITLE), COL_TITLE), COL_TITLE),
        (_center(_truncate(description, COL_DESC), COL_DESC), COL_DESC),
    ]

    line = ""
    for content, width in col_values:
        padded = content + " " * (width - _get_text_length(content))
        line += f"{_color('|', ROLE_STRUCTURE)}{_color(padded, row_color)}"
    line += f"{_color('|', ROLE_STRUCTURE)}"
    print(line)


def _close_table() -> None:
    """Close the table with bottom border."""
    print(f"{_color('+' + '-' * (COL_ID + 2) + '+' + '-' * (COL_STATUS + 2) + '+' + '-' * (COL_TITLE + 2) + '+' + '-' * (COL_DESC + 2) + '+', ROLE_STRUCTURE)}")


def _create_progress_bar(completed: int, total: int) -> str:
    """Create a visual progress bar."""
    if total == 0:
        filled = 0
    else:
        filled = int((completed / total) * PROGRESS_BAR_LENGTH)

    bar = f"{_color('#' * filled, ROLE_SUCCESS)}{_color('.', ROLE_WARNING)}{_color('.' * (PROGRESS_BAR_LENGTH - filled - 1), ROLE_WARNING)}"
    percent = f"{int((completed / total) * 100)}%" if total > 0 else "0%"
    return f"[{bar}] {percent}"


def show_tasks(tasks: list) -> None:
    """Display all tasks in a formatted table."""
    print()

    if not tasks:
        _box_top()
        _box_line(_bold("TASK LIST"), "center")
        _solid_line()
        _box_line("", "center")
        _box_line(_color("No tasks found", ROLE_ACCENT), "center")
        _box_line(_color("Add a new task to get started!", ROLE_ACCENT), "center")
        _box_line("", "center")
        _box_bottom()
        print()
        return

    # Calculate stats
    completed_count = sum(1 for t in tasks if t.completed)
    incomplete_count = len(tasks) - completed_count

    # Stats header
    _box_top()
    _box_line(_bold("TASK LIST"), "center")
    _solid_line()

    # Stats row
    stats_text = f"Total: {len(tasks)}  |  {_color('Completed:', ROLE_SUCCESS)} {completed_count}  |  {_color('Pending:', ROLE_WARNING)} {incomplete_count}"
    _box_line(stats_text, "center")

    # Progress bar
    progress = _create_progress_bar(completed_count, len(tasks))
    _box_line(progress, "center")

    _box_bottom()
    print()

    # Table with tasks
    _create_table_header()

    for idx, task in enumerate(tasks):
        status = _format_status(task.completed)
        title = task.title if task.title else _color("(no title)", DIM_WHITE)
        description = task.description if task.description else _color("(no description)", DIM_WHITE)
        _create_table_row(task.id, status, title, description, idx % 2 == 1)

    _close_table()
    print()


def show_separator() -> None:
    """Display a separator line."""
    print()
