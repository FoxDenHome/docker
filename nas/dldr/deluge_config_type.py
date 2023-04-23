#!/usr/bin/python3

import sys

if sys.argv[4] == "array":
    sys.argv[3] = [sys.argv[3]]
elif sys.argv[4] == "int":
    sys.argv[3] = int(sys.argv[3])
elif sys.argv[4] == "float":
    sys.argv[3] = float(sys.argv[3])
elif sys.argv[4] == "string":
    pass
else:
    raise ValueError(f"Invalid type {sys.argv[4]}")

