def show_menu():
    print("\n===Main menu===\n" 
    "1-STOP\n"
    "2-SOFT CHANGE CHALLENGE\n"
    "3-CONTINUE\n"
    "4-SAVE SCREENSHOT\n"
    "5-CHANGE MAX FULL LEVEL THRES\n"
    )
    op=0
    while not (op in range(1,6)):
        op=int(input("INPUT CHOICE:"))
    return op