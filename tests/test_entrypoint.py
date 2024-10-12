import forth.main
import pytest
import io


def test_main_help() -> None:
    with pytest.raises(SystemExit) as exc_info:
        forth.main.main(['forth', '--help'])
    assert exc_info.value.code == 0


def test_main_1file(capfdbinary, tmp_path) -> None:  # type: ignore
    example = tmp_path / 'example.forth'
    assert not example.exists()

    example.write_text('21 2 * . CR')

    forth.main.main(['forth', str(example)])

    out, _ = capfdbinary.readouterr()
    assert out == b'42\n'


def test_main_stdin_as_input_file(monkeypatch, capfdbinary):  # type: ignore
    monkeypatch.setattr('sys.stdin', io.StringIO('21 2 * . CR'))

    forth.main.main(['forth', '-'])

    out, _ = capfdbinary.readouterr()
    assert out == b'42\n'


def test_main_halt(tmp_path, capfdbinary):  # type: ignore
    src1 = tmp_path / 'src1.forth'
    src1.write_bytes(b'1 1 + . CR HALT')
    src2 = tmp_path / 'src2.forth'
    src2.write_bytes(b'2 3 * . CR')

    forth.main.main(['forth', str(src1), str(src2)])

    out, _ = capfdbinary.readouterr()
    assert out == b'2\n'


def test_show_stats(monkeypatch, capfdbinary):  # type: ignore
    monkeypatch.setattr('sys.stdin', io.StringIO('21 2 * . CR'))

    forth.main.main(['forth', '-'])

    out, _ = capfdbinary.readouterr()
    assert b"# counters: {'tokens_processed':" not in out

    forth.main.main(['forth', '-', '--show-stats'])

    out, _ = capfdbinary.readouterr()
    assert b"# counters: {'tokens_processed':" in out
