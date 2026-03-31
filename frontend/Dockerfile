FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

ARG NEXT_PUBLIC_API_URL
ARG RAILWAY_GIT_BRANCH
ARG RAILWAY_GIT_COMMIT_SHA
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_BRANCH=$RAILWAY_GIT_BRANCH
ENV NEXT_PUBLIC_COMMIT=$RAILWAY_GIT_COMMIT_SHA

RUN npm run build

FROM node:20-slim AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE ${PORT:-3000}
CMD ["node", "server.js"]
