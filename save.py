import os

from toolkit import Event


def main():
    print("Generating ics file as output/comicw.ics")
    path = "docs"
    if not os.path.exists(path):
        os.mkdir(path)

    with open(os.path.join(path, "comicw.ics"), "wb") as f:
        f.write(Event.to_ical().serialize().encode("utf-8"))

    print("Success")


if __name__ == "__main__":
    main()
