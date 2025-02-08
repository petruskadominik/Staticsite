import re

def markdown_to_blocks(markdown):
    remaining_text = markdown
    blocks = remaining_text.splitlines()
    result = []
    temp = ""
    for block in blocks:
        if block == "" and temp != "":
            result.append(temp)
            temp = ""
        else:
            if temp:
                if block.strip().startswith("*"):
                    temp = temp + '\n' + block.rstrip()
                else:
                    temp = temp + '\n' + block.strip()
            else:
                 temp = block.strip()
    if temp != "":
        result.append(temp)
   
    return result

def block_to_block_type(block):
    if re.match(r"#{1,6} ",block):
        return "heading"
    elif re.match(r"^```.*\n[\s\S]*```$", block) and not re.match(r"^````", block):
        return "code"
    elif re.match(r"> ",block):
        lines = block.splitlines()
        for line in lines:
            if not line.startswith("> "):
                return "paragraph"
        return "quote"
    elif block.startswith("* ") or block.startswith("- "):
        lines = block.splitlines()
        for line in lines:
            if not (line.startswith("* ") or line.startswith("- ")):
                return "paragraph"
        return "unordered_list"
    elif re.match(r"^1. ",block):
        lines = block.splitlines()
        for i, line in enumerate(lines, start=1):
                if not line.startswith(f"{i}. "):
                    return "paragraph"
        return "ordered_list"
    else:
        return "paragraph"
    