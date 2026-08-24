"""
Regenerates the bio/contact rows inside dark.svg and light.svg from the
data table below. Run this locally whenever you want to update your
profile text without hand-editing the SVGs.

NOTE: The Role/Title row was intentionally removed from this profile and
is NOT included in this table. If you ever want to re-add a role line,
you'll need to re-insert a <text> row at y="178" in both SVGs first.

Usage:
    python3 update_profile_content.py
"""
import os
import xml.etree.ElementTree as ET

def strip_ns(tag):
    return tag.split('}')[-1] if '}' in tag else tag

def update_svg_profile(file_path):
    print(f"--- Updating {file_path} ---")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    tree = ET.parse(file_path)
    root = tree.getroot()

    if 'aria-label' in root.attrib:
        root.attrib['aria-label'] = "Aryan Nannaware — profile.sh --live"

    # y-coordinate -> (row label, value text, font-size)
    table_data = {
        '198': ('Origin', 'PUNE', 14.0),
        '218': ('Education', 'B.Tech Computer Science Engineering, AISSMS Information Technology', 14.0),
        '238': ('Status', 'Building AI Products, Mastering Full Stack Development', 14.0),
        '278': ('Company', 'the one which choose me', 14.0),
        '300': ('ToolChain', 'React, Node.js, Express, MongoDB, Python, Java, JavaScript', 7.6),
        '340': ('Core.Lang', 'Python, Java, JavaScript, C++, C', 14.0),
        '360': ('Core.Frontend', 'React, Next.js, HTML, CSS, Bootstrap, Tailwind', 14.0),
        '380': ('Core.Backend', 'Node.js, Express', 14.0),
        '400': ('Core.Database', 'MongoDB, MySQL, PostgreSQL', 14.0),
        '420': ('Core.Infra', 'Git, GitHub, Docker, Vercel', 14.0),
        '466': ('Grid.Mail', 'mailto:aryan2nannaware@gmail.com', 14.0),
        '508': ('Grid.LinkedIn', 'https://www.linkedin.com/in/aryan-nannaware-6243b9318/', 14.0),
        '529': ('Grid.GitHub', 'https://github.com/aryan17129', 14.0),
        '550': ('Grid.Instagram', 'https://www.instagram.com/not.aryan.n.01/', 14.0),
    }
    subject_y = '158'
    subject_value = 'Aryan Nannaware'

    for elem in root.iter():
        tag = strip_ns(elem.tag)
        if tag == 'text':
            y = elem.attrib.get('y')
            if y in ('29', '29.0'):
                elem.text = "aryan2nannaware@gmail.com - % ./profile.sh --live"
                print(f"Updated top title bar (y={y})")
            elif y == '136':
                elem.text = "aryan2nannaware@gmail.com"
                print(f"Updated header mail (y={y})")
            elif y == subject_y:
                tspans = [child for child in elem if strip_ns(child.tag) == 'tspan']
                if len(tspans) >= 3:
                    tspans[2].text = f" {subject_value}"
                    print(f"Updated Subject row (y={y}) -> {subject_value}")
            elif y in table_data:
                key_label, val_text, fsize = table_data[y]
                tspans = [child for child in elem if strip_ns(child.tag) == 'tspan']
                if len(tspans) >= 3:
                    key_str = f"{key_label} " if key_label else ""
                    val_str = f" {val_text}"

                    if fsize == 14.0:
                        needed_dots = 79 - len(key_str) - len(val_str)
                        if needed_dots < 1:
                            needed_dots = 1
                    else:
                        needed_dots = 2

                    dots_str = "." * needed_dots

                    if key_label:
                        tspans[0].text = key_str
                    tspans[1].text = dots_str
                    tspans[2].text = val_str

                    if fsize != 14.0:
                        elem.attrib['font-size'] = str(fsize)
                    elif 'font-size' in elem.attrib:
                        elem.attrib['font-size'] = "14"

                    print(f"Updated row y={y:<4} -> {key_str}{dots_str}{val_str} (font-size={fsize})")
                else:
                    print(f"Warning: y={y} has fewer than 3 tspans ({len(tspans)})")

    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    tree.write(file_path, encoding='utf-8', xml_declaration=False)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'ns0:' in content or 'xmlns:ns0=' in content:
        content = content.replace('ns0:', '').replace('xmlns:ns0=', 'xmlns=')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Successfully finalized {file_path}!\n")

if __name__ == '__main__':
    update_svg_profile('dark.svg')
    update_svg_profile('light.svg')
