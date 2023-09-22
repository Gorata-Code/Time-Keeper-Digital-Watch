from time_watch.watch import Watch

"""
Our App Entry Point
"""


def time_piece() -> None:

    watch = Watch()
    watch.mainloop()


if __name__ == '__main__':
    time_piece()
