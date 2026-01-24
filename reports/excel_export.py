import os
import click
import pandas as pd
import xlsxwriter
from openpyxl import load_workbook
from openpyxl.styles import Font
from pathlib import Path
from queries_db.constants import data_path, comunity_dict, avatars
from queries_db import dataframe_queries as dfq
from reports.utils import fact_table_text, build_fact_df


def export_report(
    fact_df: pd.DataFrame,
    tournament_text: str,
    alias_fact_table: str,
    year_fact_table: str,
    comunity: str | None = None
):
    """
    Generar un excel con los registros de la tabla de hechos
    y hacer una tabla dinámica de los mazos

    Parameters
    ----------
    fact_df : pandas.DataFrame
        Tabla de hechos a estudiar
    tournament_text : str
        Categoría si es KOG o copa KC
    alias_fact_table : str
        Alias del nombre de `fact_df`
    year_fact_table : str
        Año del `fact_df`
    comunity : str | None, optional
        Para separar por comunidad y ser un archivo aparte, por defecto es None
    """
    comunity_name: str = f"{comunity}_" if comunity else ''
    
    excel_name: str = f"{comunity_name}{tournament_text} {alias_fact_table} {year_fact_table}"
    
    excel_file: str = excel_name.replace(" ", "_").replace(".", "").lower()
    
    general: bool = tournament_text == 'KOG' and comunity is None
    
    decks_images = pd.read_json(
        'https://monthly-report-yugioh-dl.vercel.app/decks/',
        orient='records'
    )

    decks_images = decks_images[['name', 'url_image']]
    decks_images.rename(columns={'name': 'deck'}, inplace=True)

    if general:
        folder_path = data_path / f"{year_fact_table}"
        
        folder_path.mkdir(parents=True, exist_ok=True)
        
        file_path = folder_path.joinpath(f"{excel_file}.xlsx")
    else:
        file_path = data_path.joinpath(f"{excel_file}.xlsx")

    if os.path.exists(file_path):
        os.remove(file_path)

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        fact_df.to_excel(writer, sheet_name=excel_file, index=False)
        
        decks_images.to_excel(writer, sheet_name='decks', index=False)
        
        workbook: xlsxwriter.Workbook = writer.book
        
        excel_list: list = [
            (excel_file, fact_df), ('decks', decks_images)
        ]
        
        for sheet_name, df in excel_list:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            worksheet = writer.sheets[sheet_name]
            max_row, max_col = df.shape
            
            worksheet.add_table(
                first_row=0, first_col=0, last_row=max_row,
                last_col=max_col - 1, options={
                    "name": sheet_name.replace(" ", "_"),
                    "columns": [{"header": col} for col in df.columns],
                    "style": "Table Style Medium 9"
                }
            )
        
        if sheet_name == 'decks' and 'url_image' in df.columns:
            col_idx = df.columns.get_loc('url_image')
            for row in range(1, max_row + 1):
                cell_value = df.iloc[row-1, col_idx]
                worksheet.write(
                    row, col_idx, cell_value, 
                    workbook.add_format(
                        {'font_color': 'black', 'underline': 0}
                    )
                )
            
        if comunity is None:
            percent_format = workbook.add_format({'num_format': '0%'})
            
            ws_comunidad = workbook.add_worksheet("comunidad")
            
            for i, (url_avatar, comunity_name) in enumerate(
                zip(avatars, comunity_dict.values()), start=2
            ):
                col_idx = 5 + (i - 2)
                col_letter = xlsxwriter.utility.xl_col_to_name(col_idx - 1)
                ws_comunidad.write_string(f'A{i}', comunity_name)
                ws_comunidad.write_formula(
                    f'B{i}',
                    f'=COUNTIF({excel_file}!{col_letter}:{col_letter}, TRUE)'
                )
                ws_comunidad.write_formula(
                    f'C{i}',
                    f'=B{i}/{len(fact_df)}',
                    percent_format
                )
                ws_comunidad.write_string(f'F{i}', comunity_name)
                ws_comunidad.write_string(f'G{i}', url_avatar)

            ws_comunidad.add_table(
                first_row=0,
                first_col=0,
                last_row=len(comunity_dict),
                last_col=2,
                options={
                    "name": "comunidad",
                    "columns": [
                        {"header": "Comunidad"},
                        {"header": "Registros"},
                        {"header": "%"}
                    ],
                    "style": "Table Style Medium 9"
                }
            )

            ws_comunidad.add_table(
                first_row=0,
                first_col=5,
                last_row=len(comunity_dict),
                last_col=6,
                options={
                    "name": "avatares",
                    "columns": [
                        {"header": "comunidad"},
                        {"header": "avatar"},
                    ],
                    "style": "Table Style Medium 9"
                }
            )

        decks = workbook.add_worksheet("mazos")
        
        style_deck = workbook.add_format({
            'font_name': 'Aptos Narrow',
            'font_size': 16,
            'font_color': '0070C0',
            'bold': True
        })

        top_decks: str = """
        =FILTER(
            SORTBY(
                UNIQUE(kog_jan_2026[deck]),
                COUNTIF(kog_jan_2026[deck], UNIQUE(kog_jan_2026[deck])),
                -1
            ),
            SORTBY(
                COUNTIF(kog_jan_2026[deck], UNIQUE(kog_jan_2026[deck])),
                COUNTIF(kog_jan_2026[deck], UNIQUE(kog_jan_2026[deck])),
                -1
            ) >= INDEX(
                SORTBY(
                    COUNTIF(kog_jan_2026[deck], UNIQUE(kog_jan_2026[deck])),
                    COUNTIF(kog_jan_2026[deck], UNIQUE(kog_jan_2026[deck])),
                    -1
                ),
                5
            )
        )""".replace('\n', '').replace(' ', '')
        
        decks_count: str = 'COUNTIF(kog_jan_2026[deck], ANCHORARRAY(B4))'

        decks.write_formula('B4', top_decks, style_deck)
        decks.write_formula(
            'C4',
            f'=CONCATENATE(REPT("█", {decks_count}), " " , {decks_count})',
            style_deck
        )
        decks.hide_gridlines(2)


@click.command()
@click.option("--kc-cup", is_flag=True, help="Para usar en Copas KC")
def overall_report(kc_cup):
    """
    Generar el archivo excel para la tabla de hechos estudiada
    con todas sus comunidades

    Parameters
    ----------
    kc_cup
        Comando para saber si se quiere de la lista de la copa KC,
        si no se usa le refiere a `False` y se usa la lista de mes para KOG
    """
    fact_table, tournament_text, alias_fact_table = build_fact_df(kc_cup)
    
    fact_df = dfq.df_query(fact_table, alias_fact_table)
    
    _, _, year_fact_table = fact_table_text(fact_df)
    
    export_report(
        fact_df=fact_df,
        tournament_text=tournament_text,
        alias_fact_table=alias_fact_table,
        year_fact_table=year_fact_table
    )


if __name__ == "__main__":
    overall_report()