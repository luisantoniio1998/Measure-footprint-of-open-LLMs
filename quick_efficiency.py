#!/usr/bin/env python3
"""
Quick Token Efficiency Calculator
Takes CSV energy file and output text, calculates efficiency metrics.
Usage: python3 quick_efficiency.py <csv_file> "output text"
"""

import pandas as pd
import sys
import os

def count_tokens(text):
    """Simple token count: 4 characters ≈ 1 token"""
    return len(text) // 4

def calculate_efficiency(csv_file, output_text):
    """Calculate token efficiency from CSV and output text"""
    try:
        # Read energy data
        df = pd.read_csv(csv_file)

        # Count tokens in output
        token_count = count_tokens(output_text)

        # Extract energy metrics
        total_energy_j = df['cumulative_energy_j'].iloc[-1]
        duration_s = df['elapsed_time'].iloc[-1]
        avg_power_mw = df['power_mw'].mean()

        # Calculate efficiency metrics
        tokens_per_joule = token_count / total_energy_j if total_energy_j > 0 else 0
        tokens_per_second = token_count / duration_s if duration_s > 0 else 0
        joules_per_token = total_energy_j / token_count if token_count > 0 else 0

        # Efficiency rating
        if tokens_per_joule > 1000:
            rating = "⭐⭐⭐ Excellent"
        elif tokens_per_joule > 500:
            rating = "⭐⭐ Good"
        elif tokens_per_joule > 100:
            rating = "⭐ Fair"
        else:
            rating = "❌ Poor"

        # Display results
        print(f"\n⚡ QUICK EFFICIENCY ANALYSIS")
        print(f"=" * 50)
        print(f"📁 File: {os.path.basename(csv_file)}")
        print(f"📝 Output: {output_text[:60]}{'...' if len(output_text) > 60 else ''}")
        print(f"")
        print(f"📊 METRICS:")
        print(f"   🔢 Tokens: {token_count}")
        print(f"   ⚡ Energy: {total_energy_j:.4f} J")
        print(f"   ⏱️  Time: {duration_s:.1f} s")
        print(f"   💪 Power: {avg_power_mw:.1f} mW")
        print(f"")
        print(f"🎯 EFFICIENCY:")
        print(f"   📈 {tokens_per_joule:.1f} tokens/J")
        print(f"   ⚡ {joules_per_token:.6f} J/token")
        print(f"   🚀 {tokens_per_second:.1f} tokens/s")
        print(f"   🏆 {rating}")

        return {
            'tokens': token_count,
            'energy': total_energy_j,
            'tokens_per_joule': tokens_per_joule,
            'rating': rating
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 quick_efficiency.py <csv_file> \"output text\"")
        print("Example: python3 quick_efficiency.py test10_20250919_112715.csv \"The answer is 42\"")
        return

    csv_file = sys.argv[1]
    output_text = " ".join(sys.argv[2:])

    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return

    calculate_efficiency(csv_file, output_text)

if __name__ == "__main__":
    main()