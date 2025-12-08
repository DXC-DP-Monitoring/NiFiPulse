import argparse
from nifipulse.extract_metrics import nifipulse

def main():
    parser = argparse.ArgumentParser(description="Run NifiPulse ETL CLI")
    parser.add_argument(
        "--poll",
        nargs="?",
        const=10,            # `--poll` with no value → 10
        type=int,
        default=10,          # no `--poll` at all → 10
        help="Number of polling cycles (default 10). Use --poll 0 to run forever."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Seconds between polling cycles (default 5)."
    )
    args = parser.parse_args()
    nifipulse(poll_count=args.poll, interval=args.interval)

if __name__ == "__main__":
    main()