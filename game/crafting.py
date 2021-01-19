def getCraftingItem(objects, tableType=False):
    item = ["wood", 0]

    if tableType:  # 3x3
        pass
    else:  # 2x2
        if ["wood"] * 4 == objects:
            print("hah")

        if ["log_oak", "", "", ""] == objects:
            print("log")

    return item
