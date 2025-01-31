import csv
import random
import glob
import os
import pandas as pd


def load_data(num) -> list[list]:

    path = './Annotations'
    csv_file = glob.glob(os.path.join(path, f"{num}.csv"))

    if csv_file != []:
        df = pd.read_csv(csv_file[0])
        filtered_df = df.iloc[:, 22:97]
        return filtered_df.values.tolist()
    else:
        return None


def select_one_index(indexes: list) -> int:
    """
    Select index from a list of indexes.
    
    Parameters:
    indexes (list): The list of indexes.
    
    Returns:
    int: The selected index.
    """
    
    if len(indexes) == 1:
        index = indexes[0]
    else:
        index = random.choice(indexes)

    return index


def add_preferences(output_data: dict[list], text: list[list], column_index: int, first_index: int, second_index: int) -> None:
    """
    Add preferences to the output data dictionary.
    
    Parameters:
    output_data (dict[list]): The dictionary to store the output data.
    input_data (list[list]): The input data from the CSV file.
    column_index (int): The current column index being processed.
    first_index (int): The index of the first preference.
    second_index (int): The index of the second preference.

    Returns:
    None
    """

    # Check if '-' is in the text, otherwise edit the text so the prompt is included
    if '-' not in text[column_index]:
        text[column_index] = text[column_index] + ' - ' + text[column_index]
    if '-' not in text[column_index+first_index]:
        text[column_index+first_index] = text[column_index].split(' - ')[0] + ' - ' + text[column_index+first_index]
    if '-' not in text[column_index+second_index]:
        text[column_index+second_index] = text[column_index].split(' - ')[0] + ' - ' + text[column_index+second_index]

    output_data['prompt'].append(text[column_index].split(' - ')[0])
    output_data['chosen'].append(text[column_index+first_index].split(' - ')[1])
    output_data['rejected'].append(text[column_index+second_index].split(' - ')[1])

def main():

    # Create output dict
    reward_model_data = {'prompt': [], 'chosen': [], 'rejected': []}

    for num in range(1, 9):
        rows = load_data(num)
        if rows:
            num_annotations = len(rows) - 2

            # Gather and format the Reward Model data
            for i in range(0, len(rows[1]), 3):
                if num_annotations == 1:
                    scores = [int(rows[2][i]), int(rows[2][i+1]), int(rows[2][i+2])]
                else:
                    annotator_scores = {}
                    for j in range(num_annotations):
                        annotator_scores[j] = [int(rows[2+j][i]), int(rows[2+j][i+1]), int(rows[2+j][i+2])]

                    # Calculate average scores
                    columns = list(zip(*annotator_scores.values()))
                    scores = [sum(column)/len(column) for column in columns]
                    
                # Find max score index
                max_scores_indexes = [j for j, x in enumerate(scores) if x == max(scores)]
                max_score_index = select_one_index(max_scores_indexes)

                # Find min score index
                min_scores_indexes = [j for j, x in enumerate(scores) if x == min(scores) and j != max_score_index]
                min_score_index = select_one_index(min_scores_indexes)

                # Find median score index
                median_score_index = [j for j, x in enumerate(scores) if j != min_score_index and j != max_score_index][0]

                # Add preferences to dataset
                # Highest > Lowest
                add_preferences(reward_model_data, rows[0], i, max_score_index, min_score_index)

                # Highest > Median
                add_preferences(reward_model_data, rows[0], i, max_score_index, median_score_index)

                # Median > Lowest
                add_preferences(reward_model_data, rows[0], i, median_score_index, min_score_index)
        else:
            continue

    # Write Reward Model data to CSV file
    filename = 'reward_data.csv'
    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(reward_model_data.keys())
        w.writerows(zip(*reward_model_data.values()))

    print(f'Succesfully wrote all data to {filename}')

if __name__ == "__main__":
    main()
