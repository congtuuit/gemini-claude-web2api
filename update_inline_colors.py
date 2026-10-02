import re

with open('panel.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Separate the style block so we don't accidentally mess up the CSS we just perfected
style_pattern = re.compile(r'(<style>.*?</style>)', re.DOTALL)
match = style_pattern.search(content)
style_block = match.group(1) if match else ""
rest_of_content = content.replace(style_block, "[[STYLE_BLOCK]]")

# Now apply color replacements to the rest of the HTML and JS
replacements = {
    # Inline styles - Map legacy hacking colors to modern slate/blue/emerald
    "color:#0f0": "color:#38bdf8",            # Sky blue for text highlights
    "color:#0a0": "color:#cbd5e1",            # Light slate for secondary text
    "color:#080": "color:#94a3b8",            # Slate
    "color:#060": "color:#64748b",            # Darker slate
    "color:#040": "color:#475569",            # Muted slate
    "background:#000": "background:#0f172a",  # Deep slate background
    "border:1px solid #0a0": "border:1px solid #334155",
    "background:rgba(0,255,0,0.03)": "background:rgba(56,189,248,0.05)",
    
    # Warning box
    "background:#330": "background:#451a03",
    "color:#fa0": "color:#f59e0b",
    "border:1px solid #fa0": "border:1px solid #92400e",

    # JavaScript dynamic colors
    "'#f00':'#0f0'": "'#ef4444':'#10b981'",   # Toast borders (Red vs Emerald)
    "'#060'": "'#64748b'",                    # JS offline/unknown text
    "'#0f0'": "'#10b981'",                    # JS Success / Alive (Emerald)
    "'#f00'": "'#ef4444'",                    # JS Error / Dead (Red)
    "'#fa0'": "'#f59e0b'",                    # JS Warning (Amber)
    "'#500'": "'#475569'",                    # JS OFF state (Slate)
}

for old_val, new_val in replacements.items():
    rest_of_content = rest_of_content.replace(old_val, new_val)

# Reassemble
final_content = rest_of_content.replace("[[STYLE_BLOCK]]", style_block)

with open('panel.py', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Inline HTML & JS colors updated successfully.")
