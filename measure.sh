#!/bin/bash

# Enhanced Energy Measurement Script
# Usage: ./enhanced_measure.sh <duration_in_seconds> [test_name]
# Example: ./enhanced_measure.sh 60 "SS_math_test"

if [ -z "$1" ]; then
    echo "Error: missing duration (in seconds)."
    echo "Usage: $0 <duration_in_seconds> [test_name]"
    echo "Example: $0 60 SS_math_test"
    exit 1
fi

DURATION=$1
TEST_NAME=${2:-"energy_test"}
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
CSV_FILE="${TEST_NAME}_${TIMESTAMP}.csv"

echo "🚀 Enhanced Energy Measurement"
echo "⏱️  Duration: $DURATION seconds"
echo "📝 Test: $TEST_NAME"
echo "📄 Output: $CSV_FILE"
echo "------------------------------------------------------------"

# Create CSV header
echo "sample,elapsed_time,power_mw,cumulative_energy_j,test_name" > "$CSV_FILE"

echo "📊 Measuring power consumption..."
echo "   (CSV data being saved to $CSV_FILE)"

start_time=$(date +%s)

sudo powermetrics --samplers cpu_power -i 100 -n "$DURATION" | \
awk -v csv_file="$CSV_FILE" -v test_name="$TEST_NAME" -v start_time="$start_time" -v duration="$DURATION" '
BEGIN {
    total_sum = 0;
    total_count = 0;
    cumulative_energy = 0;
    sample_interval = 0.10;
    peak_power = 0;
    min_power = 999999;  # Initialize to a high value
}

/Combined Power/ {
    split($0, a, ":");
    power_mw = a[2] + 0;
    
    total_sum += power_mw;
    total_count++;

    # Track min/max power
    if (power_mw > peak_power) peak_power = power_mw;
    if (power_mw < min_power) min_power = power_mw;

    # Calculate elapsed time
    elapsed_time = total_count * sample_interval;
    
    # Calculate cumulative energy: Power(mW) * Time(s) / 1000 = Energy(J)
    energy_increment = (power_mw / 1000.0) * sample_interval;
    cumulative_energy += energy_increment;
    
    # Write to CSV
    printf "%d,%.2f,%.2f,%.6f,%s\n", total_count, elapsed_time, power_mw, cumulative_energy, test_name >> csv_file;
    
    # Real-time display every 20 samples (1 second)
    if (total_count % 20 == 0) {
        printf "\r⚡ Sample %4d | Time: %5.1fs | Power: %7.1f mW | Energy: %8.4f J", total_count, elapsed_time, power_mw, cumulative_energy;
        fflush();
    }
}

END {
    printf "\n";
    print "============================================================";
    
    if (total_count > 0) {
        total_avg = total_sum / total_count;
        total_energy_calculated = (total_avg / 1000.0) * (total_count * sample_interval);
        
        print "✅ MEASUREMENT COMPLETE";
        printf "📊 Total samples collected: %d\n", total_count;
        printf "⏱️  Actual duration: %.1f seconds\n", total_count * sample_interval;
        printf "⚡ Average power: %.1f mW\n", total_avg;
        printf "📈 Peak power: %.1f mW\n", peak_power;
        printf "📉 Min power: %.1f mW\n", min_power;
        printf "🔋 Total energy consumed: %.4f J\n", cumulative_energy;
        printf "📁 Data saved to: %s\n", csv_file;
        printf "📏 Samples: %d (%.1f samples/sec)\n", total_count, total_count/(total_count * sample_interval);
        
    } else {
        print "❌ No power data detected.";
        exit 1;
    }
}'

echo ""
echo "🎉 Measurement completed!"
echo "📊 CSV file ready: $CSV_FILE"
echo "💻 To visualize: python3 visualize_energy.py $CSV_FILE"