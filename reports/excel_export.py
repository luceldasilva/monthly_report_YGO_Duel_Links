import os
import click
import pandas as pd
import xlsxwriter
from pathlib import Path
from queries_db.constants import data_path, comunity_dict, avatars, comunidades
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
        
        style_deck = workbook.add_format({
            'font_name': 'Aptos Narrow',
            'font_size': 16,
            'font_color': '0070C0',
            'bold': True
        })
        
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
            
            name_ranking_with_comunities = "mazos_por_comunidad"
            
            decks_with_comunities = workbook.add_worksheet(
                name_ranking_with_comunities
            )
            
            for i, (url_avatar, comunity_name, column) in enumerate(
                zip(avatars, comunity_dict.values(), comunidades), start=2
            ):
                col_idx = 5 + (i - 2)
                col_letter = xlsxwriter.utility.xl_col_to_name(col_idx - 1)
                ws_comunidad.write_string(
                    f'A{i}', f'IMAGEN("{url_avatar}";;2)'
                )
                ws_comunidad.write_string(f'B{i}', comunity_name)
                ws_comunidad.write_formula(
                    f'C{i}',
                    f'=COUNTIF({excel_file}!{col_letter}:{col_letter}, TRUE)'
                )
                ws_comunidad.write_formula(
                    f'D{i}',
                    f'=C{i}/{len(fact_df)}',
                    percent_format
                )
                
                decks_with_comunities.write_string(f'V{i}', comunity_name)
                decks_with_comunities.write_string(f'W{i}', column)
                decks_with_comunities.write_string(
                    f'X{i}', f'IMAGEN("{url_avatar}";;2)'
                )
            
            name_table_comunities: str = "columnas_comunidad"
            
            decks_with_comunities.add_table(
                first_row=0,
                first_col=21,
                last_row=len(comunity_dict),
                last_col=23,
                options={
                    "name": f"{name_table_comunities}",
                    "columns": [
                        {"header": "Comunidad"},
                        {"header": "columna"},
                        {"header": "avatar"}
                    ],
                    "style": "Table Style Medium 9"
                }
            )
            
            decks_with_comunities.hide_gridlines(2)
            
            column_lookup: str = "L2"
            
            name_comunities_lookup: str = "O2"
            
            avatar_comunities_lookup: str = "N2"
            
            decks_with_comunities.data_validation(
                name_comunities_lookup,
                {'validate': 'list', 'source': '=$V$2:$V$7'}
            )
            
            decks_with_comunities.write_formula(
                avatar_comunities_lookup, 
                f'=VLOOKUP({name_comunities_lookup},{name_table_comunities},3,0)'
            )
            
            decks_with_comunities.write_formula(
                column_lookup, 
                f'=VLOOKUP({name_comunities_lookup},{name_table_comunities},2,0)'
            )
            
            decks_count_comunities: str = f"""
            =CHOOSECOLS(
                FILTER(
                    {excel_file},
                    INDEX(
                        {excel_file}, ,
                        MATCH(
                            {column_lookup},
                            {excel_file}[#Headers], 0)) = TRUE
                    ), MATCH("deck", {excel_file}[#Headers], 0)
            )""".replace('\n', '').replace(' ', '')
            
            top_decks_comunities: str = f"""
            =FILTER(
                SORTBY(
                    UNIQUE({name_ranking_with_comunities}!A:A),
                    COUNTIF(
                        {name_ranking_with_comunities}!A:A,
                        UNIQUE({name_ranking_with_comunities}!A:A)),
                    -1
                ),
                SORTBY(
                    COUNTIF(
                        {name_ranking_with_comunities}!A:A,
                        UNIQUE({name_ranking_with_comunities}!A:A)),
                    COUNTIF(
                        {name_ranking_with_comunities}!A:A,
                        UNIQUE({name_ranking_with_comunities}!A:A)),
                    -1
                ) >= INDEX(
                    SORTBY(
                        COUNTIF(
                            {name_ranking_with_comunities}!A:A,
                            UNIQUE({name_ranking_with_comunities}!A:A)),
                        COUNTIF(
                            {name_ranking_with_comunities}!A:A,
                            UNIQUE({name_ranking_with_comunities}!A:A)),
                        -1
                    ),
                    5
                )
            )""".replace('\n', '').replace(' ', '')
            
            decks_count_cm: str = f'COUNTIF({name_ranking_with_comunities}!A:A, ANCHORARRAY(C2))'
            bars_decks_cm: str = f'REPT("█", {decks_count_cm})'
            percent_decks_cm: str = f'{decks_count_cm}/COUNTA({name_ranking_with_comunities}!A:A)'
            format_decks_cm: str = f'" (", TEXT({percent_decks_cm},"0%"), ")"'

            decks_with_comunities.write_formula(
                'A1', decks_count_comunities
            )
            decks_with_comunities.write_string(
                'B2', 'IMAGEN(BUSCARV(C2#;decks;2;0);;2)'
            )
            decks_with_comunities.write_formula(
                'C2', top_decks_comunities, style_deck
            )
            decks_with_comunities.write_formula(
                'D2',
                f'CONCATENATE({bars_decks_cm}, " " , {decks_count_cm}, {format_decks_cm})',
                style_deck
            )

            decks_with_comunities.write_formula(
                'M5', f'=COUNTA({name_ranking_with_comunities}!A:A)'
            )

            ws_comunidad.add_table(
                first_row=0,
                first_col=0,
                last_row=len(comunity_dict),
                last_col=3,
                options={
                    "name": "comunidad",
                    "columns": [
                        {"header": "avatar"},
                        {"header": "Comunidad"},
                        {"header": "Registros"},
                        {"header": "%"}
                    ],
                    "style": "Table Style Medium 9"
                }
            )

        decks = workbook.add_worksheet("mazos")

        top_decks: str = f"""
        =FILTER(
            SORTBY(
                UNIQUE({excel_file}[deck]),
                COUNTIF({excel_file}[deck], UNIQUE({excel_file}[deck])),
                -1
            ),
            SORTBY(
                COUNTIF({excel_file}[deck], UNIQUE({excel_file}[deck])),
                COUNTIF({excel_file}[deck], UNIQUE({excel_file}[deck])),
                -1
            ) >= INDEX(
                SORTBY(
                    COUNTIF({excel_file}[deck], UNIQUE({excel_file}[deck])),
                    COUNTIF({excel_file}[deck], UNIQUE({excel_file}[deck])),
                    -1
                ),
                5
            )
        )""".replace('\n', '').replace(' ', '')
        
        decks_count: str = f'COUNTIF({excel_file}[deck], ANCHORARRAY(B4))'
        bars_decks: str = f'REPT("█", {decks_count})'
        percent_decks: str = f'{decks_count}/COUNTA({excel_file}[deck])'
        format_decks: str = f'" (", TEXT({percent_decks},"0%"), ")"'

        decks.write_string('A4', 'IMAGEN(BUSCARV(B4#;decks;2;0);;2)')
        decks.write_formula('B4', top_decks, style_deck)
        decks.write_formula(
            'C4',
            f'=CONCATENATE({bars_decks}, " " , {decks_count}, {format_decks})',
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