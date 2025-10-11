import os
import click
import pandas as pd
import win32com.client as win32
from queries_db.constants import data_path
from queries_db import dataframe_queries as dfq
from reports.utils import fact_table_text, build_fact_df, ExcelConstants


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

    if tournament_text == 'KOG' and comunity is None:
        file_path = data_path / 'meses' / f'{excel_file}.xlsx'
    else:
        file_path = data_path.joinpath(f"{excel_file}.xlsx")

    if os.path.exists(file_path):
        os.remove(file_path)

    fact_df.to_excel(file_path, sheet_name=excel_file, index=False)

    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False
    
    wb = excel.Workbooks.Open(file_path)
    ws_datos = wb.Sheets(excel_file)
    ws_datos.Cells.EntireColumn.AutoFit()

    last_row = ws_datos.Cells(
        ws_datos.Rows.Count, 1
    ).End(ExcelConstants.xlUp).Row
    
    last_col = ws_datos.Cells(1, ws_datos.Columns.Count).End(
        ExcelConstants.xlToLeft
    ).Column
    
    df_excel = f"'{excel_file}'!R1C1:R{last_row}C{last_col}"

    pivot_sheet_name = "Mazos"
    ws_pivot = wb.Sheets.Add()
    ws_pivot.Name = pivot_sheet_name

    decks_cache = wb.PivotCaches().Create(
        SourceType=ExcelConstants.xlDatabase,
        SourceData=df_excel
    )

    decks_pivot = decks_cache.CreatePivotTable(
        TableDestination=ws_pivot.Range("A3"),
        TableName="Top_Decks"
    )

    decks_pivot.PivotFields("deck").Orientation = ExcelConstants.xlRowField

    decks_pivot.AddDataField(
        decks_pivot.PivotFields("nick"),
        "Total",
        ExcelConstants.xlCount
    )

    pct_decks = decks_pivot.AddDataField(
        decks_pivot.PivotFields("nick"),
        "% del Total",
        ExcelConstants.xlCount
    )
    pct_decks.Calculation = ExcelConstants.xlPercentOfTotal
    pct_decks.NumberFormat = "0%"
    
    decks_pivot.PivotFields("deck").AutoSort(
        ExcelConstants.xlDescending,
        "Total"
    )

    graph_top_decks = f"{pivot_sheet_name}!R4C1:R9C2"
    
    top_decks_cache = wb.PivotCaches().Create(
        SourceType=ExcelConstants.xlDatabase,
        SourceData=graph_top_decks,
        Version=7
    )

    top_decks_pivot = top_decks_cache.CreatePivotTable(
        TableDestination=ws_pivot.Range("F5"),
        TableName="Grafico_top_decks",
        DefaultVersion=7
    )

    top_decks_pivot.ColumnGrand = True
    top_decks_pivot.RowGrand = True
    top_decks_pivot.HasAutoFormat = True
    top_decks_pivot.DisplayErrorString = False
    top_decks_pivot.DisplayNullString = True
    top_decks_pivot.EnableDrilldown = True
    top_decks_pivot.MergeLabels = False
    top_decks_pivot.PreserveFormatting = True
    top_decks_pivot.RepeatAllLabels(1)
    top_decks_pivot.RowAxisLayout(2)
    top_decks_cache.RefreshOnFileOpen = False


    shape_obj = ws_pivot.Shapes.AddChart2(201, ExcelConstants.xlColumnClustered)
    chart = shape_obj.Chart
    chart.SetSourceData(top_decks_pivot.TableRange1)


    pf = chart.PivotLayout.PivotTable.PivotFields("Etiquetas de Fila")
    pf.Orientation = ExcelConstants.xlRowField
    pf.Position = 1

    chart.PivotLayout.PivotTable.AddDataField(
        chart.PivotLayout.PivotTable.PivotFields("Total"),
        "Suma de Total",
        ExcelConstants.xlSum
    )


    chart.ChartType = ExcelConstants.xlBarClustered

    chart.PivotLayout.PivotTable.PivotFields(
        "Etiquetas de fila"
    ).Caption = "Mazos"
    
    chart.PivotLayout.PivotTable.PivotFields(
        "Suma de Total"
    ).Caption = "Registros"

    chart.HasLegend = False
    chart.HasTitle = True
    chart.ChartTitle.Text = f"Top Decks {df_name}"
    shape_obj.Left = shape_obj.Left - 7.5
    shape_obj.Top = shape_obj.Top - 5.25

    pf.AutoSort(1, "Registros")


    wb.Save()
    wb.Close()
    excel.Quit()


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
    
    month_fact_table, year_fact_table = fact_table_text(fact_df)
    
    export_report(
        fact_df=fact_df,
        tournament_text=tournament_text,
        month_fact_table=month_fact_table,
        alias_fact_table=alias_fact_table,
        year_fact_table=year_fact_table
    )


if __name__ == "__main__":
    overall_report()