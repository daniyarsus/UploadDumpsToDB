import json
from collections import defaultdict


def find_duplicate_uuids(json_file_path) -> dict[str, set[str]]:
    uuid_counts = defaultdict(int)

    with open(json_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    process_data(data, uuid_counts)
                except json.JSONDecodeError as e:
                    print(f"Ошибка декодирования JSON: {e}")

    duplicates = {uuid for uuid, count in uuid_counts.items() if count > 1}

    return duplicates


def process_data(data, uuid_counts) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(key, str) and len(key) == 36 and key.count('-') == 4:
                uuid_counts[key] += 1
            if isinstance(value, (dict, list)):
                process_data(value, uuid_counts)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                process_data(item, uuid_counts)


json_file_path = 'dump_beru_product_20240717.1409052128.jsonl'
duplicates = find_duplicate_uuids(json_file_path)

if duplicates:
    print("Найдены дублирующиеся UUID:")
    for uuid in duplicates:
        print(uuid)
else:
    print("Дублирующиеся UUID не найдены.")
