FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /workspace

# Install system packages
RUN apt-get update && \
    apt-get install -y \
    git \
    vim \
    python3-full \
    python3-lib2to3 \
    pip \
    python3-requests \
    python3-pytest \
    python3-notebook \
    python3-rioxarray \
    python3-xarray \
    python3-geopy \
    pipx \
    python3-venv && \
    apt-get clean


# Set the default command to start from the WORKDIR
CMD ["bash"]

