from pathlib import Path


HTML = (Path(__file__).parents[1] / "static" / "index.html").read_text(
    encoding="utf-8"
)


def test_empty_cargo_list_never_falls_back_to_simulation_rows():
    assert (
        "if(cargoSource==='list'){\n"
        "    if(!Array.isArray(cargo.rows)||!cargo.rows.length)return [];"
    ) in HTML


def test_new_voyage_clears_runtime_restore_and_cargo_pool_state():
    assert "restoredSession=null;pendingConvertedCargo=null;" in HTML
    assert "cargoPoolSearch='';cargoPoolFilter='all';" in HTML
    assert "setCargoMode();build();renderCargoPool();" in HTML


def test_accepting_converted_cargo_refreshes_cargo_pool():
    acceptance = HTML.split("async function useConvertedCargo(){", 1)[1].split(
        "closeCargoConverter.onclick", 1
    )[0]
    assert "cargo.rows=data.coils||[]" in acceptance
    assert "build();renderCargoPool();" in acceptance
