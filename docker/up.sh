#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

CONFIGS=""

load_config() {
    CFG="$1"
    find 
}

load_config base
load_config "$(hostname)"
