from pathlib import Path
from collections import defaultdict
import csv

def summarize_file_extensions(directories, csv_file_path):
    file_info = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'size': 0, 'sample_path': ''}))

    for directory in directories:
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            print(f"Directory {directory} does not exist or is not a directory.")
            continue

        for file in path.rglob('*.*'):
            extension = file.suffix[1:]  # Exclude the dot
            file_info[directory][extension]['count'] += 1
            file_info[directory][extension]['size'] += file.stat().st_size / (1024 * 1024)  # Convert bytes to MB
            # Store the path of the first encountered file of each extension as a sample
            if not file_info[directory][extension]['sample_path']:
                file_info[directory][extension]['sample_path'] = str(file)

    # Write the collected information to a CSV file, with sorting
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(['Directory', 'Extension', 'Count', 'Total Size (MB)', 'Sample File Path'])

        # Iterate over each directory
        for directory, extensions in file_info.items():
            # Sort extensions within this directory by size, in descending order
            sorted_extensions_by_size = sorted(extensions.items(), key=lambda x: x[1]['size'], reverse=True)
            # Write each extension's data to the CSV, now including sample path
            for extension, info in sorted_extensions_by_size:
                writer.writerow([directory, extension, info['count'], round(info['size'], 2), info['sample_path']])  # Size is already in MB, rounded to 2 decimal places

    print(f"CSV file '{csv_file_path}' has been created with directory, extension, count, size in MB, and a sample file path, sorted by size within each directory.")

# Example usage
if __name__ == '__main__':
    directories = ['A', 'B']
    csv_file_path = 'file_extension_summary_per_directory_with_sample.csv'
    summarize_file_extensions(directories, csv_file_path)
