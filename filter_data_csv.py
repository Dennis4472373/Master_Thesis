import csv
import evaluate
from tqdm import tqdm


def compare_generations(rows: list[dict]) -> list[dict]:
    """
    Compate the generation sentences with each other
    using ChrF score and remove rows where score is lower than 70
    Args:
        The filtered rows where Source length > 5
    Returns:
        Dictionary: The filtered rows on total ChrF
    """

    chrf = evaluate.load('chrf')

    for row in tqdm(rows):
        row['Total_ChrF'] = chrf.compute(
            predictions=[row['Gen_comp'], row['Gen_comp'], row['Gen_comp1']],
            references=[[row['Gen_comp1']], [row['Gen_comp2']], [row['Gen_comp2']]])['score']
    rows_keep = [row for row in rows if row['Total_ChrF'] > 70]

    return rows_keep


def main():

    with open('Data/flan-t5-xl_cts_fine-tune_chrf.csv') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        rows_keep = [row for row in csv_reader if len(row['Source'].split()) > 4]

    filtered_rows = compare_generations(rows_keep)

    with open("Filtered_data/flan-t5-xl/test.csv", "w", newline="") as f:
        w = csv.DictWriter(f, filtered_rows[0].keys())
        w.writeheader()
        w.writerows(filtered_rows)

if __name__ == "__main__":
    main()
