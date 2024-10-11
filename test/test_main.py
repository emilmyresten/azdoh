from azdoh import main


def test_main():
    assert main()["steps"][0]["task"] == "Bash@3"
