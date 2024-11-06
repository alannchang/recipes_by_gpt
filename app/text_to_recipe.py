def text_to_recipe_dict(text, query):
    # Initialize dictionary structure
    recipe = {
        "title": query.title(),
        "contents": {"ingredients": [], "instructions": [], "tips": []},
    }

    # Split text into lines and process
    lines = text.strip().split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract title
        if line.startswith("title:"):
            recipe["title"] = line.replace("title:", "").strip().title()
        # Identify sections
        elif line == "contents:":
            continue
        elif line == "ingredients:":
            current_section = "ingredients"
        elif line == "instructions:":
            current_section = "instructions"
        elif line == "tips:":
            current_section = "tips"
        # Add content to appropriate section
        elif line.startswith("-") and current_section:
            recipe["contents"][current_section].append(line.replace("-", "", 1).strip())
        elif line.startswith(tuple("0123456789")) and current_section:
            # Remove number prefix from instructions
            recipe["contents"][current_section].append(
                line.split(".", 1)[1].strip() if "." in line else line
            )
        elif current_section and line:
            recipe["contents"][current_section].append(line)

    return recipe
