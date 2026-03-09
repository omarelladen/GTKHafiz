import gettext
gettext.install("gtkhafiz")

from .app import App


def main(prefix):
    try:
        app = App(prefix)
        app.parse_args()
        if app.setup():
            app.run()

    except Exception as e:
        print(_("Error starting application: {e}").format(e=e))


if __name__ == "__main__":
    main()
