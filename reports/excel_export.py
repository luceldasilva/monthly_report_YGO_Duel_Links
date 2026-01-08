import os
import click
import pandas as pd
import xlsxwriter
from pathlib import Path
from queries_db.constants import data_path, comunity_dict
from queries_db import dataframe_queries as dfq
from reports.utils import fact_table_text, build_fact_df


def export_report(
    fact_df: pd.DataFrame,
    tournament_text: str,
    month_fact_table: str,
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
    month_fact_table : str
        Mes del `fact_df`
    alias_fact_table : str
        Alias del nombre de `fact_df`
    year_fact_table : str
        Año del `fact_df`
    comunity : str | None, optional
        Para separar por comunidad y ser un archivo aparte, por defecto es None
    """
    comunity_name: str = f"{comunity}_" if comunity else ''
    
    df_name: str = f"{tournament_text} {month_fact_table} {year_fact_table}"
    
    excel_name: str = f"{comunity_name}{tournament_text} {alias_fact_table} {year_fact_table}"
    
    excel_file: str = excel_name.replace(" ", "_").replace(".", "").lower()
    
    general: bool = tournament_text == 'KOG' and comunity is None

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

        workbook: xlsxwriter.Workbook = writer.book
        worksheet = writer.sheets[excel_file]

        max_row, max_col = fact_df.shape
        columns = [{"header": col} for col in fact_df.columns]
        
        worksheet.add_table(
            first_row=0, first_col=0, last_row=max_row, last_col=max_col - 1,
            options={
                "name": excel_file,
                "columns": columns,
                "style": "Table Style Medium 9"
            }
        )
        
        if comunity is None:
            percent_format = workbook.add_format({'num_format': '0%'})
            
            ws_comunidad = workbook.add_worksheet("comunidad")
            
            ws_comunidad.write_string('A1', 'comunidad')
            ws_comunidad.write_string('B1', 'Registros')
            ws_comunidad.write_string('C1', '%')
            
            for i, comunity_name in enumerate(
                list(comunity_dict.values()), start=2
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

            ws_comunidad.add_table(
                first_row=0,
                first_col=0,
                last_row=len(comunity_dict),
                last_col=2,
                options={
                    "name": "comunidad",
                    "columns": [
                        {"header": "comunidad"},
                        {"header": "Registros"},
                        {"header": "%"}
                    ],
                    "style": "Table Style Medium 9"
                }
            )



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
    
    _, month_fact_table, year_fact_table = fact_table_text(fact_df)
    
    export_report(
        fact_df=fact_df,
        tournament_text=tournament_text,
        month_fact_table=month_fact_table,
        alias_fact_table=alias_fact_table,
        year_fact_table=year_fact_table
    )


if __name__ == "__main__":
    overall_report()