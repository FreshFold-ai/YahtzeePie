#!/bin/bash
cd "$(dirname "$0")"
export PATH="$HOME/.local/share/coursier/bin:$PATH"
sbt run
