FROM python:3.11-slim AS backend

WORKDIR /backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /backend

FROM node:18-alpine AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend /frontend
RUN npm run build

FROM python:3.11-slim

WORKDIR /app
COPY --from=backend /backend /app/backend
COPY --from=frontend /frontend/build /app/frontend

RUN pip install --no-cache-dir fastapi uvicorn requests scikit-learn pydantic python-multipart

ENV IQAIR_API_KEY=${IQAIR_API_KEY}

EXPOSE 7860
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
