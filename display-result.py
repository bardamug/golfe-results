import flet as ft
import pandas as pd

def main(page: ft.Page):
    print("\n[SYSTEM] Inicializando Leaderboard Ultra-Compacto...")
    
    page.title = "Resultados Golfville"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "adaptive"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def create_golf_table(df_tee, label, color, text_color=ft.Colors.WHITE):
        if df_tee.empty:
            return ft.Text(f"Vazio: {label}", color=ft.Colors.GREY_400)

        table = ft.DataTable(
            heading_row_color=ft.Colors.BLUE_GREY_50,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            column_spacing=30,
            # Ultra-compact heights
            heading_row_height=28,    
            data_row_min_height=24,   
            columns=[
                ft.DataColumn(ft.Text("Jogador", weight="bold", size=13)),
                ft.DataColumn(ft.Text("Gross", weight="bold", size=13), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['Jogador'], size=13)),
                        ft.DataCell(ft.Text(str(int(row['Gross'])), weight="bold", size=13)),
                    ]
                ) for _, row in df_tee.iterrows()
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

    def get_data():
        try:
            df = pd.read_csv('cartoes_golfville.csv', encoding='latin-1', sep=';')
            df.columns = df.columns.str.strip()
            # Double Filter: Latest Game (1) + 18 Holes (18)
            mask = (df['Ultimojogo'].astype(int) == 1) & (df['Buracos'].astype(int) == 18)
            df_filtered = df[mask].copy()
            return df_filtered.sort_values(by='Gross')
        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    df = get_data()

    if df is not None:
        # Categorization based on Tee
        df_m1 = df[df['Tee'] == 'Azur']
        df_m2 = df[df['Tee'] == 'Branco']
        df_fem = df[df['Tee'] == 'Vermelho']
        
        responsive_layout = ft.ResponsiveRow(
            columns=12,
            spacing=15,
            run_spacing=20,
            controls=[
                ft.Column([create_golf_table(df_m1, "M1", ft.Colors.BLUE_800)], col={"sm": 12, "md": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([create_golf_table(df_m2, "M2", ft.Colors.BLUE_GREY_100, ft.Colors.BLACK)], col={"sm": 12, "md": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([create_golf_table(df_fem, "Feminino", ft.Colors.RED_800)], col={"sm": 12, "md": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ]
        )

        page.add(
            ft.Text("Resultados Golfville", size=28, weight="bold", color=ft.Colors.BLUE_900),
            ft.Text("Leaderboard 18 Buracos", size=14, color=ft.Colors.BLUE_GREY_700),
            ft.Divider(height=15),
            responsive_layout
        )
    else:
        page.add(ft.Text("Erro ao carregar dados.", color="red"))

if __name__ == "__main__":
    ft.app(target=main)