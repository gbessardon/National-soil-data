import numpy as np

def Coarsendata(dataclayt,datasandt,dataclayh,datasandh):
    #"data"-t data from teagasc i.e national database to be coarsed
    #"data"-h data from hswd or the reference database
    # This scripts assume that both spatial extent are the same 
    fa=dataclayt.shape[0]/dataclayh.shape[0]
    # 255 is a random value where the mask is applied
    dataclaytcoarse=255*np.ones(dataclayh.shape)
    datasandtcoarse=255*np.ones(datasandh.shape)
    for i in range(1,dataclayh.shape[0]):
        for j in range(1,dataclayh.shape[1]):
    #        if not np.ma.is_masked(dataclayh[i,j]): #mask the sea by using HWSD masks
                if not np.ma.is_masked(np.ma.mean(dataclayt[i*fa-fa:i*fa+fa,j*fa-fa:j*fa+fa])):
                    #np.ma.mean excludes masked values unlike np.mean
                    dataclaytcoarse[i,j]=np.ma.mean(dataclayt[i*fa-fa:i*fa+fa,j*fa-fa:j*fa+fa])
                    datasandtcoarse[i,j]=np.ma.mean(datasandt[i*fa-fa:i*fa+fa,j*fa-fa:j*fa+fa])

    dataclaytcoarse_m=np.ma.masked_where(dataclaytcoarse==255,dataclaytcoarse)
    datasandtcoarse_m=np.ma.masked_where(datasandtcoarse==255,datasandtcoarse)
    return(dataclaytcoarse_m,datasandtcoarse_m)

