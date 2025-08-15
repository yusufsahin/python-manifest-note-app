import argparse, os, sys
import uvicorn
from .app import create_app

def main():
    p = argparse.ArgumentParser(description="Manifest-driven FastAPI server")
    p.add_argument("--manifest", required=True, help="Path to manifest.json")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--reload", action="store_true")
    args = p.parse_args()

    if not os.path.isfile(args.manifest):
        print(f"Manifest file not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    app = create_app(args.manifest)
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
