FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    bash \
    curl \
    jq \
    python3 \
    make \
    g++ \
    openssh-client \
    procps \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code t3

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /workspace

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["t3", "serve", "--host", "0.0.0.0", "--port", "9000"]
