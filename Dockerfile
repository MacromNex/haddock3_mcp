FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/macronex/haddock3_mcp"
LABEL org.opencontainers.image.description="HADDOCK3 integrative modeling for biomolecular docking"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget build-essential && \
    rm -rf /var/lib/apt/lists/*

# Core dependencies
RUN pip install --no-cache-dir \
    numpy scipy pandas biopython pdb-tools \
    loguru click tqdm fastmcp

# Clone and install HADDOCK3
RUN git clone https://github.com/haddocking/haddock3.git /app/repo/haddock3 && \
    cd /app/repo/haddock3 && \
    pip install --no-cache-dir -e .

# Copy MCP server source
COPY src/ src/

CMD ["python", "src/server.py"]
