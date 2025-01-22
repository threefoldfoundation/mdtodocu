#!/usr/bin/env python3

import os
import re
import shutil
import json
from pathlib import Path
import sys  # Import sys to handle command-line arguments

def parse_summary(summary_path):
    """
    Parse the SUMMARY.md file and extract the hierarchy based on indentation levels.
    Returns a list of tuples (indentation level, filename, title, position).
    """
    with open(summary_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    hierarchy = []
    for position, line in enumerate(lines, start=1):  # Start counting from 1
        # Match lines like "- [File 1](path/to/filename.md)"
        match = re.match(r'^(\s*)- \[(.*?)\]\((.*\.md)\)', line)
        if match:
            indentation = len(match.group(1))  # Number of spaces for indentation
            title = match.group(2).strip()  # Extract title
            filename = os.path.basename(match.group(3)).strip()  # Extract filename and remove extra spaces
            hierarchy.append((indentation, filename, title, position))

    return hierarchy

def find_source_file(filename, search_dir):
    """
    Recursively search for a file with the given filename in the search directory.
    Returns the full path to the file if found, otherwise None.
    """
    for root, _, files in os.walk(search_dir):
        for file in files:
            if file.lower() == filename.lower():  # Case-insensitive comparison
                return os.path.join(root, file)
    return None

def generate_frontmatter(title, position):
    """
    Generate the frontmatter block for a markdown file.
    """
    return f"""---
title: "{title}"
sidebar_position: {position}
---\n\n"""

def create_category_json(directory, label, position):
    """
    Create a _category_.json file in the specified directory.
    """
    category_data = {
        "label": label,
        "position": position
    }
    category_path = os.path.join(directory, "_category_.json")
    with open(category_path, 'w', encoding='utf-8') as file:
        json.dump(category_data, file, indent=2)
    print(f"Created: {category_path}")

def create_directory_structure(hierarchy, search_dir, output_dir):
    """
    Create the directory structure based on the hierarchy, copy files, add frontmatter,
    and create _category_.json files for directories.
    """
    current_level = 0
    current_path = output_dir

    # Track which files have children
    has_children = set()
    for i, (indentation, filename, title, position) in enumerate(hierarchy):
        level = indentation // 2
        if i + 1 < len(hierarchy):
            next_level = hierarchy[i + 1][0] // 2
            if next_level > level:
                has_children.add(filename)

    for indentation, filename, title, position in hierarchy:
        # Calculate the level based on indentation (assuming 2 spaces per level)
        level = indentation // 2

        # Adjust the current path based on the level
        if level > current_level:
            # Move deeper: create a directory named after the previous file (without .md)
            parent_filename = hierarchy[hierarchy.index((indentation, filename, title, position)) - 1][1]
            parent_dir_name = os.path.splitext(parent_filename)[0]
            current_path = os.path.join(current_path, parent_dir_name)
            os.makedirs(current_path, exist_ok=True)

            # Create _category_.json for the parent directory
            parent_title = hierarchy[hierarchy.index((indentation, filename, title, position)) - 1][2]
            parent_position = hierarchy[hierarchy.index((indentation, filename, title, position)) - 1][3]
            create_category_json(current_path, parent_title, parent_position)
        elif level < current_level:
            # Move up: adjust the current path accordingly
            for _ in range(current_level - level):
                current_path = os.path.dirname(current_path)

        current_level = level

        # Find the source file
        source_file = find_source_file(filename, search_dir)
        if not source_file:
            print(f"Warning: File '{filename}' not found in source directory. Skipping.")
            continue

        # Determine the destination path
        if filename in has_children:
            # If the file has children, create a directory named after it (without .md)
            dir_name = os.path.splitext(filename)[0]
            new_dir = os.path.join(current_path, dir_name)
            os.makedirs(new_dir, exist_ok=True)
            destination_path = os.path.join(new_dir, filename)

            # Create _category_.json for the new directory
            create_category_json(new_dir, title, position)
        else:
            # If the file has no children, place it directly in the current directory
            destination_path = os.path.join(current_path, filename)

        # Read the original file content
        with open(source_file, 'r', encoding='utf-8') as file:
            original_content = file.read()

        # Generate the frontmatter
        frontmatter = generate_frontmatter(title, position)

        # Write the updated content to the destination path
        with open(destination_path, 'w', encoding='utf-8') as file:
            file.write(frontmatter + original_content)

        print(f"Updated and copied: {source_file} -> {destination_path}")

def print_directory_tree(directory, prefix=""):
    """
    Print the directory tree structure.
    """
    contents = os.listdir(directory)
    for i, item in enumerate(contents):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            print(f"{prefix}├── {item}/")
            print_directory_tree(path, prefix + "│   ")
        else:
            print(f"{prefix}├── {item}")

def main():
    # Check if the user provided a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <userinput>")
        sys.exit(1)

    # Get the user input from the command-line argument
    userinput = sys.argv[1]

    # Define paths
    summary_path = f"../books/{userinput}/SUMMARY.md"
    search_dir = "."  # Search the current directory recursively
    output_dir = f"docu_books/{userinput}"  # Output directory includes user input

    # Parse the SUMMARY.md file
    hierarchy = parse_summary(summary_path)

    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Print initial directory tree
    print("Initial Directory Tree:")
    print_directory_tree(output_dir)

    # Create the directory structure, copy files, add frontmatter, and create _category_.json files
    create_directory_structure(hierarchy, search_dir, output_dir)

    # Print final directory tree
    print("\nFinal Directory Tree:")
    print_directory_tree(output_dir)

if __name__ == "__main__":
    main()