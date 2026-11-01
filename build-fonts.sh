#!/usr/bin/env bash
# Build the ligaturized fonts end to end with Docker, starting from a fresh clone.

set -euo pipefail

IMAGE=ligaturizer
FIRA_ZIP_URL=https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip
FIRA_TTF_DIR=fonts/fira/distr/ttf
FIRA_WEIGHTS="Bold SemiBold Retina Medium Regular Light"
SCP_DIR=fonts/source-code-pro
OUTPUT_DIR=fonts/output

target=""
skip_image=0
install=0
tmp_dir=""
marker=""

usage() {
    cat <<EOF
Usage: $(basename "$0") [options]

Build the ligaturized fonts in a Docker container. Initializes the Fira Code
and Source Code Pro submodules, downloads the Fira Code 6.2 TTFs if they
are missing, builds the '$IMAGE' image, runs the build and checks
that $OUTPUT_DIR/LigaSrcPro-*.ttf files were produced.

Options:
  --target <name>  Run 'make <name>' in the container instead of the
                   image default ('make').
  --skip-image     Reuse the existing '$IMAGE' image instead of rebuilding it.
  --install        Copy $OUTPUT_DIR/*.ttf into the user font directory
                   (~/Library/Fonts on macOS, ~/.local/share/fonts on Linux).
  -h, --help       Show this help and exit.
EOF
}

step() {
    printf '\n==> %s\n' "$*"
}

die() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

cleanup() {
    if [ -n "$tmp_dir" ]; then
        rm -rf "$tmp_dir"
    fi
    if [ -n "$marker" ]; then
        rm -f "$marker"
    fi
}
trap cleanup EXIT

while [ $# -gt 0 ]; do
    case "$1" in
        --target)
            [ $# -ge 2 ] || die "--target requires a make target"
            target="$2"
            shift 2
            ;;
        --target=*)
            target="${1#--target=}"
            shift
            ;;
        --skip-image)
            skip_image=1
            shift
            ;;
        --install)
            install=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            usage >&2
            die "unknown option: $1"
            ;;
    esac
done

cd "$(cd "$(dirname "$0")" && pwd)"

step "Checking required tools"
missing=""
for tool in docker git curl unzip; do
    command -v "$tool" >/dev/null 2>&1 || missing="$missing $tool"
done
[ -z "$missing" ] || die "missing required tools:$missing"
docker info >/dev/null 2>&1 || die "cannot reach the Docker daemon; is Docker running?"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "$PWD is not a git checkout"

step "Initializing the fonts/fira and $SCP_DIR submodules"
git submodule update --init fonts/fira "$SCP_DIR"
ls "$SCP_DIR"/TTF/*.ttf >/dev/null 2>&1 || die "$SCP_DIR/TTF has no .ttf files after submodule update"

step "Installing Fira Code 6.2 TTFs into $FIRA_TTF_DIR"
fira_missing=0
for weight in $FIRA_WEIGHTS; do
    [ -f "$FIRA_TTF_DIR/FiraCode-$weight.ttf" ] || fira_missing=1
done
if [ "$fira_missing" -eq 0 ]; then
    echo "Fira Code TTFs already present, skipping"
else
    tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/ligaturizer.XXXXXX")
    echo "Downloading $FIRA_ZIP_URL"
    curl -fsSL -o "$tmp_dir/fira.zip" "$FIRA_ZIP_URL"
    unzip -q "$tmp_dir/fira.zip" -d "$tmp_dir/fira"
    [ -d "$tmp_dir/fira/ttf" ] || die "release archive has no ttf/ directory"
    mkdir -p "$FIRA_TTF_DIR"
    cp "$tmp_dir"/fira/ttf/*.ttf "$FIRA_TTF_DIR"/
    for weight in $FIRA_WEIGHTS; do
        [ -f "$FIRA_TTF_DIR/FiraCode-$weight.ttf" ] || die "FiraCode-$weight.ttf missing from release archive"
    done
fi

if [ "$skip_image" -eq 1 ]; then
    step "Reusing existing Docker image '$IMAGE'"
    docker image inspect "$IMAGE" >/dev/null 2>&1 || die "image '$IMAGE' not found; run without --skip-image"
else
    step "Building Docker image '$IMAGE'"
    docker build -t "$IMAGE" .
fi

# Only files newer than this marker count, so output left over from an earlier run cannot mask a failed build.
marker=$(mktemp "${TMPDIR:-/tmp}/ligaturizer-marker.XXXXXX")

if [ -n "$target" ]; then
    step "Running 'make $target' in the container"
    docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work "$IMAGE" make "$target"
else
    step "Running the default build in the container"
    docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work "$IMAGE"
fi

step "Verifying output in $OUTPUT_DIR"
produced=$(find "$OUTPUT_DIR" -name 'LigaSrcPro-*.ttf' -newer "$marker" 2>/dev/null | sort)
[ -n "$produced" ] || die "no LigaSrcPro-*.ttf files were produced in $OUTPUT_DIR; check the build log above"
echo "Produced files:"
printf '%s\n' "$produced" | while IFS= read -r f; do
    printf '  %s\n' "$f"
done

if [ "$install" -eq 1 ]; then
    case "$(uname -s)" in
        Darwin) font_dir="$HOME/Library/Fonts" ;;
        Linux) font_dir="$HOME/.local/share/fonts" ;;
        *) die "--install is only supported on macOS and Linux" ;;
    esac
    step "Installing fonts into $font_dir"
    mkdir -p "$font_dir"
    cp "$OUTPUT_DIR"/*.ttf "$font_dir"/
    if [ "$(uname -s)" = Linux ] && command -v fc-cache >/dev/null 2>&1; then
        fc-cache -f "$font_dir"
    fi
fi

step "Done"
