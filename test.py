#!/usr/bin/env python3
"""
Quick Energy Data Visualizer - 2 Hour Version
Usage: python3 quick_visualizer.py file1.csv [file2.csv ...]
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def analyze_single_file(csv_file):
    """Quick analysis of a single CSV file"""
    try:
        df = pd.read_csv(csv_file)
        
        # Basic stats
        avg_power = df['power_mw'].mean()
        max_power = df['power_mw'].max()
        min_power = df['power_mw'].min()
        std_power = df['power_mw'].std()
        total_energy = df['cumulative_energy_j'].iloc[-1]
        duration = df['elapsed_time'].iloc[-1]

        print(f"\n📊 {csv_file}:")
        print(f"   ⚡ Average Power: {avg_power:.1f} mW")
        print(f"   📊 Std Deviation: {std_power:.1f} mW")
        print(f"   📈 Peak Power: {max_power:.1f} mW")
        print(f"   📉 Min Power: {min_power:.1f} mW")
        print(f"   🔋 Total Energy: {total_energy:.4f} J")
        print(f"   ⏱️  Duration: {duration:.1f} seconds")
        
        return {
            'file': csv_file,
            'avg_power': avg_power,
            'std_power': std_power,
            'total_energy': total_energy,
            'duration': duration,
            'df': df
        }
        
    except Exception as e:
        print(f"❌ Error reading {csv_file}: {e}")
        return None

def create_quick_plots(data_list):
    """Create quick comparison plots"""
    if len(data_list) == 1:
        # Single test plot
        data = data_list[0]
        df = data['df']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"Energy Analysis: {os.path.basename(data['file'])}")
        
        # Power over time
        ax1.plot(df['elapsed_time'], df['power_mw'], linewidth=2, label='Power')
        ax1.axhline(y=data['avg_power'], color='red', linestyle='--',
                   label=f"Avg: {data['avg_power']:.1f} mW")
        ax1.fill_between(df['elapsed_time'],
                        data['avg_power'] - data['std_power'],
                        data['avg_power'] + data['std_power'],
                        alpha=0.2, color='red',
                        label=f"±1σ: {data['std_power']:.1f} mW")
        ax1.set_title('Power Consumption')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Power (mW)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Cumulative energy
        ax2.plot(df['elapsed_time'], df['cumulative_energy_j'],
                color='orange', linewidth=2)
        ax2.set_title('Cumulative Energy')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Energy (J)')

        # Add final cumulative energy annotation
        final_energy = data['total_energy']
        ax2.annotate(f'Final: {final_energy:.4f} J',
                    xy=(df['elapsed_time'].iloc[-1], final_energy),
                    xytext=(df['elapsed_time'].iloc[-1] * 0.7, final_energy * 0.8),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))

        ax2.grid(True, alpha=0.3)
        
    else:
        # Comparison plot
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('LLM Energy Comparison')
        
        # Extract names and metrics
        names = [os.path.basename(d['file']).replace('.csv', '')[:15] for d in data_list]
        avg_powers = [d['avg_power'] for d in data_list]
        std_powers = [d['std_power'] for d in data_list]
        total_energies = [d['total_energy'] for d in data_list]
        
        # Average power comparison with error bars
        bars1 = ax1.bar(names, avg_powers, yerr=std_powers, alpha=0.7,
                        color=['blue', 'red', 'green', 'orange'][:len(names)],
                        capsize=5)
        ax1.set_title('Average Power (±1σ)')
        ax1.set_ylabel('Power (mW)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Total energy comparison  
        bars2 = ax2.bar(names, total_energies, alpha=0.7, color=['blue', 'red', 'green', 'orange'][:len(names)])
        ax2.set_title('Total Energy')
        ax2.set_ylabel('Energy (J)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, avg_val, std_val in zip(bars1, avg_powers, std_powers):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std_val + max(avg_powers)*0.02,
                    f'{avg_val:.1f}±{std_val:.1f}', ha='center', va='bottom', fontsize=9)

        for bar, value in zip(bars2, total_energies):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(total_energies)*0.01,
                    f'{value:.4f} J', ha='center', va='bottom', fontweight='bold')
        
        # Power over time comparison
        for i, data in enumerate(data_list):
            df = data['df']
            # Normalize time for comparison
            normalized_time = df['elapsed_time'] / df['elapsed_time'].iloc[-1]
            ax3.plot(normalized_time, df['power_mw'],
                    label=names[i], linewidth=2, alpha=0.8)
        
        ax3.set_title('Power Profiles')
        ax3.set_xlabel('Normalized Time (0-1)')
        ax3.set_ylabel('Power (mW)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    output_name = "energy_analysis.png"
    plt.savefig(output_name, dpi=200, bbox_inches='tight')
    print(f"\n📊 Plot saved as: {output_name}")
    # plt.show()  # Comment out to avoid interactive display

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quick_visualizer.py file1.csv [file2.csv ...]")
        print("Example: python3 quick_visualizer.py SS_math_*.csv SL_explanation_*.csv")
        return
    
    print("🚀 Quick Energy Analysis")
    print("=" * 30)
    
    # Load and analyze all files
    data_list = []
    for csv_file in sys.argv[1:]:
        result = analyze_single_file(csv_file)
        if result:
            data_list.append(result)
    
    if not data_list:
        print("❌ No valid data files found!")
        return
    
    # Create plots
    create_quick_plots(data_list)
    
    # Quick comparison summary
    if len(data_list) > 1:
        print(f"\n🔍 QUICK COMPARISON:")
        energies = [d['total_energy'] for d in data_list]
        powers = [d['avg_power'] for d in data_list]
        
        most_efficient = min(data_list, key=lambda x: x['total_energy'])
        least_efficient = max(data_list, key=lambda x: x['total_energy'])
        
        print(f"   🏆 Most efficient: {os.path.basename(most_efficient['file'])} ({most_efficient['total_energy']:.4f} J)")
        print(f"   ⚠️  Least efficient: {os.path.basename(least_efficient['file'])} ({least_efficient['total_energy']:.4f} J)")
        
        improvement = (least_efficient['total_energy'] / most_efficient['total_energy'] - 1) * 100
        print(f"   📈 Potential improvement: {improvement:.1f}%")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()