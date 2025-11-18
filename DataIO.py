from Model import Addition, BallType, DatabaseEntry, PokedexEntry
import pandas as pd
from pandas import DataFrame, Series
from collections import defaultdict

class DataIO:

    _pokedex_path: str = 'data/pokedex.xlsx'
    _additions_path: str = 'data/additions.xlsx'
    _success_path: str = 'log/success.txt'
    _error_path: str = 'log/error.txt'
    _database_path: str = 'database.xlsx'

    #################
    #region Additions
    #################
    @staticmethod
    def read_additions() -> list[Addition]:
        df: DataFrame = pd.read_excel(DataIO._additions_path, dtype={"Name": str, "Form": str})
        data: list[Addition] = []
        for _, row in df.iterrows():
            data.append(Addition(row["Name"], DataIO._get_form(row)))

        DataIO._clear_additions()
        return data

    @staticmethod
    def _clear_additions() -> None:
        df = pd.DataFrame()
        df.to_excel(DataIO._additions_path, index=False)
    #endregion

    ###############
    #region Pokedex
    ###############
    @staticmethod
    def read_pokedex() -> dict[int, list[PokedexEntry]]:
        df: DataFrame = pd.read_excel(DataIO._pokedex_path, dtype={"number": int, "name": str, "form": str, "ball": str, "count": int})
        data: defaultdict[int, list[PokedexEntry]] = defaultdict(list)

        for _, row in df.iterrows():
            entry: PokedexEntry = PokedexEntry(
                number=row["number"],
                name=row["name"],
                form=DataIO._get_form(row),
                ball=DataIO._get_ball(row),
                count=row["count"],
                gen=row["gen"]
            )

            data[entry.number].append(entry)

        return data

    @staticmethod
    def write_pokedex(data: dict[int, list[PokedexEntry]]) -> None:
        rows = []
        for number in sorted(data.keys()):
            for entry in data[number]:
                rows.append({
                    "number": entry.number,
                    "name": entry.name,
                    "form": entry.form or "",
                    "ball": entry.ball.value,
                    "count": entry.count
                })

        df = pd.DataFrame(rows)
        df.to_excel(DataIO._pokedex_path, index=False)
    #endregion

    ##############
    #region Update
    ##############
    @staticmethod
    def write_success_log(log: list[str]) -> None:
        DataIO._write_log(DataIO._success_path, log)

    @staticmethod
    def write_error_log(log: list[str]) -> None:
        DataIO._write_log(DataIO._error_path, log)

    @staticmethod
    def _write_log(path: str, log: list[str]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for line in log:
                f.write(line + "\n")
    #endregion

    ################
    #region Database
    ################
    @staticmethod
    def read_database() -> list[DatabaseEntry]:
        df: DataFrame = pd.read_excel(DataIO._database_path, dtype={"number": int, "name": str, "form": str})
        data: list[DatabaseEntry] = []

        for _, row in df.iterrows():
            data.append(DatabaseEntry(
                number=row["number"],
                name=row["name"],
                form=DataIO._get_form(row),
                gen=row["gen"]
            ))

        return data

    #######################
    #region Private Helpers
    #######################
    @staticmethod
    def _get_form(row: Series) -> str | None:
        form_value = row.get("form")
        if isinstance(form_value, str) and form_value.strip() == "":
            form_value = None
        return form_value

    @staticmethod
    def _get_ball(row: Series) -> BallType:
        return BallType(row["ball"])
    #endregion