# 🎯 RosettaDeltaAnalyzer

This repository contains a Python script for analyzing and comparing Rosetta score files (`.sc`). The script loads, processes, and visualizes score data, allowing users to compare multiple designs against a reference structure.

---

## 📌 Overview

This is a Python-based tool that processes `.sc` files from Rosetta, computes score differences between various designs and a reference structure, and visualizes the results.

### 🚀 Features

✅ Parses and compiles scores from `.sc` files automatically.  
✅ Computes deltas for specified metrics.  
✅ Generates comparative bar plots for visualization.  
✅ Supports CSV export of processed data.  
✅ User-friendly CLI with customizable parameters.  

---

## 🔧 Installation

### 📌 Using `pip`

```sh
pip install -r requirements.txt
```

### 🏗️ Using Conda

```sh
conda env create -f environment.yml
conda activate rosetta_delta_analysis
```

---

## 📁 Requirements File (`requirements.txt`)

```
pandas
matplotlib
seaborn
numpy
```

---

## ⚙️ Environment File (`environment.yml`)

```yaml
name: rosetta_delta_analysis
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.9
  - pandas
  - matplotlib
  - seaborn
  - numpy
```

---

## 🎯 Usage

Run the script using the following command:

```sh
python analyse_delta_run.py <directory_path> <reference_file> --metrics <metric1> <metric2> --output_plot <output_file> --output_csv <output_file>
```

### 💡 Example:

```sh
python  analyse_delta_run.py ./scores/ reference_score.sc --metrics total_score ddG --output_plot comparison.png --output_csv results.csv
```

---

## 📊 Arguments

| Argument         | Description                                                                                |
|-----------------|--------------------------------------------------------------------------------------------|
| `directory_path` | Path to the directory containing `.sc` files.                                              |
| `reference_file` | Full path to the reference `.sc` file.                                                     |
| `--metrics`      | List of metrics to analyze (default: `total_score`, `ddG`, `sasa_1comp`, `sc1_1comp`, etc). |
| `--output_plot`  | Output file name for the plot (default: `rosetta_k18c2_scores.png`).                       | 
| `--output_csv`   | Output file name for the CSV of computed deltas.                                           |
| `--help`         | Display usage information.                                                                 |

---

## 📜 License

📖 This project is licensed under the **MIT License**.

---

## 🤝 Contributing

We welcome contributions! Please fork the repository and submit a pull request for any improvements.

---

## 📧 Contact

For questions or suggestions, feel free to reach out! 😊
