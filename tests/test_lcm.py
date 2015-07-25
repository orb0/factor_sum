import factor_sum

def test_lcm_1():
   assert factor_sum.lcm(9,6) == 18

def test_lcm_2():
   assert factor_sum.lcm(5,3) == 15

def test_lcm_3():
   assert factor_sum.lcm(121, 545) == 65945
