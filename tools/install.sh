#!/usr/bin/env bash
# Symlink every maintained skill (<repo>/<name>/SKILL.md) and every pinned
# third-party skill into the harness skill directories.
#
# - Links always point at the main checkout, never at a linked worktree.
# - Existing symlinks into this repository that no longer resolve to a skill
#   are removed (renamed or deleted skills).
# - Real directories and links to other locations are left alone and reported.
#
# Usage: tools/install.sh [--dry-run] [harness-dir ...]
#   default harness dirs: ~/.claude/skills ~/.codex/skills (only those that exist)
set -euo pipefail

DRY=0
if [[ "${1:-}" == "--dry-run" ]]; then DRY=1; shift; fi

ROOT=$(git -C "$(dirname "$0")" worktree list --porcelain | sed -n '1s/^worktree //p')
HARNESS=("$@")
if [[ ${#HARNESS[@]} -eq 0 ]]; then
  for d in "$HOME/.claude/skills" "$HOME/.codex/skills"; do [[ -d "$d" ]] && HARNESS+=("$d"); done
fi

run() { if [[ $DRY -eq 1 ]]; then echo "would: $*"; else "$@"; fi; }

# Skill directories: maintained skills plus third-party skills pinned in SOURCES.md.
mapfile -t SKILLS < <(
  find "$ROOT" -mindepth 2 -maxdepth 2 -name SKILL.md -not -path "$ROOT/.worktree/*" -printf '%h\n'
  if [[ -f "$ROOT/third-party/SOURCES.md" ]]; then
    grep -oE '^\| `[^`]+` \|.*\| `skills/[^`]+` \|$' "$ROOT/third-party/SOURCES.md" |
      sed -E 's/^\| `([^`]+)` \|.*\| `([^`]+)` \|$/\1\/\2/' |
      while read -r rel; do [[ -f "$ROOT/third-party/$rel/SKILL.md" ]] && echo "$ROOT/third-party/$rel"; done
  fi
)

for h in "${HARNESS[@]}"; do
  echo "== $h"
  # Remove stale links into this repository.
  for link in "$h"/*; do
    [[ -L "$link" ]] || continue
    raw=$(readlink "$link")
    case "$raw" in
      "$ROOT"/*) [[ -f "$raw/SKILL.md" ]] || { echo "remove stale $link -> $raw"; run rm "$link"; } ;;
    esac
  done
  for dir in "${SKILLS[@]}"; do
    name=$(basename "$dir")
    dest="$h/$name"
    if [[ -L "$dest" ]]; then
      [[ "$(readlink -f "$dest")" == "$dir" ]] && continue
      echo "relink $name"
      run ln -sfn "$dir" "$dest"
    elif [[ -e "$dest" ]]; then
      echo "skip $name: $dest is a real directory or file; replace it by hand if it is a stale copy"
    else
      echo "link $name"
      run ln -s "$dir" "$dest"
    fi
  done
done
