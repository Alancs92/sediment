FROM python:3.12-slim AS base

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .

ENV PYTHONUNBUFFERED=1
EXPOSE 8420

ENTRYPOINT ["python", "-m", "sediment_aggregator"]
CMD ["serve"]
