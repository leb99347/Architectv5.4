# Entry point for ArchitectV4 system
from data.fetch_oanda import get_price_data
from signals.signal_generator import generate_signal
from core.logging import log_event

def main():
    prices = get_price_data()
    signal = generate_signal(prices)
    log_event("signal_generator", "signal", signal)

if __name__ == "__main__":
    main()
