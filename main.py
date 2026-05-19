import flet as ft
from engine import TransitSystem, LINES


BG = "#0D0F14"   # main background
SURFACE = "#161B24"   # slightly lighter background
CARD = "#1C2333"   # card background
BORDER = "#2A3450"   # border color
ACCENT = "#3B82F6"   # blue — main accent
GREEN = "#10B981"   # green — success / Zone A
AMBER = "#F59E0B"   # amber — warning / Zone B
RED = "#EF4444"   # red — danger / Zone C
PURPLE = "#8B5CF6"   # purple — Zone D
TEXT_PRI = "#F0F4FF"   # primary text
TEXT_SEC = "#8B9CC8"   # secondary text
TEXT_MUTED = "#4B5A7A"   # muted text

ZONE_COLORS = {
    "ZONE A - DOOR 1": GREEN,
    "ZONE B - DOOR 2": AMBER,
    "ZONE C - DOOR 3": RED,
    "ZONE D - DOOR 4": PURPLE,
}


def get_zone_color(zone):
    for key, color in ZONE_COLORS.items():
        if zone.startswith(key):
            return color
    return ACCENT


def txt(text, size=13, color=TEXT_PRI, weight=None, expand=False):
    return ft.Text(
        text, size=size, color=color, weight=weight, expand=expand, no_wrap=False
    )


def card(content, padding=16, expand=False, width=None):
    return ft.Container(
        content=content,
        bgcolor=CARD,
        border_radius=12,
        padding=padding,
        border=ft.Border.all(BORDER, 1),
        expand=expand,
        width=width,
    )


def section_title(text):
    return ft.Text(text, size=13, color=TEXT_SEC, weight=ft.FontWeight.BOLD)


def divider():
    return ft.Divider(color=BORDER, height=1)


def badge(text, color):
    return ft.Container(
        content=ft.Text(text, size=10, color='#000000',
                        weight=ft.FontWeight.BOLD),
        bgcolor=color,
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
    )


def passenger_tile(p):
    color = get_zone_color(p.zone)
    status = {
        'On Platform': AMBER,
        'Boarded': GREEN,
        'Alighted': TEXT_MUTED,
    }.get(p.status, TEXT_SEC)

    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=txt(p.passenger_id, size=10, color=TEXT_MUTED), width=75,
            ),
            ft.Column([
                txt(p.name, size=13, weight=ft.FontWeight.W_600),
                txt(f'{p.origin} → {p.destination} ({p.line})',
                    size=11, color=TEXT_SEC),
            ], spacing=2, expand=True),
            ft.Column([
                badge(p.zone.split(' - ')[0].strip(), color),
                txt(f'{p.stops} mins',
                    size=11, color=TEXT_SEC),
            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.END),
            ft.Container(
                content=txt(p.status, size=10, color=status, weight=ft.FontWeight.BOLD), width=80, alignment=ft.alignment.Alignment(1, 0)
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=SURFACE,
        border_radius=8,
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border=ft.Border.all(1, BORDER),
        margin=ft.Margin(0, 4, 0, 0)
    )


def build_train_visual(train):
    car_cards = []

    for car in train.cars:
        zone_columns = []

        for zone_name, passengers in car.zones.items():
            color = get_zone_color(zone_name)
            door_label = zone_name.split("-")[1].strip() \
                if "-" in zone_name else zone_name

            # passenger icons inside this zone
            passenger_icons = []
            for p in passengers:
                passenger_icons.append(
                    ft.Column([
                        ft.Icon(
                            ft.Icons.PERSON,
                            color=color,
                            size=16,
                            tooltip=f'{p.name} | {p.stops} mins | {p.position_label}',
                        ),
                        ft.Text(
                            p.position_label,
                            size=7,
                            color=color,
                            text_align=ft.TextAlign.CENTER,
                            no_wrap=False,
                        ),
                    ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )

            # empty zone placeholder
            if not passenger_icons:
                passenger_icons.append(
                    txt("empty", size=9, color=TEXT_MUTED)
                )

            zone_col = ft.Container(
                content=ft.Column([
                    # door label at top
                    ft.Container(
                        content=txt(
                            door_label, size=9,
                            color=color,
                            weight=ft.FontWeight.BOLD
                        ),
                        bgcolor=SURFACE,
                        border_radius=4,
                        padding=ft.Padding.symmetric(
                            horizontal=4, vertical=2
                        ),
                    ),
                    # passenger count
                    txt(
                        f"{len(passengers)} pax",
                        size=9, color=TEXT_MUTED
                    ),
                    # passenger icons
                    ft.Column(
                        passenger_icons,
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=CARD,
                border_radius=8,
                padding=8,
                border=ft.Border.all(1, color),
                expand=True,
            )
            zone_columns.append(zone_col)

        car_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TRAIN, color=ACCENT, size=14),
                    txt(f"Car {car.car_number}", size=12,
                        weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    txt(f"{car.total_passengers()}/{car.capacity}",
                        size=11, color=TEXT_SEC),
                ], spacing=6),
                divider(),
                ft.Row(zone_columns, spacing=6),
                # platform label at bottom
                ft.Container(
                    content=txt(
                        "← PLATFORM SIDE →",
                        size=9, color=TEXT_MUTED
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                    margin=ft.Margin(0, 4, 0, 0),
                ),
            ], spacing=8),
            bgcolor=SURFACE,
            border_radius=10,
            padding=12,
            border=ft.Border.all(1, BORDER),
            expand=True,
        )
        car_cards.append(car_card)

    return ft.Column([
        section_title("TRAIN VISUAL — 5 CARS × 4 ZONES"),
        ft.Row(car_cards, spacing=8),
        # zone legend
        ft.Row([
            txt("ZONES:", size=11, color=TEXT_MUTED),
            *[
                ft.Row([
                    ft.Container(
                        width=8, height=8,
                        bgcolor=color,
                        border_radius=2
                    ),
                    txt(zone.split("-")[0].strip(),
                        size=11, color=TEXT_SEC),
                ], spacing=4)
                for zone, color in ZONE_COLORS.items()
            ],
        ], spacing=12),
    ], spacing=8)


def main(page: ft.Page):
    page.title = "Transit Destination Grouping System"
    page.bgcolor = BG
    page.window.width = 1900
    page.window.height = 800
    page.window.min_width = 1700
    page.window.min_height = 800
    page.padding = 0

    system = TransitSystem()

    # --- FORM FIELDS ---
    name_field = ft.TextField(
        label="Passenger Name",
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        height=48,
        text_size=13,
        cursor_color=ACCENT,
    )

    line_dd = ft.Dropdown(
        label="Transit Line",
        options=[ft.dropdown.Option(k) for k in LINES.keys()],
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        text_size=13,
    )

    confirm_line_btn = ft.Button(
        "Confirm Line",
        icon=ft.Icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor=SURFACE,
            color=TEXT_SEC,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )

    arrive_dd = ft.Dropdown(
        label='Arriving at Station',
        options=[],
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        text_size=13
    )

    origin_dd = ft.Dropdown(
        label="Origin Station",
        options=[],
        disabled=True,
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        text_size=13,
    )

    dest_dd = ft.Dropdown(
        label="Destination Station",
        options=[],
        disabled=True,
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        text_size=13,
    )

    # --- FEEDBACK ---
    feedback = ft.Text("", size=12, color=GREEN)
    feedback_box = ft.Container(
        content=feedback,
        bgcolor=SURFACE,
        border_radius=8,
        padding=ft.Padding.symmetric(horizontal=10, vertical=8),
        visible=False,
    )

    # --- RESULT PANEL ---
    result_zone = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    result_id = ft.Text("", size=11, color=TEXT_MUTED)
    result_stops = ft.Text("", size=12, color=TEXT_SEC)
    result_path = ft.Text("", size=11, color=TEXT_SEC, no_wrap=False)
    result_desc = ft.Text("", size=11, color=TEXT_SEC, no_wrap=False)
    result_car = ft.Text("", size=12, color=ACCENT)
    result_panel = ft.Column([], visible=False, spacing=6)

    # --- LIST COLUMNS ---
    platform_col = ft.Column(
        [txt("— Empty —", color=TEXT_MUTED)],
        spacing=0, scroll=ft.ScrollMode.AUTO, expand=True
    )
    boarding_col = ft.Column(
        [txt("— Empty —", color=TEXT_MUTED)],
        spacing=0, scroll=ft.ScrollMode.AUTO, expand=True
    )

    # --- TRAIN VISUAL CONTAINER ---
    train_visual_container = ft.Ref[ft.Column]()

    # --- STAT TEXTS ---
    stat_platform = ft.Text("0", size=26, color=AMBER,
                            weight=ft.FontWeight.BOLD)
    stat_boarding = ft.Text("0", size=26, color=ACCENT,
                            weight=ft.FontWeight.BOLD)
    stat_train = ft.Text("0", size=26, color=GREEN,
                         weight=ft.FontWeight.BOLD)
    stat_alighted = ft.Text("0", size=26, color=TEXT_SEC,
                            weight=ft.FontWeight.BOLD)

    # --- EVENT HANDLERS ---

    def show_feedback(msg, success=True):
        feedback.value = msg
        feedback.color = GREEN if success else RED
        feedback_box.visible = True
        page.update()

    def update_stats():
        s = system.get_stats()
        stat_platform.value = str(s["on_platform"])
        stat_boarding.value = str(s["in_boarding_queue"])
        stat_train.value = str(s["total_in_train"])
        stat_alighted.value = str(s["total_alighted"])

    def refresh_lists():
        # platform queue
        platform_col.controls = (
            [passenger_tile(p) for p in system.platform_queue.all()]
            or [txt("— Empty —", color=TEXT_MUTED)]
        )
        # boarding queue
        boarding_col.controls = (
            [passenger_tile(p) for p in system.boarding_queue.all()]
            or [txt("— Empty —", color=TEXT_MUTED)]
        )
        update_stats()
        refresh_train_visual()
        page.update()

    def refresh_train_visual():
        new_visual = build_train_visual(system.train)
        train_visual_ref.controls = new_visual.controls
        page.update()

    def on_line_change(e):
        line = line_dd.value
        if line and line in LINES:
            opts = [ft.dropdown.Option(s) for s in LINES[line]]
            origin_dd.options = opts
            dest_dd.options = opts
            arrive_dd.options = opts
            origin_dd.value = None
            dest_dd.value = None
            origin_dd.disabled = False
            dest_dd.disabled = False
            print(f'Stations loaded: {len(opts)}')
        page.update()

    line_dd.on_change = on_line_change
    confirm_line_btn.on_click = on_line_change

    def on_register(e):
        ok, msg, p = system.register_passenger(
            name=name_field.value or "",
            line=line_dd.value or "",
            origin=origin_dd.value or "",
            destination=dest_dd.value or "",
        )
        if not ok:
            show_feedback(msg, success=False)
            result_panel.visible = False
            page.update()
            return

        # fill result panel
        result_id.value = f"ID: {p.passenger_id}  •  {p.timestamp}"
        result_zone.value = p.zone
        result_zone.color = get_zone_color(p.zone)
        result_stops.value = f"{p.stops} mins travel time"
        result_path.value = "  →  ".join(p.path)
        result_desc.value = p.zone_desc
        result_car.value = "Pending boarding assignment..."

        result_panel.controls = [
            divider(),
            txt("BOARDING ASSIGNMENT", size=11, color=TEXT_MUTED),
            result_id,
            result_zone,
            result_stops,
            txt("Route:", size=11, color=TEXT_MUTED),
            result_path,
            ft.Container(
                content=result_desc,
                bgcolor=SURFACE,
                border_radius=8,
                padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                border=ft.Border.all(1, BORDER),
            ),
            result_car,
        ]
        result_panel.visible = True

        # clear form
        name_field.value = ""
        origin_dd.value = None
        dest_dd.value = None

        show_feedback(f"✓ {p.name} registered!", success=True)
        refresh_lists()

    def on_board_next(e):
        ok, msg, p = system.board_next()
        if ok and p:
            result_car.value = f"Assigned to Car {p.car_number}"
        show_feedback(msg, success=ok)
        refresh_lists()

    def on_board_all(e):
        count, _ = system.board_all()
        show_feedback(
            f"✓ {count} passenger(s) boarded in priority order.",
            success=count > 0
        )
        refresh_lists()

    def on_alight(e):
        # alight the first boarded passenger found
        for car in system.train.cars:
            for zone_list in car.zones.values():
                if zone_list:
                    p = zone_list[0]
                    system.alight_passenger(p.passenger_id)
                    show_feedback(
                        f"✓ {p.name} alighted at {p.destination}.",
                        success=True
                    )
                    refresh_lists()
                    return
        show_feedback("No passengers to alight.", success=False)

    def on_arrive_at_station(e):
        station = arrive_dd.value
        if not station:
            show_feedback("Please select a station first.", success=False)
            return

        alighted = system.arrive_at_station(station)

        if not alighted:
            show_feedback(
                f"No passengers alighting at {station}.",
                success=False
            )
        else:
            names = ", ".join(p.name for p in alighted)
            show_feedback(
                f"✓ {len(alighted)} passenger(s) alighted at {station}: {names}",
                success=True
            )
        refresh_lists()

    def on_reset(e):
        system.reset_system()
        result_panel.visible = False
        feedback_box.visible = False
        name_field.value = ""
        line_dd.value = None
        origin_dd.value = None
        dest_dd.value = None
        arrive_dd.value = None
        origin_dd.options = []
        dest_dd.options = []
        arrive_dd.options = []
        origin_dd.disabled = True
        dest_dd.disabled = True
        refresh_lists()

    # --- BUILD LAYOUT ---

    # header
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.TRAIN, color=ACCENT, size=28),
            ft.Column([
                ft.Text("Transit Destination Grouping System",
                        size=18, color=TEXT_PRI,
                        weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Dijkstra  •  Priority Queue  •  FIFO  •  Stack  |  CS2-1",
                    size=11, color=TEXT_MUTED
                ),
            ], spacing=1, expand=True),
        ], spacing=12),
        bgcolor=SURFACE,
        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
    )

    # stats row
    def stat_box(label, value_widget, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=10, color=TEXT_MUTED),
                value_widget,
            ], spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=CARD,
            border_radius=10,
            padding=ft.Padding.symmetric(vertical=12, horizontal=20),
            border=ft.Border.all(1, BORDER),
            expand=True,
        )

    stats_row = ft.Row([
        stat_box("On Platform",     stat_platform, AMBER),
        stat_box("Boarding Queue",  stat_boarding, ACCENT),
        stat_box("In Train",        stat_train,    GREEN),
        stat_box("Alighted",        stat_alighted, TEXT_SEC),
    ], spacing=10)

    # control buttons
    controls = ft.Row([
        ft.Button(
            "Board Next",
            on_click=on_board_next,
            icon=ft.Icons.ARROW_CIRCLE_RIGHT,
            style=ft.ButtonStyle(
                bgcolor=GREEN, color="#000000",
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding.symmetric(vertical=10, horizontal=14),
            ),
        ),
        ft.Button(
            "Board All",
            on_click=on_board_all,
            icon=ft.Icons.DONE_ALL,
            style=ft.ButtonStyle(
                bgcolor=ACCENT, color=TEXT_PRI,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding.symmetric(vertical=10, horizontal=14),
            ),
        ),
        ft.Container(
            content=arrive_dd,
            width=200,
        ),

        ft.Button(
            'Arrive at Station',
            on_click=on_arrive_at_station,
            icon=ft.Icons.TRAIN,
            style=ft.ButtonStyle(
                bgcolor=AMBER, color='#000000',
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding.symmetric(vertical=10, horizontal=14),
            ),
        ),

        ft.Container(expand=True),
        ft.OutlinedButton(
            "Reset System",
            on_click=on_reset,
            icon=ft.Icons.REFRESH,
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, RED),
                color=RED,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),
    ], spacing=8)

    # left panel — registration form
    left_panel = ft.Container(
        content=ft.Column([
            ft.Text("Register Passenger", size=16,
                    color=TEXT_PRI, weight=ft.FontWeight.BOLD),
            divider(),
            name_field,
            line_dd,
            confirm_line_btn,
            origin_dd,
            dest_dd,
            ft.Button(
                "Register & Assign Zone",
                on_click=on_register,
                icon=ft.Icons.PERSON_ADD,
                style=ft.ButtonStyle(
                    bgcolor=ACCENT, color=TEXT_PRI,
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.Padding.symmetric(vertical=14),
                ),
                width=float("inf"),
            ),
            feedback_box,
            result_panel,
        ], spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True),
        width=290,
        bgcolor=SURFACE,
        border=ft.Border.only(right=ft.BorderSide(1, BORDER)),
        padding=ft.Padding.all(18),
    )

    # queue panels
    def queue_panel(title, subtitle, col, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=color, size=16),
                    ft.Column([
                        ft.Text(title, size=13, color=TEXT_PRI,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(subtitle, size=10, color=TEXT_MUTED),
                    ], spacing=1, expand=True),
                ], spacing=8),
                divider(),
                col,
            ], spacing=8),
            bgcolor=CARD,
            border_radius=12,
            padding=16,
            border=ft.Border.all(1, BORDER),
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    queues_row = ft.Row([
        queue_panel(
            "Platform Queue (FIFO)",
            "Arrival order — First In First Out",
            platform_col,
            ft.Icons.PEOPLE, AMBER,
        ),
        queue_panel(
            "Priority Boarding Queue",
            "Longest trip boards first",
            boarding_col,
            ft.Icons.SORT, ACCENT,
        ),
    ], spacing=10, expand=True)

    # train visual ref
    train_visual_ref = ft.Column([], spacing=8)

    def refresh_train_visual():
        new_visual = build_train_visual(system.train)
        train_visual_ref.controls = new_visual.controls
        page.update()

    refresh_train_visual()

    # right panel
    right_panel = ft.Container(
        content=ft.Column([
            stats_row,
            controls,
            queues_row,
            divider(),
            ft.Container(
                content=train_visual_ref,
                bgcolor=SURFACE,
                border_radius=12,
                padding=16,
                border=ft.Border.all(1, BORDER),
            ),

        ], spacing=12, expand=True),
        expand=True,
        padding=ft.Padding.all(18),
    )

    # full layout
    page.add(
        ft.Column([
            header,
            ft.Row([left_panel, right_panel],
                   expand=True, spacing=0),
        ], spacing=0, expand=True)
    )

    from demo import run_demo
    run_demo(system)

    refresh_lists()


ft.app(target=main)
