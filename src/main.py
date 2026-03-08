from .app import App


def main(prefix):
    try:
        app = App(prefix)
        app.parse_args()
        if app.setup():
            app.run()

    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()
