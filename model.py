import numpy as np
def wrap(x):return (np.asarray(x)+np.pi)%(2*np.pi)-np.pi
def gate(x,k=2.):return np.exp(k*(np.cos(x)-1))
def complex_mean(psi,O,gamma,alpha,tau):return gate(psi-alpha-O*tau)*np.exp(-1j*(gamma+O*tau))
def gate_window(A,th,k=2.):
 if A<th:return None
 if th<=A*np.exp(-2*k):return np.pi
 return float(np.arccos(1+np.log(th/A)/k))
def sensitivity(r,C,h=1.,su=.7,sd=.7):return r*h*C/np.sqrt(r*r*su*su+sd*sd)
def ols(X,y):
 c=np.linalg.lstsq(X,y,rcond=None)[0];e=y-X@c;return c,(e@e/(len(y)-X.shape[1]))*np.linalg.inv(X.T@X)
def shifted(x,n):
 if n==0:return x.copy()
 y=np.zeros_like(x);y[n:]=x[:-n];return y
