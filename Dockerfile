FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY nifipulse/ ./nifipulse/
RUN pip install -U pip && pip install --no-cache-dir .
ENTRYPOINT ["nifipulse"]
CMD ["--poll","10","--interval","60"] 