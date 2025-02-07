


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