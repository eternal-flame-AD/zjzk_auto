def show_menu():
    print("===Main menu===\n" 
    "1-STOP\n"
    "2-SOFT CHANGE CHALLENGE\n"
    "3-CONTINUE\n")
    op=0
    while (op<1) or (op>3):
        op=int(input("INPUT CHOICE:"))
    return op