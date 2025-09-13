if __name__ == "__main__":
    import os
    from queries_db.constants import comunidades, root_path, comunity_dict
    
    
    quarto_file = root_path / "notebooks" / "comunity_analysis.qmd"
    
    
    for comunity in comunidades:
        print(f"Generating report for {comunity_dict[comunity]}")
        os.system(
            f"quarto render {quarto_file} -P comunity:{comunity} --output {comunity}.html"
        )
