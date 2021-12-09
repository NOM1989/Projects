#==================#
# Quick Stats v1.2 - 8/12/21
# by Nicholas Michau
# -----------------
# Input summary statistics - PMCC & Linear Regression calculated
#==================#

def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def get_input(prompt):
    x = input(prompt)
    while not is_number(x):
        print('Not num - Try again')
        x = input(prompt)
    return float(x)

def inputs(Σx2=False,Σy2=False):
    n = get_input('n: ')
    Σx = get_input('Ex: ')
    Σy = get_input('Ey: ')
    if Σx2 == True:
        Σx2 = get_input('Ex2: ')
    if Σy2 == True:
        Σy2 = get_input('Ey2: ')
    Σxy = get_input('Exy: ')
    return n, Σx, Σy, Σx2, Σy2, Σxy

def PMCC():
    n, Σx, Σy, Σx2, Σy2, Σxy = inputs(Σx2=1,Σy2=1)
    print((Σxy-((Σx*Σy)/n))/(((Σx2-(Σx**2/n))*(Σy2-(Σy**2/n)))**.5))

def lin_reg_y_x():
    n, Σx, Σy, Σx2, Σy2, Σxy = inputs(Σx2=1)
    b = round((Σxy-((Σx*Σy)/n))/(Σx2-(Σx**2/n)), 4)
    c = round(b*(-(Σx/n)) + (Σy/n), 4)
    print('y=%.12gx%s%.12g' % (b, '+' if c > 0 else '-', abs(c)))

def lin_reg_x_y():
    n, Σx, Σy, Σx2, Σy2, Σxy = inputs(Σy2=1)
    b = round((Σxy-((Σx*Σy)/n))/(Σy2-(Σy**2/n)), 4)
    c = round(b*(-(Σy/n)) + (Σx/n), 4)
    print('x=%.12gy%s%.12g' % (b, '+' if c > 0 else '-', abs(c)))

func_dict = {
    1: PMCC,
    2: lin_reg_y_x,
    3: lin_reg_x_y
}
titles_dict = {
    1: 'PMCC',
    2: 'Lin reg y on x',
    3: 'Lin reg x on y',
    4: 'Exit'
}

x = 0
while x != 4:
    print('--Quick Stats Mode--\n' + '\n'.join(['%d. %s' % (i, titles_dict[i]) for i in titles_dict]))
    x = 0
    while x not in titles_dict:
        x = get_input('Selection: ')
    print('\n' + titles_dict[x])
    if x != 4:
        try:
            func_dict[x]()
            input('Enter to continue\n')
        except ZeroDivisionError:
            print('ERROR - Div Zero')
            input('Enter to try again\n')
print('Disclaimer: Values rounded not truncated (rounding errors occur)')