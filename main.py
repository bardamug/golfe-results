import flet as ft
import pandas as pd


def main(page: ft.Page):
    page.title = "Resultados Golfville"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "adaptive"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ── Load all data once ────────────────────────────────────────────────────
    def load_all_data():
        try:
            df = pd.read_csv('cartoes_golfville.csv', encoding='latin-1', sep=';')
            df.columns = df.columns.str.strip()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            return df
        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    df_all = load_all_data()

    # ── Last-tournament leaderboard ───────────────────────────────────────────
    def create_golf_table(df_tee, label, color, text_color=ft.Colors.WHITE):
        if df_tee.empty:
            return ft.Text(f"Vazio: {label}", color=ft.Colors.GREY_400)

        table = ft.DataTable(
            heading_row_color=ft.Colors.BLUE_GREY_50,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            column_spacing=30,
            heading_row_height=26,
            data_row_min_height=20,
            data_row_max_height=20,
            columns=[
                ft.DataColumn(ft.Text("Jogador", weight="bold", size=13)),
                ft.DataColumn(ft.Text("Gross",   weight="bold", size=13), numeric=True),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(row['Jogador'], size=13)),
                    ft.DataCell(ft.Text(str(int(row['Gross'])), weight="bold", size=13)),
                ])
                for _, row in df_tee.iterrows()
            ]
        )

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.Text(label, color=text_color, weight="bold", size=16),
                    bgcolor=color,
                    padding=ft.padding.symmetric(vertical=4, horizontal=20),
                    border_radius=ft.border_radius.only(top_left=10, top_right=10),
                    alignment=ft.Alignment(0, 0),
                ),
                table
            ]
        )

    def get_last_tournament(df):
        try:
            mask = (df['Ultimojogo'].astype(int) == 1) & (df['Buracos'].astype(int) == 18)
            return df[mask].copy().sort_values(by='Gross')
        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    # ── Player history ────────────────────────────────────────────────────────
    history_content = ft.Column(
        controls=[ft.Text("Selecione um jogador para ver o histórico.",
                          color=ft.Colors.GREY_500, size=13)],
        spacing=10,
    )

    def get_player_rows(player_name):
        if df_all is None or not player_name:
            return []
        df_p = df_all[df_all['Jogador'] == player_name].copy()
        df_p = df_p.sort_values('Data', ascending=False)
        result = []
        for _, row in df_p.iterrows():
            entry = {
                'Torneio':  str(row.get('Torneio', '')),
                'Data':     row['Data'].strftime('%d/%m/%Y') if pd.notna(row['Data']) else '',
                'Tee':      str(row.get('Tee', '')),
                'HCP':      str(int(row['Handicap'])) if pd.notna(row.get('Handicap')) else '-',
                'Gross':    str(int(row['Gross']))    if pd.notna(row.get('Gross'))    else '-',
                'Buracos':  str(int(row['Buracos']))  if pd.notna(row.get('Buracos'))  else '-',
            }
            for h in range(1, 19):
                val = row.get(str(h), None)
                try:
                    entry[str(h)] = str(int(float(val))) if pd.notna(val) else '-'
                except (ValueError, TypeError):
                    entry[str(h)] = '-'
            result.append(entry)
        return result

    def build_history_table(rows_data):
        columns = [
            ft.DataColumn(ft.Text("Torneio", weight="bold", size=11)),
            ft.DataColumn(ft.Text("Data",    weight="bold", size=11)),
            ft.DataColumn(ft.Text("Gross",   weight="bold", size=11), numeric=True),
            ft.DataColumn(ft.Text("Tee",     weight="bold", size=11)),
            ft.DataColumn(ft.Text("HCP",     weight="bold", size=11), numeric=True),
            *[ft.DataColumn(ft.Text(str(h),  weight="bold", size=10), numeric=True)
              for h in range(1, 19)],
        ]
        rows = []
        for r in rows_data:
            cells = [
                ft.DataCell(ft.Text(r['Torneio'], size=10,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    max_lines=1, width=140)),
                ft.DataCell(ft.Text(r['Data'],    size=10)),
                ft.DataCell(ft.Text(r['Gross'],   size=10, weight="bold")),
                ft.DataCell(ft.Text(r['Tee'],     size=10)),
                ft.DataCell(ft.Text(r['HCP'],     size=10)),
                *[ft.DataCell(ft.Text(r[str(h)],  size=10)) for h in range(1, 19)],
            ]
            rows.append(ft.DataRow(cells=cells))

        return ft.DataTable(
            heading_row_color=ft.Colors.BLUE_GREY_50,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            border_radius=10,
            column_spacing=6,
            heading_row_height=26,
            data_row_min_height=20,
            data_row_max_height=20,
            columns=columns,
            rows=rows,
        )

    def load_player_history(player_name):
        rows_data = get_player_rows(player_name)
        history_content.controls.clear()
        if not rows_data:
            history_content.controls.append(
                ft.Text("Nenhum dado encontrado para este jogador.",
                        color=ft.Colors.GREY_500, size=13)
            )
        else:
            history_content.controls.append(
                ft.Row(
                    [ft.Text(f"{len(rows_data)} rodada(s) encontrada(s)",
                             size=12, color=ft.Colors.BLUE_GREY_600)],
                    alignment=ft.MainAxisAlignment.END,
                )
            )
            history_content.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[build_history_table(rows_data)],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                    border_radius=10,
                    padding=0,
                )
            )
        history_content.update()

    # ── Custom compact dropdown ───────────────────────────────────────────────
    def build_history_section(df):
        if df is None:
            return ft.Text("Erro ao carregar dados.", color="red")

        player_names = sorted(df['Jogador'].dropna().unique().tolist())

        ITEM_H   = 28   # px per list item
        MAX_ROWS = 8    # max visible rows before scroll

        selected_name = [None]  # mutable ref

        selected_text = ft.Text(
            "Selecionar Jogador...",
            size=13,
            color=ft.Colors.BLUE_GREY_400,
            expand=True,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        arrow_icon = ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.BLUE_GREY_600)

        dropdown_field = ft.Container(
            content=ft.Row(
                controls=[selected_text, arrow_icon],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            border=ft.border.all(1, ft.Colors.BLUE_800),
            border_radius=6,
            padding=ft.Padding(left=12, top=6, right=8, bottom=6),
            expand=True,
            bgcolor=ft.Colors.WHITE,
        )

        # The popup list — starts hidden
        list_items = []

        # map name -> container so we can highlight by name
        item_map = {}

        def set_highlight(name):
            """Highlight one item, clear all others."""
            for n, itm in item_map.items():
                selected = (n == name)
                itm.bgcolor = ft.Colors.BLUE_700 if selected else ft.Colors.WHITE
                itm.content.color = ft.Colors.WHITE if selected else ft.Colors.BLUE_GREY_900
                itm.update()

        def make_item(name):
            item = ft.Container(
                content=ft.Text(name, size=13, weight="bold", color=ft.Colors.BLUE_GREY_900),
                height=ITEM_H,
                padding=ft.Padding(left=12, top=0, right=12, bottom=0),
                alignment=ft.Alignment(-1, 0),
                bgcolor=ft.Colors.WHITE,
                ink=True,
                ink_color=ft.Colors.BLUE_700,
            )
            def on_hover(e, n=name):
                # desktop: highlight on mouse-over (don't override selected)
                if e.data == "true":
                    set_highlight(n)
                elif n != selected_name[0]:
                    item_map[n].bgcolor = ft.Colors.WHITE
                    item_map[n].update()
            def on_tap_down(e, n=name):
                # mobile: highlight immediately on finger press
                set_highlight(n)
            def on_click(e, n=name):
                selected_name[0] = n
                set_highlight(n)
                close_popup()
                selected_text.value = n
                selected_text.color = ft.Colors.BLUE_GREY_900
                selected_text.update()
                load_player_history(n)
            item.on_hover    = on_hover
            item.on_tap_down = on_tap_down
            item.on_click    = on_click
            return item

        for n in player_names:
            itm = make_item(n)
            item_map[n] = itm
            list_items.append(itm)

        popup_height = min(len(player_names), MAX_ROWS) * ITEM_H

        popup = ft.Container(
            content=ft.ListView(
                controls=list_items,
                item_extent=ITEM_H,
                height=popup_height,
            ),
            border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
            border_radius=6,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 3),
            ),
            visible=False,
            expand=True,
        )

        def close_popup():
            popup.visible = False
            arrow_icon.name = ft.Icons.ARROW_DROP_DOWN
            popup.update()
            arrow_icon.update()

        def refresh_highlights():
            for n, itm in item_map.items():
                selected = (n == selected_name[0])
                itm.bgcolor = ft.Colors.BLUE_700 if selected else ft.Colors.WHITE
                itm.content.color = ft.Colors.WHITE if selected else ft.Colors.BLUE_GREY_900

        def toggle_popup(e):
            popup.visible = not popup.visible
            arrow_icon.name = (ft.Icons.ARROW_DROP_UP
                               if popup.visible else ft.Icons.ARROW_DROP_DOWN)
            if popup.visible:
                refresh_highlights()
                for itm in list_items:
                    itm.update()
            popup.update()
            arrow_icon.update()

        dropdown_field.on_click = toggle_popup

        dropdown_stack = ft.Column(
            controls=[dropdown_field, popup],
            spacing=2,
            expand=True,
        )

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.Text("Histórico do Jogador",
                                    color=ft.Colors.WHITE, weight="bold", size=16),
                    bgcolor=ft.Colors.BLUE_900,
                    padding=ft.padding.symmetric(vertical=6, horizontal=20),
                    border_radius=ft.border_radius.only(top_left=10, top_right=10),
                ),
                ft.Container(
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Row([dropdown_stack],
                                   alignment=ft.MainAxisAlignment.START,
                                   expand=True),
                            history_content,
                        ],
                    ),
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                    border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
                    padding=ft.padding.all(16),
                ),
            ]
        )

    # ── Assemble page ─────────────────────────────────────────────────────────
    if df_all is not None:
        df_last = get_last_tournament(df_all)

        if df_last is not None:
            df_m1  = df_last[df_last['Tee'] == 'Azur']
            df_m2  = df_last[df_last['Tee'] == 'Branco']
            df_fem = df_last[df_last['Tee'] == 'Vermelho']

            leaderboard = ft.ResponsiveRow(
                columns=12,
                spacing=15,
                run_spacing=20,
                controls=[
                    ft.Column(
                        [create_golf_table(df_m1, "M1", ft.Colors.BLUE_800)],
                        col={"sm": 12, "md": 4},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [create_golf_table(df_m2, "M2",
                                           ft.Colors.BLUE_GREY_100, ft.Colors.BLACK)],
                        col={"sm": 12, "md": 4},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [create_golf_table(df_fem, "Feminino", ft.Colors.RED_800)],
                        col={"sm": 12, "md": 4},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ]
            )
        else:
            leaderboard = ft.Text("Sem dados do último torneio.", color="orange")

        page.add(
            ft.Text("Resultados Golfville", size=28, weight="bold",
                    color=ft.Colors.BLUE_900),
            ft.Text("Leaderboard 18 Buracos", size=14,
                    color=ft.Colors.BLUE_GREY_700),
            ft.Divider(height=15),
            leaderboard,
            ft.Divider(height=30),
            build_history_section(df_all),
        )
    else:
        page.add(ft.Text("Erro ao carregar dados.", color="red"))


if __name__ == "__main__":
    ft.app(
        target=main, 
        view=None,             # No desktop window
        port=7860,             # Mandatory for Hugging Face
        host="0.0.0.0",        # Listen on all network interfaces
        export_to_html=False   # Run as a dynamic app
    )