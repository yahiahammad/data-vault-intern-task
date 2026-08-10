FROM apache/superset:latest
USER root
COPY requirements.txt /requirements.txt
RUN uv pip install --python /app/.venv/bin/python -r /requirements.txt
USER superset
