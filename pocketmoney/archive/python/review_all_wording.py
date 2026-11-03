# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_section(title, start_line, end_line):
    print(f"\n==================== {title} (L{start_line} - L{end_line}) ====================")
    for idx in range(start_line - 1, min(end_line, len(lines))):
        line = lines[idx]
        # Look for user visible strings in HTML / template literals
        # strip indent for readable output
        print(f"{idx+1}: {line}", end='')

# Let's inspect renderDashboard: 1523 to 1700
print_section("renderDashboard", 1523, 1700)

# renderBanksTab: 1700 to 1750, renderBanksAndCards: 1750 to 1830
print_section("renderBanksTab & renderCardsTab", 1700, 1830)

# renderCards: 1830 to 1910
print_section("Cards rendering & big expenses", 1830, 1910)

# renderInstallments: 1910 to 1980
print_section("renderInstallments", 1910, 1980)

# renderBills: 1980 to 2070
print_section("renderBills", 1980, 2070)

# renderStocks: 2070 to 2180
print_section("renderStocks", 2070, 2180)
