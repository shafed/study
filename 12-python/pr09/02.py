def bread(func):
    def wrapper():
        print("</---------------\\>")
        func()
        print("   <\\_______/>")

    return wrapper


def cheese(func):
    def wrapper():
        print("      =сыр=")
        func()
        print("      =сыр=")

    return wrapper


def tomatoes(func):
    def wrapper():
        print("    #помидоры#")
        func()

    return wrapper


def salad(func):
    def wrapper():
        print("     ~салат~")
        func()

    return wrapper


@bread
@cheese
@tomatoes
@salad
def sandwich():
    print("   --котлета--")


sandwich()
