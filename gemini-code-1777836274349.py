import flet as ft
import pandas as pd

def main(page: ft.Page):
    # Terminal Log: Start
    print("\n[SYSTEM] Inicializando Resultados Golfville...")
    
    page.title = "Resultados Golfville"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "adaptive"
    
    # Page-level centering
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    header = ft.Text("Resultados Golfville", size=32, weight="bold", color=ft.Colors.BLUE_900)
    subheader = ft.Text("Competição 18 Buracos", size=16, color=ft.Colors.BLUE_GREY_700)

    def get_data():
        try:
            # 1. Load Data
            print("[DATA] Lendo 'cartoes_golfville.csv'...")
            df = pd.read_csv('cartoes_golfville.csv', encoding='latin-1', sep=';')
            df.columns = df.columns.str.strip()
            print(f"[DATA] Carga inicial: {len(df)} linhas detectadas.")
            
            # 2. Apply Filters (Ultimojogo=1 AND Buracos=18)
            mask = (df['Ultimojogo'].astype(int) == 1) & (df['Buracos'].astype(int) == 18)
            df_filtered = df[mask].copy()
            print(f"[FILTER] Filtro aplicado: {len(df_filtered)} jogadores (18 Buracos / Último Jogo).")
            
            # 3. Sort Logic
            tee_order = {'Azur': 0, 'Branco': 1, 'Vermelho': 2}
            df_filtered['Tee_Rank'] = df_filtered['Tee'].map(tee_order)
            df_sorted = df_filtered.sort_values(by=['Tee_Rank', 'Gross'])
            print("[SYSTEM] Dados ordenados com sucesso.")
            
            return df_sorted
        except Exception as e:
            print(f"[ERROR] Falha ao processar dados: {e}")
            return None

    df = get_data()

    if df is not None and not df.empty:
        # Create Table
        results_table = ft.DataTable(
            heading_row_color=ft.Colors.BLUE_GREY_50,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            border_radius=10,
            columns=[
                ft.DataColumn(ft.Text("Jogador", weight="bold")),
                ft.DataColumn(ft.Text("Gross", weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Tee", weight="bold")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['Jogador'])),
                        ft.DataCell(ft.Text(str(int(row['Gross'])), weight="bold")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(row['Tee'], color=ft.Colors.WHITE, size=11),
                                bgcolor=ft.Colors.BLUE_700 if row['Tee'] == 'Azur' else ft.Colors.BLACK if row['Tee'] == 'Branco' else ft.Colors.RED_700,
                                padding=ft.padding.symmetric(vertical=4, horizontal=10),
                                border_radius=5,
                                # New valid alignment syntax
                                alignment=ft.Alignment(0, 0)
                            )
                        ),
                    ]
                ) for _, row in df.iterrows()
            ]
        )
        
        # Center the table container
        table_container = ft.Row(
            controls=[results_table],
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
    else:
        table_container = ft.Text("Nenhum dado encontrado.", color="red")
        print("[WARNING] A tabela resultou em zero linhas.")

    # Build Layout
    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                header,
                subheader,
                ft.Divider(height=20, thickness=1),
                table_container
            ]
        )
    )
    print("[SYSTEM] Interface renderizada. Aguardando interação...")

if __name__ == "__main__":
    ft.app(target=main)