import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
import numpy as np

def load_and_compile_scores(directory_path):
    """
    Load and compile scores from all .sc files in the specified directory.
    
    Args:
        directory_path (str): Path to the directory containing .sc files.
    
    Returns:
        pd.DataFrame: Combined DataFrame containing scores from all files.
    """
    combined_scores = pd.DataFrame()

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.sc'):
            file_path = os.path.join(directory_path, file_name)
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                
                score_lines = [line for line in lines if line.startswith("SCORE:")]
                
                
                header = score_lines[0].split()[1:]
                data = [line.split()[1:] for line in score_lines[1:]]
                
                
                df = pd.DataFrame(data, columns=header)
                
                
                df = df.apply(pd.to_numeric, errors='coerce')
                
                
                df['file_name'] = file_name.replace('_score.sc', '')
                
                
                if 'total_score' in df.columns:
                    combined_scores = pd.concat([combined_scores, df], ignore_index=True)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    return combined_scores

def calculate_deltas(reference, others, metrics):
    """
    Calculate deltas for specified metrics between reference and other designs.
    
    Args:
        reference (pd.DataFrame): DataFrame containing reference scores.
        others (pd.DataFrame): DataFrame containing scores of other designs.
        metrics (list): List of metrics to calculate deltas for.
    
    Returns:
        pd.DataFrame: DataFrame containing deltas for specified metrics.
    """
    deltas = others.copy()
    
    for metric in metrics:
        if metric in reference.columns and metric in others.columns:
            deltas[metric] = others[metric] - reference[metric].values[0]
    
    return deltas

def plot_comparison(reference, deltas, metrics, output_file):
    """
    Plot comparison of deltas for specified metrics.
    
    Args:
        reference (pd.DataFrame): DataFrame containing reference scores.
        deltas (pd.DataFrame): DataFrame containing deltas for specified metrics.
        metrics (list): List of metrics to plot.
        output_file (str): Path to save the output plot.
    """
    sns.set(style="white")
    sns.set_context("talk")
    plt.rcParams["font.family"] = "Arial"
    
    colors = sns.color_palette("husl", len(metrics))
    fig, axes = plt.subplots(nrows=1, ncols=len(metrics), figsize=(20, 5))
    axes = np.atleast_1d(axes)  

    for i, metric in enumerate(metrics):
        if metric in deltas.columns:
            sns.barplot(x='file_name', y=metric, data=deltas, ax=axes[i], color=colors[i], edgecolor='black')
            axes[i].set_title(f'Δ {metric}')
            axes[i].set_xlabel('Designs')
            axes[i].set_ylabel(f'Δ {metric}')
            axes[i].tick_params(axis='x', rotation=90)
            axes[i].spines['top'].set_visible(True)
            axes[i].spines['right'].set_visible(True)
            axes[i].spines['bottom'].set_visible(True)
            axes[i].spines['left'].set_visible(True)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Analyze and compare Rosetta scores.")
    parser.add_argument('directory_path', type=str, help="Path to the directory containing .sc files.")
    parser.add_argument('reference_file', type=str, help="Full path to the reference file (e.g., /path/to/I3_k18_score.sc).")
    parser.add_argument('--metrics', type=str, nargs='+', default=['total_score', 'ddG', 'sasa_1comp', 'sc1_1comp'], help="List of metrics to analyze.")
    parser.add_argument('--output_plot', type=str, default='rosetta_scores.png', help="Output file name for the plot.")
    parser.add_argument('--output_csv', type=str, help="Output file name for the CSV of the data.")
    
    args = parser.parse_args()
    
    all_scores = load_and_compile_scores(args.directory_path)
    reference_file_name = os.path.basename(args.reference_file).replace('_score.sc', '')
    reference_data = all_scores[all_scores['file_name'] == reference_file_name]
    other_data = all_scores[all_scores['file_name'] != reference_file_name]

    if not reference_data.empty and not other_data.empty:
        deltas = calculate_deltas(reference_data, other_data, args.metrics)
        plot_comparison(reference_data, deltas, args.metrics, args.output_plot)
        
        if args.output_csv:
            deltas.to_csv(args.output_csv, index=False)
    else:
        print("Failed to load the reference or other data files correctly. Check the paths and file names.")

if __name__ == "__main__":
    main()
