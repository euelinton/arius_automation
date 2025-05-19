
from pathlib import Path
import pandas as pd

class Load:
    def __init__(self) -> None: 
        pass

    def append_to_pdf(self, e, url, params, ocorrencia):
        params.update({ "ocorrencia": f"{ocorrencia}" })
        # Create a Path object
        file_path = Path(f"./pdfs/{params["ocorrencia"]} {params["dataproc_i"].replace("/", "-")} {params["dataproc_f"].replace("/", "-")}.pdf")

        # Check if the file exists
        if not file_path.exists():
            pdf = e.fetch_html_after_login(url=url, params=params)
            with open(file_path, "wb") as f:
                f.write(pdf)
        return file_path
    
    def append_to_excel(self, df):
        with pd.ExcelWriter("data.xlsx", engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="CANCELAMENTOS", index=False)