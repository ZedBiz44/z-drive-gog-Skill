#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_file="$root_dir/SKILL.md"
manifest_file="$root_dir/package-resources.txt"

if [[ ! -f "$skill_file" || ! -f "$manifest_file" ]]; then
  echo "ERROR: SKILL.md and package-resources.txt are required." >&2
  exit 1
fi

skill_name="$(sed -n 's/^name: *//p' "$skill_file" | head -n 1 | xargs)"
if [[ -z "$skill_name" ]]; then
  echo "ERROR: Could not read skill name from SKILL.md." >&2
  exit 1
fi

package_dir="$root_dir/dist/$skill_name"
rm -rf "$package_dir"
mkdir -p "$package_dir"
cp "$skill_file" "$package_dir/SKILL.md"

while IFS= read -r resource || [[ -n "$resource" ]]; do
  resource="${resource%%#*}"
  resource="$(printf '%s' "$resource" | xargs)"
  [[ -z "$resource" ]] && continue
  case "$resource" in
    assets|references|scripts)
      [[ -d "$root_dir/$resource" ]] || { echo "ERROR: Missing $resource directory." >&2; exit 1; }
      cp -a "$root_dir/$resource" "$package_dir/$resource"
      ;;
    *)
      echo "ERROR: Unsupported package resource: $resource" >&2
      exit 1
      ;;
  esac
done < "$manifest_file"

find "$package_dir" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$package_dir" -type f -name '*.pyc' -delete

printf 'Built deployable package: %s\n' "$package_dir"
