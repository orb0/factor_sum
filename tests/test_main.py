import factor_sum
import pytest

def test_main(capsys):
    factor_sum.main(('factor_sum','20','3','5'))
    out, err = capsys.readouterr()
    assert out == '98\n'

def test_main_with_min(capsys):
    factor_sum.main(('factor_sum','-m','18','20','3','5'))
    out, err = capsys.readouterr()
    assert out == '38\n'

def test_main_with_bad_min(capsys):
    with pytest.raises(SystemExit):
        factor_sum.main(('factor_sum','-m','20','18','3','5'))

def test_main_with_bad_max(capsys):
    with pytest.raises(SystemExit):
        factor_sum.main(('factor_sum','a','3','5'))

def test_main_with_bad_divisor(capsys):
    with pytest.raises(SystemExit):
        factor_sum.main(('factor_sum','20','a','5'))
