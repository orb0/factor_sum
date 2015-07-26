import factor_sum

def test_main(capsys):
    factor_sum.main(('factor_sum','20','3','5'))
    out, err = capsys.readouterr()
    assert out == '98\n'

def test_compute_sum_with_min(capsys):
    factor_sum.main(('factor_sum','-m','18','20','3','5'))
    out, err = capsys.readouterr()
    assert out == '38\n'
