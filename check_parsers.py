import sys
sys.path.insert(0, 'src')
from ayga_mcp_client.server import PARSERS

print(f'Total parsers: {len(PARSERS)}')
print('\nParser IDs:')
for p in PARSERS:
    print(f'  {p["id"]}')
