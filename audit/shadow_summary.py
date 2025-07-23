import json

def summarize_shadow_trades(shadow_log='logs/shadow_trades_log_v4.jsonl'):
    wins = losses = 0
    with open(shadow_log, 'r') as f:
        for line in f:
            trade = json.loads(line)
            if trade.get('result') == 'win':
                wins += 1
            elif trade.get('result') == 'loss':
                losses += 1
    total = wins + losses
    win_rate = (wins / total * 100) if total else 0
    print(f"Shadow Trades Summary:\nWins: {wins}, Losses: {losses}, Win Rate: {win_rate:.2f}%")
