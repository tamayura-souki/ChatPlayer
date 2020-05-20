import sys
from draw import PygameStrRender, PygameWindow, get_quit_event

if __name__ == "__main__":
    pg_window = PygameWindow()

    @pg_window.main
    def main():
        if get_quit_event():
            pg_window.quit()
            sys.exit(0)

    PygameStrRender.set_font("yugothicregularyugothicuisemilight", 100)
    PygameStrRender.set_screen(pg_window.screen)
    render = PygameStrRender()
    pg_window.add_render(render)

    while True:
        main()