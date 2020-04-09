import blessed
from time import sleep

def counter(i):

    print(i)

if __name__ == "__main__":
    term = blessed.Terminal()
    print(term.height)
    print(term.width)
    with term.fullscreen():
        with term.location(0, term.height - 1):
            test = ["apples", "bananas", "pears"]
            for x in test:
                counter(x)
                sleep(3)
                print(term.home + term.clear_eos)
        print('This is back where I came from.')
        sleep(5)


