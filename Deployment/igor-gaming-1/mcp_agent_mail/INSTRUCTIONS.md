# Deploy mcp_agent_mail on igor-gaming-1

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Dicklesworthstone/mcp_agent_mail.git
   cd mcp_agent_mail
   ```

2. **Create/Update `docker-compose.yml`**:
   Use the following configuration:

   ```yaml
   version: '3.8'
   services:
     db:
       image: postgres:16-alpine
       environment:
         POSTGRES_DB: agent_mail
         POSTGRES_USER: agent
         POSTGRES_PASSWORD: ${DATABASE_PASSWORD:-agent_pass}
       volumes:
         - pgdata:/var/lib/postgresql/data
     server:
       build: .
       ports:
         - "8765:8765"
       environment:
         DATABASE_URL: postgres+asyncpg://agent:${DATABASE_PASSWORD:-agent_pass}@db:5432/agent_mail
         STORAGE_ROOT: /data/mailbox
         HTTP_HOST: 0.0.0.0
         HTTP_BEARER_TOKEN: ${AUTH_TOKEN:-antigravity_secret}
       volumes:
         - mailbox_data:/data/mailbox
       depends_on:
         - db
   volumes:
     pgdata:
     mailbox_data:
   ```

3. **Set Environment Variables**:
   Create a `.env` file or set them in your shell:

   ```bash
   echo "DATABASE_PASSWORD=your_secure_db_pass" > .env
   echo "AUTH_TOKEN=your_secure_auth_token" >> .env
   ```

4. **Launch**:

   ```bash
   docker compose up -d
   ```
