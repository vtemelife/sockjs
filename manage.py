import getopt
import logging
import os
import sys

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
if root not in sys.path:
    sys.path.append(root)


logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["runserver"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("manage.py runserver")
            sys.exit()
        elif opt in ("--runserver",):
            from core.sockjs.runners import SockJsRunner

            SockJsRunner().run()


if __name__ == "__main__":
    main(sys.argv[1:])
