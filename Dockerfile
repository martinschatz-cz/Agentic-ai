FROM continuumio/miniconda3:23.3.1

# Set working directory
WORKDIR /opt/app

# Copy repository
COPY . /opt/app

# Create the Conda environment from environment.yml
RUN conda env create -f environment.yml && \
    conda clean -afy

# Ensure the environment's binaries are on PATH
ENV PATH /opt/conda/envs/agentic-ai/bin:$PATH
# Default command
CMD ["python", "demos.py"]
