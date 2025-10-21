import csv
import re

def parse_markdown_to_csv(md_file, csv_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_block = ""
    current_subject = ""
    current_topic = ""

    for line in lines:
        line = line.strip()
        if not line or line.startswith('# ') or line == '---' or line.startswith('**'):
            continue

        if line.startswith('## '):
            current_block = line[3:].strip()
            current_subject = ""
            current_topic = ""
        elif line.startswith('### '):
            current_subject = re.sub(r'^\d+\.\s*', '', line[4:].strip())
            current_topic = ""
        elif line.startswith('#### '):
            current_topic = re.sub(r'^\d+\.\d+\.\s*', '', line[5:].strip())
        elif line.startswith('- '):
            subtopic = line[2:].strip()
            data.append([current_block, current_subject, current_topic, subtopic])
        elif current_topic and not line.startswith('-'):
            # If there's a current topic and this line is not a subtopic, it might be a continuation or new topic
            # For simplicity, if it's not starting with -, treat as subtopic if topic exists
            if current_topic:
                data.append([current_block, current_subject, current_topic, line])

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Bloco', 'Disciplina', 'Topico', 'Subtopico'])
        writer.writerows(data)

if __name__ == "__main__":
    parse_markdown_to_csv('edital-verticalizado.md', 'conteudo_programatico.csv')