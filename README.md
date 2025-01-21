## Installation Steps

1. First, set up Traefik and Consul:

```bash
docker compose up --build -d
```

2. If you want to deploy the services to the same environment, run:

```bash
python scripts/deploy.py
```

When the second script runs successfully:
- The current Consul IP address will be automatically set
- Services will automatically register with Consul
- Traefik will detect these services
- API Gateway will be configured automatically

> Note: Make sure you have Docker and Python installed on your system before running these commands.

