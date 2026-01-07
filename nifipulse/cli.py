import argparse
from nifipulse.extract_metrics import nifipulse

def main():
    parser = argparse.ArgumentParser(description="Run NifiPulse ETL CLI")
    parser.add_argument(
        "--poll",
        type=int,
        default=10, 
        metavar="N",
        help="Number of polling cycles (default 10; use 0 to run forever)."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Seconds between polling cycles (default 60)."
    )
    args = parser.parse_args()
    nifipulse(poll_count=args.poll, interval=args.interval)

if __name__ == "__main__":
    main()