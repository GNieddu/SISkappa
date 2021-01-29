

def lgm(x):
    return scipy.special.loggamma(x)
# calculate KL divergence between two discrete pmfs
def KLDIV(P,Q):
    totlength = len(P)+1
    kldiv_vec = np.zeros(totlength)
    j=0
    for i in P:
        if i!=0 and Q[j]!=0:
            kldiv_vec[j] = i * (np.log(i) - np.log(Q[j]))
        else:
            kldiv_vec[j] = 0
        j+=1
    return kldiv_vec.sum()

# Make pmf from observation data
def make_pmf(inf_dat):
    n_obs = inf_dat.shape[0] # total number of observations
    maxI = inf_dat.max() # largets I-value observed
    count_I = np.zeros(int(maxI)+1) # make count vector for 0-maxI
    pmf_I = np.zeros(int(maxI)+1) # make pmf vector for 0-maxI
    for i in range(int(maxI)+1):
        count_I[i] = (inf_dat==float(i)).sum()
        pmf_I[i] = count_I[i] / n_obs
    return pmf_I
# Make SISk pmf / pdf
def SISk_pmf(I,κ,Npop):
    def SISk_pdf_u(I,param):
        mu, beta, kappa, gam, N = param
        I = np.array(I)
        pi0 = 1 # will normalize below
        log_density = lgm(N+1) + lgm(N*kappa/beta + I) + I * np.log(beta / ((mu+gam+kappa)*N)) - lgm(N-I+1) - lgm(N*kappa/beta) - lgm(I+1)
#         print(log_density)
        return np.exp(log_density)

    param = np.array([5e-5, 0.5, κ, 1, Npop])

    def SISk_pdf_unnorm(I):
        return SISk_pdf_u(I,param)

#     AUC = quad(SISk_pdf_unnorm,0,np.inf)
    AUC = quad(SISk_pdf_unnorm,0,I.max()+10)
    pynot = AUC[0]
    def SISk_pdf(I):
        return SISk_pdf_unnorm(I) / pynot

    def SISk_pmf_u(I):
        maxI = max(I)+1
        AUC_I = np.zeros(int(maxI))
        for i in range(int(maxI)):
            AUC_I[i] = quad(SISk_pdf,i,i+1)[0]
        return AUC_I
    return SISk_pmf_u(I)

def plotPDF(I,κ,Npop):
    pmf_u = SISk_pmf(I,κ,Npop)
    plt.plot(pmf_u)

def genFlName(mdl_name, kappa_val, N_val):
    kappa = kappa_val
    ku = "%.3E" % kappa
    ku = ku.replace(".","p")
    ku = ku.replace("-","m")
    ku = ku.replace("+","")

    N = N_val
    Nu = "%.3E" % N
    Nu = Nu.replace(".","p")
    Nu = Nu.replace("-","m")
    Nu = Nu.replace("+","")

    flname = mdl_name + 'k_keq_' + ku + '_Neq_' +  Nu
    return flname
