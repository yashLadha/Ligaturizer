# Build environment for Ligaturizer.
#
# Provides FontForge (with Python bindings) plus the Python tooling the build
# needs (fonttools for postprocess.py), make and zip.
#
# Usage (from the repo root, with submodules checked out):
#
#   docker build -t ligaturizer .
#
#   # Build the fonts (output lands in ./fonts/output on the host).
#   # Run as your own uid/gid so the generated files are not owned by root.
#   docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work ligaturizer
#
#   # Run the unit tests instead of a build:
#   docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work ligaturizer \
#     python3 -m unittest discover -s tests -v
#
#   # Any other make target, e.g. a full release zip:
#   docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work ligaturizer make release
FROM debian:bookworm-slim

# fontforge          - the CLI used by `make` (fontforge -lang=py -script build.py)
# python3-fontforge  - the Python bindings imported by ligaturize.py
# python3-fonttools  - fontTools, used by postprocess.py
# make, zip          - build orchestration and release packaging
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        fontforge \
        python3-fontforge \
        python3-fonttools \
        make \
        zip \
    && rm -rf /var/lib/apt/lists/*

# FontForge and Python want a writable HOME/cache even when the container is
# run with an arbitrary --user; point everything at /tmp so builds never fail
# on an unwritable home directory.
ENV HOME=/tmp \
    XDG_CONFIG_HOME=/tmp \
    XDG_CACHE_HOME=/tmp

WORKDIR /work

# Default to the standard build (equivalent to `make`, i.e. without-characters).
CMD ["make"]
