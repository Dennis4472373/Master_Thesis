from sklearn.metrics import cohen_kappa_score
from scipy.stats import spearmanr
import glob
import os
import pandas as pd
import regex as re
import csv


def get_label(score: int) -> str:
    """
    Get the label for the score.
    
    Parameters:
    score (int): The score to get the label for.
    
    Returns:
    str: The label for the score.
    """
    
    if score >= 4:
        label = 'High'
    elif score <= 2:
        label = 'Low'
    else:
        label = 'Medium'
    
    return label


def calculate_correlation(include_labels) -> list[list]:

    path = './Annotations'
    csv_files = glob.glob(os.path.join(path, "1.csv")) 

    labels = {}
    for f in csv_files: 

        num = int(re.findall('\\d+', f)[0])

        first_labels = []
        second_labels = []
        third_labels = []
        fourth_labels = []

        new_data = pd.read_csv(f)
        filtered_data = new_data.iloc[:, 22:97]
        rows = filtered_data.values.tolist()

        for i in range(len(rows[1])):
            if include_labels:
                first_labels.append(get_label(int(rows[2][i])))
                second_labels.append(get_label(int(rows[3][i])))
                third_labels.append(get_label(int(rows[4][i])))
                fourth_labels.append(get_label(int(rows[5][i])))
            else:
                first_labels.append(int(rows[2][i]))
                second_labels.append(int(rows[3][i]))
                third_labels.append(int(rows[4][i]))
                fourth_labels.append(int(rows[5][i]))

        print(first_labels)

        # labels[num] = cohen_kappa_score(first_labels, second_labels)
        labels[num] = []
        labels[num].append(spearmanr(first_labels, second_labels)[0])
        labels[num].append(spearmanr(first_labels, third_labels)[0])
        labels[num].append(spearmanr(first_labels, fourth_labels)[0])
        labels[num].append(spearmanr(second_labels, third_labels)[0])
        labels[num].append(spearmanr(second_labels, fourth_labels)[0])
        labels[num].append(spearmanr(third_labels, fourth_labels)[0])

        print(labels[num])
        avg_spearman = sum(labels[num]) / len(labels[num])

    return avg_spearman


def main():

    include_labels = False
    labels = calculate_correlation(include_labels)

    print(labels)

    with open("Annotations/agreement/agreement.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # writer.writerow(fieldnames)
        for data in labels.items():
            writer.writerow(data)

if __name__ == "__main__":
    main()
