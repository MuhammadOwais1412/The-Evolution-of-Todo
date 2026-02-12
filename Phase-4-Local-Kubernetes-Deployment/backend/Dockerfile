FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-cache

COPY . .

EXPOSE 7860

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]