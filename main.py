import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gio,Gdk

import sqlite3
dbfile = 'db.sqlite3'


class Book:
    def __init__(self,
        name_arabic :str = '',
        name_latin  :str = '',
        # author      :str = '',
        n_chapters  :int = 0,
        n_verses    :int = 0,
        n_words     :int = 0,
        n_letters   :int = 0
    ):
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        # self.author = author
        self.n_chapters = n_chapters
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters



class Chapter:
    def __init__(self,
        number      :int = 0,
        name_arabic :str = '',
        name_latin  :str = '',
        n_verses    :str = 0,
        n_words     :int = 0,
        n_letters   :int = 0
    ):
        self.number = number
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters



class User:
    def __init__(self,
        username         :str = '',
        full_name        :str = '',
        country          :str = '',
        n_mem_chapters   :int = 0,
        n_mem_words      :int = 0,
        n_mem_verses     :int = 0,
        n_mem_letters    :int = 0,
        # pct_mem_chapters :int = 0,
        # pct_mem_words    :int = 0,
        # pct_mem_verses   :int = 0,
        # pct_mem_letters  :int = 0,
        mem_chapters     :list = [],
        mem_words        :list = [],
        mem_verses       :list = [],
        # mem_letters      :list = []
    ):
        self.username = username
        self.full_name = full_name
        self.country = country
        self.mem_chapters = mem_chapters
        self.n_mem_chapters = n_mem_chapters
        self.n_mem_words = n_mem_words
        self.n_mem_verses = n_mem_verses
        self.n_mem_letters = n_mem_letters
        # self.pct_mem_chapters = pct_mem_chapters
        # self.pct_mem_words = pct_mem_words
        # self.pct_mem_verses = n_mem_verses
        # self.pct_mem_letters= n_mem_letters
        # self.mem_words = mem_words
        # self.mem_verses = mem_verses
        # self.mem_letters = mem_letters
        # self.mem_letters = mem_letters

    def calc_pct_mem_chapters(self) -> float:
        return round(self.n_mem_chapters / book.n_chapters * 100, 1)
    def calc_pct_mem_words(self) -> float:
        return round(self.n_mem_words / book.n_words * 100, 1)
    def calc_pct_mem_verses(self) -> float:
        return round(self.n_mem_verses / book.n_verses * 100, 1)
    def calc_pct_mem_letters(self) -> float:
        return round(self.n_mem_letters / book.n_letters * 100, 1)



class GTKHafizWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        ## Window
        self.win_default_l = 300
        self.win_default_h = 440
        self.set_border_width(6)
        self.set_default_size(self.win_default_l, self.win_default_h)

        # print(self.get_size())


        # self.drawing_area = Gtk.DrawingArea()
        # self.drawing_area.connect("draw", self.on_draw)
        # self.add(self.drawing_area)

        # # Example data for rectangles: (x, y, width, height, r, g, b)
        # self.rectangles = [
        #     (50, 50, 50, 50, 1.0, 0.0, 0.0),   # Red rectangle
        #     (110, 50, 50, 50, 0.0, 1.0, 0.0),  # Green rectangle
        #     (50, 110, 50, 50, 0.0, 0.0, 1.0),  # Blue rectangle
        #     (110, 110, 50, 50, 1.0, 1.0, 0.0), # Yellow rectangle
        # ]


        ## Vertical Box
        outerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(outerbox)

        # Menu Popover
        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bt_preferences = Gtk.ModelButton(label="Preferences")
        vbox.pack_start(bt_preferences, False, True, 10)
        bt_about = Gtk.ModelButton(label="About GTK Hafiz")
        bt_about.connect("clicked", self.on_about_clicked)
        vbox.pack_start(bt_about, False, True, 10)
        vbox.show_all()
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        

        ## Header Bar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "GTK Hafiz"
        self.set_titlebar(headerbar)

        # Menu Button
        bt_menu = Gtk.MenuButton(popover=self.popover)
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        bt_menu.add(image)
        headerbar.pack_end(bt_menu)

        # Profile Button
        # bt_profile = Gtk.Button()
        # bt_profile.connect("clicked", self.on_profile_clicked)
        # icon = Gio.ThemedIcon(name="user-info-symbolic")
        # image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        # bt_profile.add(image)
        # headerbar.pack_end(bt_profile)


        ## Stack
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)


        # Matrix Tab
        # label_matrix = Gtk.Label(label="Matrix!")
        # stack.add_titled(label_matrix, "matrix", "Matrix")
        
        
        ## Matrix Tab with DrawingArea
        # self.rects_per_col  = 19
        # self.rects_per_line = 6
        # drawing_area = Gtk.DrawingArea()
        # drawing_area.connect("draw", self.on_draw_matrix)
        # self.refresh_rectangles()
        # stack.add_titled(drawing_area, "matrix", "Matrix")

        self.rects_per_col  = 19
        self.rects_per_line = 6
        self.rectangles = []
        drawing_area = Gtk.DrawingArea()
        drawing_area.connect("draw", self.on_draw_matrix)
        drawing_area.connect("button-press-event", self.on_click_matrix)  # Conectando o evento de clique
        drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.refresh_rectangles()
        stack.add_titled(drawing_area, "matrix", "Matrix")



        # List Tab
        checkbutton_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # label = Gtk.Label(label="Memorized Chapters:")
        # checkbutton_container.pack_start(label, False, False, 0)
        self.checkboxes = []
        for c in list_obj_chapter:
            checkbutton = Gtk.CheckButton(label=f"{c.number}. ({c.name_latin}) {c.name_arabic}")
            if c.number in user.mem_chapters:
                checkbutton.set_active(True)
            self.checkboxes.append((checkbutton, c))
            checkbutton.connect("toggled", lambda btn, obj=c: self.on_checkbox_toggled(btn, obj))
            checkbutton_container.pack_start(checkbutton, False, False, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(checkbutton_container)
        stack.add_titled(scrolled_window, "list", "List")


        # Stats Tab
        self.label_stats = Gtk.Label()
        self.refresh_stats_label()
        stack.add_titled(self.label_stats, "stats", "Stats")


        # Profile Tab
        label_profile = Gtk.Label()
        label_profile.set_markup(
            f"<b>Name:</b> {user.full_name}\n"
            f"<b>Username:</b> {user.username}\n"
            f"<b>Country:</b> {user.country}\n\n"

            '<a href="https://github.com/omarelladen" '
            'title="Visit website">GitHub</a>'
        )
        stack.add_titled(label_profile, "profile", "Profile")


        ## Stack Switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)  # horizontal
        # stack_switcher.set_valign(Gtk.Align.CENTER)  # vertical (optional)

        outerbox.pack_start(stack_switcher, False, True, 0)
        outerbox.pack_start(stack, True, True, 0)
   



    def on_click_matrix(self, widget, event):
        if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS: # Gdk.EventType._2BUTTON_PRESS
            print("double")
        elif event.type == Gdk.EventType.BUTTON_PRESS:  # Clique simples
            if event.button == Gdk.BUTTON_PRIMARY:
                # Verifica se o clique está dentro de algum retângulo
                x, y = event.x, event.y
                # print(x, y)
                for idx, (rx, ry, width, height, r, g, b) in enumerate(self.rectangles):
                    if rx <= x <= rx + width and ry <= y <= ry + height:
                        # Alterar cor do retângulo clicado
                        self.toggle_rectangle(idx)
                        break
    def toggle_rectangle(self, idx):
        x, y, width, height, r, g, b = self.rectangles[idx]
        
        # Toggle colors
        if (r, g, b) == (0.5, 0.5, 0.5):
            self.rectangles[idx] = (x, y, width, height, 0.0, 0.8, 0.0)
        else:
            self.rectangles[idx] = (x, y, width, height, 0.5, 0.5, 0.5)
        self.queue_draw()  # Redraw

    def on_draw_matrix(self, widget, cr):
        for x, y, width, height, r, g, b in self.rectangles:
            cr.set_source_rgb(r, g, b)
            cr.rectangle(x, y, width, height)
            cr.fill()

    def on_about_clicked(self, widget):
        print("About")

    def refresh_rectangles(self):
        # Update rectangle colors based on mem_chapters
        self.rectangles = []
        for i in range(self.rects_per_col):
            for j in range(self.rects_per_line):
                x = 127 + j * 40
                y = 15 + i * 20
                chapter_num = i * (self.rects_per_line) + j + 1
                r, g, b = (0.0, 0.8, 0.0) if chapter_num in user.mem_chapters else (0.5, 0.5, 0.5)
                self.rectangles.append((x, y, 30, 10, r, g, b))
        
        self.queue_draw() # Redraw the matrix tab

    def on_checkbox_toggled(self, button, c=''):
        if button.get_active():
            user.mem_chapters.append(c.number)
            user.n_mem_chapters += 1
            user.n_mem_verses   += c.n_verses
            user.n_mem_words    += c.n_words
            user.n_mem_letters  += c.n_letters
            self.save_mem_chapters(c, 'add')
        else:
            user.mem_chapters.remove(c.number)
            user.n_mem_chapters -= 1
            user.n_mem_verses   -= c.n_verses
            user.n_mem_words    -= c.n_words
            user.n_mem_letters  -= c.n_letters
            self.save_mem_chapters(c, 'rm')
        self.refresh_stats_label()
        self.refresh_rectangles()

    def refresh_stats_label(self):
        self.label_stats.set_markup(
            f"<big><b>Chapters:</b> {user.n_mem_chapters} ({user.calc_pct_mem_chapters()}%)</big>\n"
            f"<big><b>Verses:</b> {user.n_mem_verses} ({user.calc_pct_mem_verses()}%)</big>\n"
            f"<big><b>Words:</b> {user.n_mem_words} ({user.calc_pct_mem_words()}%)</big>\n"
            f"<big><b>Letters:</b> {user.n_mem_letters} ({user.calc_pct_mem_letters()}%)</big>"
        )
    
    def save_mem_chapters(self, c, op):
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        cur.execute("""
            UPDATE users
            SET n_mem_chapters = ?, n_mem_verses = ?, n_mem_words = ?, n_mem_letters = ?
            WHERE username = ?
        """, (user.n_mem_chapters, user.n_mem_verses, user.n_mem_words, user.n_mem_letters, user.username))

        if op == 'add':
            cur.execute("""
                INSERT INTO mem_chapters
                (users_username, chapters_number) VALUES (?, ?)
            """, (user.username, c.number))
        elif op == 'rm':
            cur.execute("""
                DELETE FROM mem_chapters
                WHERE users_username = ? AND
                      chapters_number = ?
            """, (user.username, c.number))

        con.commit()
        con.close()



if __name__ == '__main__':
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    # Load persistance data from db
    table_book = [a for a in cur.execute("SELECT * FROM books")]
    list_obj_book=[]
    for b in table_book:
        list_obj_book.append(Book(b[1], b[2], b[3], b[4], b[5], b[6]))
    book = list_obj_book[0]

    table_chapter = [a for a in cur.execute("SELECT * FROM chapters")]
    list_obj_chapter=[]
    for c in table_chapter:
        list_obj_chapter.append(Chapter(c[0], c[1], c[2], c[3], c[4], c[5]))

    table_user = [a for a in cur.execute("SELECT * FROM users")]
    if len(table_user) > 0:
        list_obj_user =[]
        for u in table_user:
            list_obj_user.append(User(u[0], u[1], u[2], u[3], u[4], u[5], u[6]))
        user = list_obj_user[0]

        table_user_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
        for t in table_user_mem_chapters:
            user.mem_chapters.append(t[1])
    else:
        username  = input("Username: ")
        full_name = input("Full Name: ")
        country   = input("Country: ")
        user = User(username, full_name, country)

        cur.execute("""
            INSERT INTO users
            (username, full_name, country, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user.username, user.full_name, user.country, user.n_mem_chapters, user.n_mem_words, user.n_mem_verses, user.n_mem_letters))
    
    con.commit()
    con.close()


    # Load GTK Window
    win = GTKHafizWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
