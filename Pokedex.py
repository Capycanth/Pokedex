from Model import Addition, BallType, DatabaseEntry, PokedexEntry
from DataIO import DataIO

# We need enough ball slots to cover all possible Pokémon entries.
#
# Assumptions:
# - Each ball type can hold at least 100 Pokémon.
# - Each Pokémon can have at most 3 duplicate entries
#     → 100 capacity / 3 entries per Pokémon ≈ 33 Pokémon per ball type.
#
# - There are up to 1025 Pokémon, and on average have up to 2 forms (most have one, some have many, average to around two).
#     → Maximum possible entries = 1025 * 2 = 2050 total entries.
#
# - To store 2050 entries with ~33 Pokémon per ball:
#     → 2050 / 33 ≈ 63 ball "blocks" needed.
#
# - We currently support 6 ball types.
#     → 63 blocks / 6 ball types ≈ 11 repetitions of the ball list.
#
# Therefore, generate the ball type order by repeating the 6 ball types 11×.

_ball_type_order: list[BallType] = [BallType.POKE, BallType.GREAT, BallType.ULTRA, BallType.MASTER, BallType.LOVE, BallType.PARK] * 11

def run() -> None:
    print("Starting Pokedex Update Process...")
    pokedex: dict[int, list[PokedexEntry]] = DataIO.read_pokedex()
    additions: list[Addition] = DataIO.read_additions()
    database: list[DatabaseEntry] = DataIO.read_database()
    print("Loaded data...")

    success_log: list[str] = []
    error_log: list[str] = []

    for addition in additions:
        print(f"Processing addition: {addition.name} {addition.form}...")
        search_results: list[DatabaseEntry] = [entry for entry in database if addition.name in entry.name and _does_form_match(addition.form, entry.form)]
        if len(search_results) == 0:
            error_log.append(f"Unable to find {addition.name} {addition.form} in database.")
            continue
        elif len(search_results) > 1:
            error_log.append(f"Too many matches in database for {addition.name} {addition.form}.")
            continue

        db_entry: DatabaseEntry = search_results[0]

        if db_entry.number in pokedex:
            dex_entries: list[PokedexEntry] = pokedex[db_entry.number]
            dex_entry_matches: list[PokedexEntry] = [entry for entry in dex_entries if addition.name in entry.name and _does_form_match(addition.form, entry.form)]

            if len(dex_entry_matches) == 0:
                pokedex[db_entry.number].append(PokedexEntry(db_entry.number, db_entry.name, db_entry.form, BallType.NONE, 1, db_entry.gen, True))
                success_log.append(f"[NEW FORM ADDED] | {db_entry.name} {db_entry.form}")
            elif len(dex_entry_matches) == 1:
                match: PokedexEntry = dex_entry_matches[0]
                match.count += 1
                success_log.append(f"[DUPLICATE ADDED] | {db_entry.name} {db_entry.form} | Total Count: {match.count}")
            else:
                error_log.append(f"Multiple entries for the same pokemon form: {db_entry.name} {db_entry.form}")
        else:
            pokedex[db_entry.number] = [PokedexEntry(db_entry.number, db_entry.name, db_entry.form, BallType.NONE, 1, db_entry.gen, True)]
            success_log.append(f"[NEW POKEMON ADDED] | {db_entry.name} {db_entry.form}")

    success_log.append("\n [Insert Locations] \n")

    ball_type_index: int = 0
    ball_index: int = 1
    for number in sorted(pokedex.keys()):
        for entry in pokedex[number]:
            entry.ball = _ball_type_order[ball_type_index]
            if entry.added:
                success_log.append(f"Insert {entry.name} {entry.form} into {entry.ball.value}:{ball_index}")
            ball_index += entry.count
        if ball_index > 100:
            ball_type_index += 1
            ball_index = 1

    DataIO.write_pokedex(pokedex)
    DataIO.write_success_log(success_log)
    DataIO.write_error_log(error_log)

def _does_form_match(add_form: str | None, entry_form: str | None) -> bool:
    if add_form is None and entry_form is None:
        return True
    if add_form is None:
        return False
    if entry_form is None:
        return False
    return add_form in entry_form

run()