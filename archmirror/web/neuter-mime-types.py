#!/usr/bin/env python3

# /sbin/neuter-mime-type.sh 'text/html' && \
# /sbin/neuter-mime-type.sh 'application/xhtml+xml' && 
# /sbin/neuter-mime-type.sh 'text/html-sandboxed' && \
# /sbin/neuter-mime-type.sh 'text/javascript'

from collections import defaultdict

TYPE_SWAPS = {
    'text/html': 'text/plain',
    'application/xhtml+xml': 'text/plain',
    'text/html-sandboxed': 'text/plain',
    'text/javascript': 'text/plain',
}

def main():
    with open('/etc/mime.types', 'r') as f:
        lines = f.readlines()

    mime_type_additions = defaultdict(list)
    mime_type_lines = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('#') or not line:
            continue

        mime_type, *extensions = line.split()
        mime_type_lines[mime_type] = i
        if mime_type in TYPE_SWAPS:
            lines[i] = f"#{lines[i]}"
            mime_type_additions[mime_type] += extensions

    for mime_type, new_mime_type in TYPE_SWAPS.items():
        extensions = mime_type_additions[mime_type]
        if not extensions:
            continue

        if new_mime_type in mime_type_lines:
            i = mime_type_lines[new_mime_type]
            lines[i] = lines[i].strip() + ' ' + ' '.join(extensions) + '\n'
        else:
            lines.append(f"{new_mime_type}     {' '.join(extensions)}\n")

    output = ''.join(lines)
    with open('/etc/mime.types.neutered', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()
