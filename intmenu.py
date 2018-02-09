def show_menu():
    print("\n===Main menu===\n" 
    "1-STOP\n"
    "2-SOFT CHANGE CHALLENGE\n"
    "3-CONTINUE\n"
    "4-SAVE SCREENSHOT\n")
    op=0
    while not (op in range(1,5)):
        op=int(input("INPUT CHOICE:"))
    return op