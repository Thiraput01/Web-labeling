FROM node:20

ENV NODE_ENV=production

WORKDIR /usr/src/app

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm add prisma --save-dev
RUN pnpm prisma generate
RUN pnpm prisma migrate deploy

RUN pnpm build

EXPOSE 8000

CMD ["pnpm", "start"]
