# Measuring the energy footprint of open LLMs

Our work from the swissAI hackathon challenge, [Measure footprint of open LLMs](https://swissai.dribdat.cc/project/44).

We used a Mac Studio to look at how prompt length, response length, language, and topic affected the energy readings while running Apertus. We also made a small comparison with Llama 7B. This repo contains the measurement scripts and CSV files from those sessions.

## Team Members

- **Agustín Herrerapicazo** - agustin.it@proton.me
- **Luis Barros** - luisantoniio1998@gmail.com
- **Stefan Aeschbacher** - stefan@aeschbacher.ch

## The measurement problem

Early checks showed a roughly 3–4× difference between `powermetrics` readings and physical measurements. We did not resolve that discrepancy during the hackathon. Idle readings also varied with background activity.

That limits what we can conclude from the numbers. These are exploratory measurements from one setup, not a calibrated comparison of whole-system energy use.

## Files

- `measure.sh` — collects `powermetrics` output into a CSV
- `quick_efficiency.py` — estimates tokens per joule and related metrics from a CSV and response text
- `test.py` — analysis and plotting code
- `data/` — saved idle, prompt-length, topic, language, and model-comparison runs
- `Measure energy in LLM.docx` — experiment notes

## Collect a measurement

The collection script uses macOS `powermetrics` and requests sudo access. Give it a numeric argument and a name for the output file:

```bash
chmod +x measure.sh
./measure.sh 300 "my_experiment"
```

The script labels the argument as seconds, but passes it to `powermetrics -n`, the sample-count option, with a configured interval of 100 ms. It also calculates elapsed time from the sample count rather than recording wall-clock time. Check that behaviour before using it for a timed comparison.

The CSV columns are:

```csv
sample,elapsed_time,power_mw,cumulative_energy_j,test_name
```

## Look at the results

The analysis scripts use Python, pandas, and matplotlib. For an efficiency estimate:

```bash
python3 quick_efficiency.py data/test_short_short_20250919_115157.csv "model output text"
```

Replace the text with the actual output from the matching run. The script estimates token count as text length divided by four; it does not use the model’s tokenizer. Its efficiency ratings are thresholds in the script, not a validated benchmark scale.

## What we observed

Our notes describe longer responses as the clearest contributor to higher readings, with less variation by prompt topic. They also record a higher reading for the Portuguese test and no clear winner in the small Apertus/Llama comparison.

Those observations need more controlled runs before treating them as model or language characteristics. In particular, the token estimate, background activity, and unresolved physical-measurement discrepancy all affect the comparison.

The raw files are here so the measurements and assumptions can be inspected alongside the code.
