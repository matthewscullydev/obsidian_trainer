import re
import os
import time
# Define functions


# Example usage:
file_path = '/home/matt/Documents/obsidian_bubble_vault/bubble_trainer/your_file.md'
directory_path = '/home/matt/Documents/obsidian_bubble_vault/bubble_trainer/'


def remove_markdown_files():
    try:
        os.system(f'rm {directory_path}*.md')
        print("Markdown files removed successfully.")
    except Exception as e:
        print(f"Error: {e}")

def train_mode():
    global file_path
    def parse_markdown(file_path):
        # Define a dictionary to store replaced text
        references = {}

        # Read the Markdown file using an absolute path
        with open(file_path, 'r') as file:
            markdown_content = file.read()

        # Define the regex pattern to find text between double brackets
        pattern = r'\[\[(.*?)\]\]'

        # Use regex to replace text surrounded by double brackets with increasing question marks
        def replace_text(match):
            text_to_replace = match.group(1)
            references[len(references)] = text_to_replace
            question_marks = '?' * (len(references))  # Append two extra question marks for each replacement
            return f'[[{question_marks}]]'

        replaced_content = re.sub(pattern, replace_text, markdown_content)

        # Write the modified content back to the original file
        with open(file_path, 'w') as file:
            file.write(replaced_content)

        # Check other markdown files in the parent directory
        parent_directory_path = os.path.dirname(file_path)

        for filename in os.listdir(parent_directory_path):
            if filename.endswith('.md') and filename != os.path.basename(file_path):
                original_filename = os.path.splitext(filename)[0]

                # Check if the file name is a reference
                if original_filename in references.values():
                    position = list(references.values()).index(original_filename)
                    associated_string = '?' * (position + 1)
                    new_file_path = os.path.join(parent_directory_path, associated_string + '.md')
                    print(new_file_path)
                    os.rename(os.path.join(parent_directory_path, filename), new_file_path)

        start_time = time.time()

        # Prompt the user to resolve references
        skipped_indices = []

        for index in range(len(references)):
            user_input = input(f"\nWhat is the subject for {'?' * (index + 1)}\n ").lower()

            # Check if user input is correct
            if user_input == references[index].lower():
                print("\nCorrect!")

                # Write back the correct value to the Markdown file

                replaced_content = replaced_content.replace(f'[[{"?" * (index + 1)}]]', f'[[{references[index]}]]', 1)
                with open(file_path, 'w') as file:
                    file.write(replaced_content)

                # Rename the file back to the correct value
                restored_filename = os.path.join(parent_directory_path, references[index] + '.md')
#
                position = list(references.values()).index(user_input.lower())
                associated_string = '?' * (position + 1)
                new_file_path = os.path.join(parent_directory_path, associated_string + '.md')

#
                os.rename(new_file_path, restored_filename)

                question_marks = '?' * (index + 2)
                filename_without_extension, extension = os.path.splitext(restored_filename)
                new_path = os.path.dirname(filename_without_extension) + '/'
                new_file_path = f'{new_path}{references[index]}.md'

            else:
                skipped_indices.append(index)
                while True:
                    retry_input = input("\nIncorrect! Try again? (Y/N):").lower()
                    if retry_input == 'y':
                        user_input = input(f"\nWhat is the subject for {'?' * (index + 1)}\n ").lower()
                        if user_input == references[index].lower():
                            print("\nCorrect!")

                            # Write back the correct value to the Markdown file
                            replaced_content = replaced_content.replace(f'[[{"?" * (index + 1)}]]', f'[[{references[index]}]]', 1)
                            with open(file_path, 'w') as file:
                                file.write(replaced_content)

                            # Rename the file back to the correct value
                            restored_filename = os.path.join(parent_directory_path, references[index] + '.md')
#
                            position = list(references.values()).index(user_input.lower())
                            associated_string = '?' * (position + 1)
                            new_file_path = os.path.join(parent_directory_path, associated_string + '.md')

#
                            os.rename(new_file_path, restored_filename)

                            question_marks = '?' * (index + 2)
                            filename_without_extension, extension = os.path.splitext(restored_filename)
                            new_path = os.path.dirname(filename_without_extension) + '/'
                            new_file_path = f'{new_path}{references[index]}.md'

                             # Remove the index from skipped_indices since the user got it correct after retrying
                            if index in skipped_indices:
                                skipped_indices.remove(index)

                            break
                    elif retry_input == 'n':
                        print("\nMoving to the next index.")

                        restored_filename = os.path.join(parent_directory_path, references[index] + '.md')

                        question_marks = '?' * (index + 2)
                        filename_without_extension, extension = os.path.splitext(restored_filename)
                        new_path = os.path.dirname(filename_without_extension) + '/'
                        new_file_path = f'{new_path}{question_marks}.md'

                        break
                    else:
                        print("Invalid input. Please enter Y or N.")

            # Process skipped indices
        for skipped_index in skipped_indices:
            # Write back the correct value to the Markdown file for skipped indices
            replaced_content = replaced_content.replace(f'[[{"?" * (skipped_index + 1)}]]', f'[[{references[skipped_index]}]]', 1)

            # Rename the file back to the correct value for skipped indices
            restored_filename = os.path.join(parent_directory_path, references[skipped_index] + '.md')
            new_file_path = os.path.join(parent_directory_path, '?' * (skipped_index + 1) + '.md')
            os.rename(new_file_path, restored_filename)

        # Write back the correct values for skipped indices to the Markdown file
        with open(file_path, 'w') as file:
            file.write(replaced_content)

        end_time = time.time()
        elapsed_time = end_time - start_time
        retention_rate = (len(references) - len(skipped_indices)) / len(references) if len(references) != 0 else 0

        print(f"\nTime taken to finish: {elapsed_time:.2f} seconds")
        print(f"Retention rate: {retention_rate * 100:.2f}% (Correct: {len(references) - len(skipped_indices)}/{len(references)})")


    parse_markdown(file_path)

def free_mode():
    global file_path

    def parse_markdown(file_path):
        # Define a dictionary to store replaced text
        references = {}

        # Read the Markdown file using an absolute path
        with open(file_path, 'r') as file:
            markdown_content = file.read()

        # Define the regex pattern to find text between double brackets
        pattern = r'\[\[(.*?)\]\]'

        # Use regex to replace text surrounded by double brackets with increasing question marks
        def replace_text(match):
            text_to_replace = match.group(1)
            references[len(references)] = text_to_replace
            question_marks = '?' * (len(references))  # Append two extra question marks for each replacement
            return f'[[{question_marks}]]'

        replaced_content = re.sub(pattern, replace_text, markdown_content)

        # Write the modified content back to the original file
        with open(file_path, 'w') as file:
            file.write(replaced_content)

        # Check other markdown files in the parent directory
        parent_directory_path = os.path.dirname(file_path)

        for filename in os.listdir(parent_directory_path):
            if filename.endswith('.md') and filename != os.path.basename(file_path):
                original_filename = os.path.splitext(filename)[0]

                # Check if the file name is a reference
                if original_filename in references.values():
                    position = list(references.values()).index(original_filename)
                    associated_string = '?' * (position + 1)
                    new_file_path = os.path.join(parent_directory_path, associated_string + '.md')
                    os.rename(os.path.join(parent_directory_path, filename), new_file_path)

        start_time = time.time()

        # Prompt the user to resolve references
        skipped_indices = []

        while True:
            user_input = input(f"\nEnter a node (or 'q' to exit): ").lower()

            # Check if user wants to exit
            if user_input == 'q':
                break

            # Check if user input is correct
            if user_input in references.values():
                print("\nCorrect!")

                # Find the index of the reference
                index = list(references.values()).index(user_input)

                # Write back the correct value to the Markdown file
                replaced_content = replaced_content.replace(f'[[{"?" * (index + 1)}]]', f'[[{user_input}]]', 1)
                with open(file_path, 'w') as file:
                    file.write(replaced_content)

                # Rename the file back to the correct value
                restored_filename = os.path.join(parent_directory_path, user_input + '.md')
                position = list(references.values()).index(user_input)
                associated_string = '?' * (position + 1)
                new_file_path = os.path.join(parent_directory_path, associated_string + '.md')
                os.rename(new_file_path, restored_filename)

                question_marks = '?' * (index + 2)
                filename_without_extension, extension = os.path.splitext(restored_filename)
                new_path = os.path.dirname(filename_without_extension) + '/'
                new_file_path = f'{new_path}{user_input}.md'

            else:
                print("Incorrect! Try again.")
                skipped_indices.append(index)

        # Provide statistics even if the user exits with 'q'
        end_time = time.time()
        elapsed_time = end_time - start_time
        retention_rate = (len(references) - len(skipped_indices)) / len(references) if len(references) != 0 else 0

        print(f"\nTime taken to finish: {elapsed_time:.2f} seconds")
        print(f"Retention rate: {retention_rate * 100:.2f}% (Correct: {len(references) - len(skipped_indices)}/{len(references)})")

    parse_markdown(file_path)

# Call the function
#free_mode()


def select_markdown_file():
    global file_path  # Use the global file_path variable
    new_filename = input("Enter the new filename (without extension): ")
    # Extract the directory path from the global file_path
    directory_path = os.path.dirname(file_path)
    # Modify the file path with the new filename
    file_path = os.path.join(directory_path, f'{new_filename}.md')

# accessory functions for generate_markdown_files

def create_markdown_file(filename):
    with open(filename, 'w') as file:
        file.write('---\n')

def append_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(f'[[{content}]]\n')

#def remove_markdown_files(filenames):
#    for filename in filenames:
#        try:
#            os.remove(filename)
#        except FileNotFoundError:
#            pass
#


def generate_markdown_files():
    global directory_path
    print(directory_path)
    try:
        root_node = input("Enter Root Node: ")
        root_filename = f'{root_node}.md'
        create_markdown_file(root_filename)

        first_level_dependencies = input("Enter First Level Dependencies (separate with commas): ").split(',')
        for dependency in first_level_dependencies:
            dep_filename = f'{dependency.strip()}.md'
            create_markdown_file(dep_filename)
            append_to_file(root_filename, dependency.strip())

        # Prompt to continue with first level dependencies
        continue_first_level = input("Do you want to continue with first level dependencies? (Y/N): ").lower()
        if continue_first_level != 'y':
            print("Exiting.")
            return

        try:
            second_level_dependencies = []
            for node in first_level_dependencies:
                node_filename = f'{node.strip()}.md'
                create_markdown_file(node_filename)

                second_level_nodes = input(f"Enter Dependencies for {node.strip()} (separate with commas): ").split(',')
                for second_node in second_level_nodes:
                    second_node_filename = f'{second_node.strip()}.md'
                    create_markdown_file(second_node_filename)
                    append_to_file(node_filename, second_node.strip())
                    second_level_dependencies.append(second_node.strip())

            continue_second_level = input("Do you want to continue with second level dependencies? (Y/N): ").lower()
            while continue_second_level == 'y':
                new_second_level_dependencies = []
                for node in second_level_dependencies:
                    add_node = input(f"Do you want to add nodes for {node.strip()}? (Y/N): ").lower()
                    if add_node == 'y':
                        node_filename = f'{node.strip()}.md'
                        new_second_nodes = input(f"Enter Dependencies for {node.strip()} (separate with commas): ").split(',')
                        for new_second_node in new_second_nodes:
                            new_second_node_filename = f'{new_second_node.strip()}.md'
                            create_markdown_file(new_second_node_filename)
                            append_to_file(node_filename, new_second_node.strip())
                            new_second_level_dependencies.append(new_second_node.strip())

                second_level_dependencies = new_second_level_dependencies
                continue_second_level = input("Do you want to continue with second level dependencies? (Y/N): ").lower()

        except KeyboardInterrupt:
            print("\nTerminated by user. Cleaning up and exiting.")
            return

    except KeyboardInterrupt:
        print("\nTerminated by user. Cleaning up and exiting.")
        return

    print("Exiting.")
#generate_markdown_files()

def show_statistics():
    print("Showing statistics")
    # Add your statistics display logic here

def exit_program():
    print("Exiting program")
    # Add any cleanup logic here if needed
    exit()

# Define a dictionary mapping choices to functions
menu_options = {
    "1": train_mode,
    "2": free_mode,
    "3": select_markdown_file,
    "4": generate_markdown_files,
    "5": show_statistics,
    "6": remove_markdown_files,
    "7": exit_program,
}

while True:
    print("\nMenu:")
    for key, value in menu_options.items():
        print(f"{key}. {value.__name__.replace('_', ' ').title()}")  # Format function names

    choice = input("\nEnter your choice (1-7): ")

    # Use the dictionary to call the corresponding function
    menu_options.get(choice, lambda: print("Invalid choice"))()
