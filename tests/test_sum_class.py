import factor_sum

def test_add_divisors():
    s = factor_sum.Sum()
    s.add(3,5)
    assert s.divisors == set((3,5))

def test_double_add_divisors():
    s = factor_sum.Sum()
    s.add(3,5)
    s.add(3,5,6)
    assert s.divisors == set((3,5,6))

def test_remove_divisors():
    s = factor_sum.Sum()
    s.add(3,5)
    s.remove(5)
    assert s.divisors == set((3,))

def test_clear_divisors():
    s = factor_sum.Sum()
    s.add(3,5)
    s.clear()
    assert s.divisors == set()

def test_compute_sum():
    s = factor_sum.Sum()
    s.maximum = 20
    s.add(3,5)
    assert s.compute_sum() == 98
