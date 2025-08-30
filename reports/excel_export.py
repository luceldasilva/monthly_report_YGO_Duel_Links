if __name__ == "__main__":
    import os
    from queries_db.constants import data_path
    from reports import (
        kog_df, ExcelConstants, tournament_text, month_fact_table,
        year_fact_table, df_name
    )
    import win32com.client as win32


    file_path = data_path.joinpath(
        f"{tournament_text}_{month_fact_table}_{year_fact_table}.xlsx"
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    kog_df.to_excel(file_path, sheet_name='Resumen', index=False)

    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False
    
    wb = excel.Workbooks.Open(file_path)
    ws_datos = wb.Sheets("Resumen")
    ws_datos.Cells.EntireColumn.AutoFit()

    last_row = ws_datos.Cells(
        ws_datos.Rows.Count, 1
    ).End(ExcelConstants.xlUp).Row
    
    last_col = ws_datos.Cells(1, ws_datos.Columns.Count).End(
        ExcelConstants.xlToLeft
    ).Column
    
    kog_excel = f"'Resumen'!R1C1:R{last_row}C{last_col}"

    pivot_sheet_name = "Top_Decks"
    ws_pivot = wb.Sheets.Add()
    ws_pivot.Name = pivot_sheet_name

    decks_cache = wb.PivotCaches().Create(
        SourceType=ExcelConstants.xlDatabase,
        SourceData=kog_excel
    )

    decks_pivot = decks_cache.CreatePivotTable(
        TableDestination=ws_pivot.Range("A3"),
        TableName="Top_Decks_Mazos"
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
