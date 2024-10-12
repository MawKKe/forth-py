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
