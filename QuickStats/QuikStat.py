#==================#
# Quick Stats v1.3 - 8/12/21
# by Nicholas Michau
# -----------------
# Input summary statistics - PMCC & Linear Regression calculated
#==================#
S='\n'
R='-'
Q='+'
P=abs
O=float
I=False
H=True
G=round
F=input
C=print
def J(x):
	try:O(x);return H
	except ValueError:return I
def A(prompt):
	B=prompt;A=F(B)
	while not J(A):C('Not num - Try again');A=F(B)
	return O(A)
def E(Σx2=I,Σy2=I):
	C=Σy2;B=Σx2;D=A('n: ');E=A('Ex: ');F=A('Ey: ')
	if B==H:B=A('Ex2: ')
	if C==H:C=A('Ey2: ')
	G=A('Exy: ');return D,E,F,B,C,G
def K():A,B,D,F,G,H=E(Σx2=1,Σy2=1);C((H-B*D/A)/((F-B**2/A)*(G-D**2/A))**0.5)
def L():A,B,D,I,K,J=E(Σx2=1);F=G((J-B*D/A)/(I-B**2/A),4);H=G(F*-(B/A)+D/A,4);C('y=%.12gx%s%.12g'%(F,Q if H>0 else R,P(H)))
def M():A,D,B,K,I,J=E(Σy2=1);F=G((J-D*B/A)/(I-B**2/A),4);H=G(F*-(B/A)+D/A,4);C('x=%.12gy%s%.12g'%(F,Q if H>0 else R,P(H)))
N={1:K,2:L,3:M}
D={1:'PMCC',2:'Lin reg y on x',3:'Lin reg x on y',4:'Exit'}
B=0
while B!=4:
	C('--Quick Stats Mode--\n'+S.join(['%d. %s'%(A,D[A])for A in range(1,len(D)+1)]));B=0
	while B not in D:B=A('Selection: ')
	C(S+D[B])
	if B!=4:
		try:N[B]();F('Enter to continue\n')
		except ZeroDivisionError:C('ERROR - Div Zero');F('Enter to try again\n')
C('Disclaimer: Values rounded not truncated (rounding errors occur)')