import os


def format_post(filename):
    with open(filename, 'r', encoding='utf-8') as old, open(f'{filename}.bak', 'w', encoding='utf-8') as new:
        line = old.readline()
        while line:
            if line.startswith('tags'):
                tags = []
                line = old.readline()
                while line.startswith('- '):
                    tags.append(line[2:].strip())
                    line = old.readline()
                tag = ','.join(tags)
                new.write(f'tags: {tag}\n')
                continue

            if line.startswith('categories'):
                cats = []
                line = old.readline()
                while line.startswith('- '):
                    cats.append(line[2:].strip())
                    line = old.readline()
                cat = ','.join(cats)
                new.write(f'category: {cat}\n')
                continue

            if line.startswith('description:'):
                line = old.readline()
                continue

            if line.startswith('# '):
                new.write(f'##{line}')
                line = old.readline()
            else:
                new.write(line)
                line = old.readline()


for root, _, files in os.walk(r'../../content/posts'):
    for filename in files:
        _, ext = os.path.splitext(filename)
        if ext == '.md':
            rel_path = os.path.join(root, filename)
            format_post(rel_path)
            os.remove(rel_path)
            os.renames(f'{rel_path}.bak', rel_path)
