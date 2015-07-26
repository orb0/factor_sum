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

def test_compute_sum_with_min():
    s = factor_sum.Sum()
    s.maximum = 20
    s.minimum = 18
    s.add(3,5)
    assert s.compute_sum() == 38

def test_compute_sum_with_redunancy_1():
    s = factor_sum.Sum()
    s.maximum = 20
    s.add(3,5,6)

def test_compute_sum_with_redunancy_2():
    s = factor_sum.Sum()
    s.maximum = 20
    s.add(5,6,3)
    assert s.compute_sum() == 98
    assert s.compute_sum() == 98
