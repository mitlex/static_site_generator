# Local Development Server
#
# This script performs a local build of the site and then launches 
# a simple HTTP server to preview the results.
#
# Usage:
#   ./main.sh
#
# Note: The server stays active until interrupted (Ctrl+C).

python3 src/main.py
cd public && python3 -m http.server 8888