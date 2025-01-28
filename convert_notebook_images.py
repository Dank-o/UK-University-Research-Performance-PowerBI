import json
import re
import sys


def convert_image_blocks_to_html(markdown_text):
    """
    Converts image blocks with captions in markdown to HTML with centring and margin adjustment.
    """
    # Pattern for image and caption matching
    pattern = r"!\[.*?\]\((.*?)\)\n\n_(.*?)_"

    def replacement(match):
        image_src, caption = match.groups()
        return (
            f'<div style="text-align: center; margin-right: 70px;">\n'
            f'    <img src="{image_src}" alt="{caption}" />\n'
            f'    <p style="text-align: center;"><em>{caption}</em></p>\n'
            f"</div>"
        )

    markdown_text = re.sub(pattern, replacement, markdown_text)

    # Replace "\[here\]" with a centred gif and caption
    pattern2 = r"\\\[here\\\]\n\n_(.*?)_"

    def replacement2(match):
        caption = match.groups()
        return (
            f'<div style="text-align: center; margin-right: 70px;">\n'
            f'    <img src="quick_demo.gif" alt="{caption[0]}" style="width: 20cm;\
                position: relative; display: inline-block; clip-path: inset(2px 0 0 0);">\n'
            f'    <p style="text-align: center;"><em>{caption[0]}</em></p>\n'
            f"</div>"
        )

    markdown_text = re.sub(pattern2, replacement2, markdown_text)

    # markdown_text = re.sub(
    #     r"\\\[here\\\]",
    #     (
    #         "<div style='text-align: center;'>\n"
    #         "    <img src='short_demo.gif' alt='short_demo' style='width: 15cm;'>\n"
    #         "    <p style='text-align: center;'><em>short_demo</em></p>\n"
    #         "</div>"
    #     ),
    #     markdown_text,
    # )

    return f'<div style="margin-right: 70px;">\n\n{markdown_text}\n</div>'


def style_lines(text):
    """
    Styles specific lines based on the provided rules.
    """
    lines = text.splitlines()
    output_lines = []
    glossary_found = False
    references_found = False

    for i, line in enumerate(lines):
        # Set the size of the first line to 25 pts
        if i == 0:
            output_lines.append(
                f'<p style="font-size: 25pt; text-align: center;">{line}</p>'
            )
        # Convert hyperlinks in lines 2 and 3 to HTML
        elif i in [1, 2]:
            line = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', line)
            if i == 2:
                output_lines.append(f'<div style="text-align: right;">{line}</div>')
            else:
                output_lines.append(line)
        # Style the 5th line: justify right and font size 8 pts
        elif i == 4:
            line = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', line)
            output_lines.append(
                f'<div style="text-align: right; font-size: 8pt;">{line}</div>'
            )
        # Indent lines after "Glossary" but before "References"
        elif "Glossary" in line:
            glossary_found = True
            output_lines.append(line)
        elif "References" in line:
            references_found = True
            output_lines.append(line)
        elif glossary_found and not references_found and line.strip():
            output_lines.append(
                f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{line}"
            )
        # Centre lines containing "Score =", remove backslashes
        elif "Score =" in line:
            cleaned_line = line.replace("\\", "")
            output_lines.append(
                f'<div style="text-align: center;">{cleaned_line}</div>'
            )
        else:
            output_lines.append(line)

    return "\n".join(output_lines)


def process_file(input_file, output_file):
    """
    Processes the input .txt or .ipynb file and applies the necessary transformations.
    """
    if input_file.endswith(".txt"):
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        styled_text = style_lines(text)
        styled_text = convert_image_blocks_to_html(
            styled_text
        )  # Ensure images are centred
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": styled_text.splitlines(),
                    "metadata": {},
                }
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        print(f"Converted .txt file saved as .ipynb: {output_file}")
    elif input_file.endswith(".ipynb"):
        with open(input_file, "r", encoding="utf-8") as f:
            notebook = json.load(f)
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "markdown":
                original_source = "".join(cell.get("source", ""))
                converted_source = convert_image_blocks_to_html(original_source)
                styled_source = style_lines(converted_source)
                cell["source"] = (
                    [styled_source]
                    if original_source != styled_source
                    else cell["source"]
                )
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        print(f"Converted notebook saved to: {output_file}")
    else:
        print("Unsupported file format. Use a .txt or .ipynb file.")


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py <input_file> <output_file>")
    #     sys.exit(1)

    input_file = 't.txt' #sys.argv[1]
    output_file = (
        'detailed_description.ipynb' # "t.ipynb"  #sys.argv[2]
    )
    process_file(input_file, output_file)
