FROM node:18-alpine

# SOVEREIGN PROPERTY OF IGOR GONCHARENKO
WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY agent_bridge.js ./

# Set environment variable during deployment via secret
# ENV GEMINI_API_KEY=""

CMD ["node", "agent_bridge.js"]
