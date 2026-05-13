import flet as ft
from engine import TransitSystem, LINES, Passenger


BG = "#0D0F14"
SURFACE = "#161B24"
CARD = "#1C2333"
BORDER = "#2A3450"
ACCENT = "#3B82F6"
ACCENT2 = "#10B981"
WARN = "#F59E0B"
DANGER = "#EF4444"
TEXT_PRI = "#F0F4FF"
TEXT_SEC = "#8B9CC8"
TEXT_MUTED = "#4B5A7A"

ZONE_COLORS = {
    "ZONE A": "#10B981",
    "ZONE B": "#F59E0B",
    "ZONE C": "#EF4444",
}


def zone_color(zone: str) -> str:
    for k, v in ZONE_COLORS.items():
        if zone.startswith(k):
            return v
    return ACCENT


def card(content, padding=16, expand=False):
    return ft.Container(
        content=content,
        bgcolor=CARD,
        border_radius=12,
        padding=padding,
        border=ft.border.all(1, BORDER),
        expand=expand,
    )


def label(text: str, size=12, color=TEXT_SEC, weight=None):
    return ft.Text(text, size=size, color=color, weight=weight)


def heading(text: str, size=18, color=TEXT_PRI):
    return ft.Text(text, size=size, color=color, weight=ft.FontWeight.BOLD)


def stat_box(title: str, value: str, color: str = ACCENT):
    return card(
        ft.Column([
            label(title, size=11),
            ft.Text(value, size=28, color=color, weight=ft.FontWeight.BOLD),
        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.symmetric(vertical=14, horizontal=18),
    )


def zone_badge(zone: str):
    short = zone.split("—")[0].strip()
    return ft.Container(
        content=ft.Text(short, size=10, color="#000000",
                        weight=ft.FontWeight.BOLD),
        bgcolor=zone_color(zone),
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
    )


def passenger_tile(p: Passenger):
    status_color = {
        "On Platform": WARN,
        "Boarded": ACCENT2,
        "Alighted": TEXT_MUTED,
    }.get(p.status, TEXT_SEC)

    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text(p.passenger_id, size=10,
                                color=TEXT_MUTED, weight=ft.FontWeight.BOLD),
                width=68,
            ),
            ft.Column([
                ft.Text(p.name, size=13, color=TEXT_PRI,
                        weight=ft.FontWeight.W_600),
                ft.Text(f"{p.origin}  →  {p.destination}  ({p.line})",
                        size=11, color=TEXT_SEC),
            ], spacing=1, expand=True),
            ft.Column([
                zone_badge(p.zone),
                ft.Text(f"{p.stops} stop{'s' if p.stops != 1 else ''}",
                        size=11, color=TEXT_SEC),
            ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.END),
            ft.Container(
                content=ft.Text(p.status, size=10,
                                color=status_color, weight=ft.FontWeight.BOLD),
                width=84,
                alignment=ft.alignment.center_right,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=SURFACE,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
        border=ft.border.all(1, BORDER),
        margin=ft.margin.only(bottom=4),
    )


def main(page: ft.Page):
    page.title = "Transit Destination Grouping System"
    page.bgcolor = BG
    page.window.width = 1100
    page.window.height = 780
    page.window.min_width = 900
    page.window.min_height = 650
    page.padding = 0
    page.fonts = {
        "Mono": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap"
    }
    page.theme = ft.Theme(color_scheme_seed=ACCENT)

    system = TransitSystem()

    feedback_text = ft.Ref[ft.Text]()
    feedback_container = ft.Ref[ft.Container]()
    stats_row = ft.Ref[ft.Row]()

    # Registration fields
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
        height=48,
        text_size=13,
    )

    origin_dd = ft.Dropdown(
        label="Origin Station",
        options=[],
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        height=48,
        text_size=13,
    )

    dest_dd = ft.Dropdown(
        label="Destination Station",
        options=[],
        border_color=BORDER,
        focused_border_color=ACCENT,
        label_style=ft.TextStyle(color=TEXT_SEC),
        color=TEXT_PRI,
        bgcolor=SURFACE,
        border_radius=8,
        height=48,
        text_size=13,
    )

    result_panel = ft.Ref[ft.Column]()
    result_id = ft.Ref[ft.Text]()
    result_zone = ft.Ref[ft.Text]()
    result_stops = ft.Ref[ft.Text]()
    result_path = ft.Ref[ft.Text]()
    result_desc = ft.Ref[ft.Text]()

    platform_list = ft.Ref[ft.Column]()
    boarding_list = ft.Ref[ft.Column]()
    traincar_list = ft.Ref[ft.Column]()

    stat_platform = ft.Ref[ft.Text]()
    stat_boarding = ft.Ref[ft.Text]()
    stat_train = ft.Ref[ft.Text]()
    stat_alighted = ft.Ref[ft.Text]()

    def show_feedback(msg: str, success: bool = True):
        color = ACCENT2 if success else DANGER
        feedback_text.current.value = msg
        feedback_text.current.color = color
        feedback_container.current.visible = True
        page.update()

    def update_stats():
        s = system.get_stats()
        stat_platform.current.value = str(s["on_platform"])
        stat_boarding.current.value = str(s["in_boarding_queue"])
        stat_train.current.value = f"{s['in_train']}/{s['train_capacity']}"
        stat_alighted.current.value = str(s["total_alighted"])

    def refresh_lists():
        platform_list.current.controls = (
            [passenger_tile(p) for p in system.platform_queue.all()]
            or [label("— Queue is empty —", color=TEXT_MUTED)]
        )
        boarding_list.current.controls = (
            [passenger_tile(p) for p in system.boarding_queue.all()]
            or [label("— No passengers waiting —", color=TEXT_MUTED)]
        )
        traincar_list.current.controls = (
            [passenger_tile(p) for p in system.train_car.all()]
            or [label("— Train car is empty —", color=TEXT_MUTED)]
        )
        update_stats()
        page.update()

    def on_line_change(e):
        line = line_dd.value
        if line and line in LINES:
            stations = LINES[line]
            opts = [ft.dropdown.Option(s) for s in stations]
            origin_dd.options = opts
            dest_dd.options = opts
            origin_dd.value = None
            dest_dd.value = None
        page.update()

    line_dd.on_change = on_line_change

    def on_register(e):
        ok, msg, p = system.register_passenger(
            name=name_field.value or "",
            line=line_dd.value or "",
            origin=origin_dd.value or "",
            destination=dest_dd.value or "",
        )
        if not ok:
            show_feedback(msg, success=False)
            result_panel.current.visible = False
            page.update()
            return

        result_id.current.value = f"ID: {p.passenger_id}  •  {p.timestamp}"
        result_zone.current.value = p.zone
        result_zone.current.color = zone_color(p.zone)
        result_stops.current.value = f"{p.stops} stop{'s' if p.stops != 1 else ''}"
        result_path.current.value = "  →  ".join(p.path)
        result_desc.current.value = p.zone_desc
        result_panel.current.visible = True

        name_field.value = ""
        origin_dd.value = None
        dest_dd.value = None

        show_feedback(f"✓ {p.name} registered successfully!", success=True)
        refresh_lists()

    def on_board_next(e):
        ok, msg, _ = system.board_next()
        show_feedback(msg, success=ok)
        refresh_lists()

    def on_board_all(e):
        count, _ = system.board_all()
        show_feedback(
            f"✓ {count} passenger(s) boarded in priority order.", success=count > 0)
        refresh_lists()

    def on_alight(e):
        ok, msg, _ = system.alight_next()
        show_feedback(msg, success=ok)
        refresh_lists()

    def on_reset(e):
        system.reset()
        result_panel.current.visible = False
        feedback_container.current.visible = False
        name_field.value = ""
        line_dd.value = None
        origin_dd.value = None
        dest_dd.value = None
        origin_dd.options = []
        dest_dd.options = []
        refresh_lists()

    register_form = ft.Column([
        heading("Register Passenger", size=16),
        ft.Divider(color=BORDER, height=1),
        name_field,
        line_dd,
        origin_dd,
        dest_dd,
        ft.ElevatedButton(
            "Register & Assign Zone",
            on_click=on_register,
            style=ft.ButtonStyle(
                bgcolor=ACCENT,
                color=TEXT_PRI,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(vertical=14),
            ),
            width=float("inf"),
            icon=ft.Icons.PERSON_ADD,
        ),

        ft.Container(
            ref=feedback_container,
            content=ft.Text("", ref=feedback_text, size=12),
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            border_radius=8,
            bgcolor=SURFACE,
            visible=False,
        ),

        ft.Column(
            ref=result_panel,
            visible=False,
            controls=[
                ft.Divider(color=BORDER, height=1),
                label("BOARDING ASSIGNMENT", size=11, color=TEXT_MUTED),
                ft.Text("", ref=result_id, size=11, color=TEXT_MUTED),
                ft.Text("", ref=result_zone, size=15,
                        weight=ft.FontWeight.BOLD),
                ft.Text("", ref=result_stops, size=12, color=TEXT_SEC),
                label("Optimal Path:", size=11, color=TEXT_MUTED),
                ft.Text("", ref=result_path, size=11,
                        color=TEXT_SEC, no_wrap=False, max_lines=4),
                ft.Container(
                    content=ft.Text("", ref=result_desc, size=11,
                                    color=TEXT_SEC, no_wrap=False, max_lines=3),
                    bgcolor=SURFACE, border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    border=ft.border.all(1, BORDER),
                ),
            ],
            spacing=6,
        ),
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    controls_row = ft.Row([
        ft.ElevatedButton(
            "Board Next (Priority)",
            on_click=on_board_next,
            icon=ft.Icons.ARROW_CIRCLE_RIGHT,
            style=ft.ButtonStyle(
                bgcolor=ACCENT2,
                color="#000000",
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(vertical=10, horizontal=14),
            ),
        ),
        ft.ElevatedButton(
            "Board All",
            on_click=on_board_all,
            icon=ft.Icons.DONE_ALL,
            style=ft.ButtonStyle(
                bgcolor="#1D4ED8",
                color=TEXT_PRI,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(vertical=10, horizontal=14),
            ),
        ),
        ft.ElevatedButton(
            "Alight Next",
            on_click=on_alight,
            icon=ft.Icons.LOGOUT,
            style=ft.ButtonStyle(
                bgcolor=WARN,
                color="#000000",
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(vertical=10, horizontal=14),
            ),
        ),
        ft.Container(expand=True),
        ft.OutlinedButton(
            "Reset System",
            on_click=on_reset,
            icon=ft.Icons.REFRESH,
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, DANGER),
                color=DANGER,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),
    ], spacing=8)

    def _stat(label_txt: str, ref, color=ACCENT):
        return ft.Container(
            content=ft.Column([
                ft.Text(label_txt, size=10, color=TEXT_MUTED),
                ft.Text("0", ref=ref, size=26, color=color,
                        weight=ft.FontWeight.BOLD),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=CARD,
            border_radius=10,
            padding=ft.padding.symmetric(vertical=12, horizontal=20),
            border=ft.border.all(1, BORDER),
            expand=True,
        )

    stats_row_widget = ft.Row([
        _stat("On Platform",      stat_platform, WARN),
        _stat("Boarding Queue",   stat_boarding, ACCENT),
        _stat("In Train / Cap",   stat_train,    ACCENT2),
        _stat("Alighted",         stat_alighted, TEXT_SEC),
    ], spacing=10)

    def list_panel(title: str, subtitle: str, ref, icon, color):
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
                ft.Divider(color=BORDER, height=1),
                ft.Column(
                    ref=ref,
                    controls=[label("— Empty —", color=TEXT_MUTED)],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ], spacing=8, expand=True),
            bgcolor=CARD,
            border_radius=12,
            padding=16,
            border=ft.border.all(1, BORDER),
            expand=True,
        )

    lists_row = ft.Row([
        list_panel(
            "Platform Queue (FIFO)",
            "Arrival order — First In, First Out",
            platform_list,
            ft.Icons.PEOPLE,
            WARN,
        ),
        list_panel(
            "Priority Boarding Queue",
            "Dijkstra-sorted — longest trip boards first",
            boarding_list,
            ft.Icons.SORT,
            ACCENT,
        ),
        list_panel(
            "Train Car  (Stack)",
            "Current occupants — top = nearest door",
            traincar_list,
            ft.Icons.TRAIN,
            ACCENT2,
        ),
    ], spacing=10, expand=True)

    legend = ft.Row([
        label("ZONE LEGEND:", size=11, color=TEXT_MUTED),
        *[
            ft.Row([
                ft.Container(width=10, height=10, bgcolor=c, border_radius=2),
                label(k, size=11, color=TEXT_SEC),
            ], spacing=4)
            for k, c in ZONE_COLORS.items()
        ],
    ], spacing=12)

    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.TRAIN, color=ACCENT, size=28),
            ft.Column([
                ft.Text("Transit Destination Grouping System",
                        size=18, color=TEXT_PRI, weight=ft.FontWeight.BOLD),
                ft.Text("Dijkstra · Priority Queue · FIFO · Stack  |  CS2-1 Final Project",
                        size=11, color=TEXT_MUTED),
            ], spacing=1, expand=True),
        ], spacing=12),
        bgcolor=SURFACE,
        padding=ft.padding.symmetric(horizontal=24, vertical=14),
        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
    )

    left_panel = ft.Container(
        content=register_form,
        width=290,
        bgcolor=SURFACE,
        border=ft.border.only(right=ft.BorderSide(1, BORDER)),
        padding=ft.padding.all(18),
    )

    right_panel = ft.Container(
        content=ft.Column([
            stats_row_widget,
            controls_row,
            legend,
            lists_row,
        ], spacing=12, expand=True),
        expand=True,
        padding=ft.padding.all(18),
    )

    body = ft.Row([left_panel, right_panel], expand=True, spacing=0)

    page.add(
        ft.Column([header, body], spacing=0, expand=True)
    )

    refresh_lists()


ft.app(target=main)
