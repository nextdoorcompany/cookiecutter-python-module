import {{ cookiecutter.main_file }} as f


def test_main(capsys):
    f.main()
    assert capsys.readouterr().out == "hello world\n"
