FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

#Enable bytecode compilation and Python optimization
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONOPTIMIZE=1
ENV UV_LINK_MODE=copy

#Set Python path to include source directory for imports
ENV PYTHONPATH="/app/src"

#Copy only dependencies to leverage Docker cache
COPY pyproject.toml uv.lock ./

#Install Dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Copy Application Code
COPY src/chatbot-ui ./src/chatbot-ui/

# Pre-compile Python files to Bytecode
RUN python -m compileall ./src/chatbot-ui

# Set path to use the environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user and set permissions
RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

# Switch to non-root user
USER app

#Expose the Streamlit port
EXPOSE 8501

#Command to run the Streamlit app
CMD ["streamlit", "run", "src/chatbot-ui/streamlit_app.py", "--server.address=0.0.0.0"]    