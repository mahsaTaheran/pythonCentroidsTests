# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:46:32 2019

@author: mtaheran
"""

def plot_Centroids:
    
    fig=plt.figure(figsize=(14,9))
    ax1s=fig.add_subplot(211,title=Title)
    ax1=ax1s.twinx()
    ax2s=fig.add_subplot(212,sharex=ax1)
    ax2=ax2s.twinx()
    #fig3=plt.figure()
    #ax3s=fig3.add_subplot(111)
    #ax3=ax3s.twinx()
    
    figc=plt.figure(figsize=(14,6))
    axcs=figc.add_subplot(111,title=Title)
    axc=axcs.twinx()
    
    l1=[]
    l2=[]
    psdaxes=[ax1s,ax2s]
    cumaxes=[ax1,ax2]


    PSD=[(centroids.signal.welch(c[:,0],fs,nperseg=2**10),
          centroids.signal.welch(c[:,1],fs,nperseg=2**10),
          centroids.signal.welch(c[:,2],fs,nperseg=2**10))
         for c,(fs,*_) in zip(C,F)]
    RCS=[centroids.get_cumsum(c,fs,flip=reverse_cumsumfreq,fstart=cumsum_fstart)
         for c,(fs,*_) in zip(C,F)]

    for i,axi in enumerate(cumaxes):
        for (fr,rcs),fp in zip(RCS,fileprops):        
            l1.append(axi.plot(fr,rcs[:,i],
                                   **fp['props'],
                                   linewidth=2.5))
        axi.set_prop_cycle(None)
    for i,axi in enumerate(psdaxes):
        for psd3,fp in zip(PSD,fileprops):
            f,psd=psd3[i]
            l2.append(axi.plot(f,psd,
                                   **fp['props'],
                                   alpha=0.4))    
            f1,f2=sorted(plot_xlim)            
        axi.set_prop_cycle(None)

    for (ff,rcs),psd3,fp in zip(RCS,PSD,fileprops):        
        ffpsd,psdx=psd3[0]
        ffpsd,psdy=psd3[1]
        rcscombs=np.sqrt(rcs[:,0]**2+rcs[:,1]**2)
        psdcombs=np.sqrt(psdx**2+psdy**2)
        axc.plot(ff,rcscombs,
                   **fp['props'],
                   linewidth=2.5)                
        axcs.plot(ffpsd,psdcombs,
                   **fp['props'],
                   alpha=0.4)                
    axc.set_prop_cycle(None)
    

    if plot_xscale=='log':
        locxmaj=ticker.LogLocator(base=10.,subs=np.arange(1.,10,1))
        locxmin=ticker.LogLocator(base=10.,subs=np.arange(1.1,10,.1))
        for axi in psdaxes+[axcs]:
            axi.set_xscale('log')
            axi.xaxis.set_major_locator(locxmaj)
            axi.xaxis.set_minor_locator(locxmin)
            axi.xaxis.set_major_formatter(ticker.ScalarFormatter())
            axi.xaxis.set_minor_formatter(ticker.NullFormatter())
        
    for axi in psdaxes+[axcs]:
        axi.set_xlim(plot_xlim)
        axi.set_ylabel('PSD [arcsec²/Hz]')
        axi.set_yscale('log')
        axi.set_ylim(plot_psdylim)
        axi.grid(axis='x',which='major')
        axi.grid(axis='x',which='minor',alpha=0.3)    
    for axi in cumaxes+[axc]:    
        axi.set_yscale(plot_yscale)
        axi.grid(axis='y',which='major')
        axi.grid(axis='y',which='minor',alpha=0.3)        
        
    ax2s.set_xlabel("Frequency [Hz]")
    ax1.set_ylabel("Image Jitter XEL [arcsec rms]")
    ax2.set_ylabel("Image Jitter EL [arcsec rms]")
    #ax3.set_ylabel("HFD [arcsec rms]")   
    ax1.legend()
    
    axc.set_xlabel("Frequency [Hz]")
    axc.set_ylabel("Image Jitter XEL/EL combined [arcsec rms]")
    axc.legend()
    
    fig.tight_layout()
    figc.tight_layout()
    return (fig,figc)

if __name__=="__main__":    
    import argparse
    import json
    
    parser=argparse.ArgumentParser()
    parser.add_argument('propfile')
    parser.add_argument('-r','--reverse',
                        action='store_true',
                        default=False)
    parser.add_argument('-x','--plot_xscale',
                        choices=['log','linear'],
                        default='log')
    parser.add_argument('-y','--plot_yscale',
                        choices=['square','linear'],
                        default='square')
    parser.add_argument('-s','--save',
                        nargs='*')
    parser.add_argument('-d','--dir',
                        default='./')    
    args=parser.parse_args()
    with open(args.propfile,'r') as pfh:
        cfg=json.load(pfh)
    if args.plot_xscale=='linear':
        xlim=[0,210]
    else:
        xlim=[15,210]
    fig,figc=plot_jitter(cfg['fileprops'],cfg['title'],
                  reverse_cumsumfreq=args.reverse,
                  plot_xscale=args.plot_xscale,
                  plot_yscale=args.plot_yscale,
                  plot_xlim=xlim)
    rev=['fwd','rev']
    fn="{}/{}_{}_{}-{}".format(
            args.dir,cfg['prefix'],rev[args.reverse],args.plot_xscale,args.plot_yscale)
    if args.save:    
        for ext in args.save:
            fig.savefig('{}_axes.{}'.format(fn,ext))
            figc.savefig('{}_combined.{}'.format(fn,ext))   
        plt.close(fig)
        plt.close(figc)
    else:
        plt.draw()
        plt.show()

