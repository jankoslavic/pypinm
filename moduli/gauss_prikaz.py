"""Vizualizacija algoritma Gaussove eliminacija"""

__author__ = "Domen Gorjup"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def gauss_visualize(A, b, LU=False, cmap='PRGn', float_precision=1, savepath='', fps=1):
    """
    Izračun in vizualizacija algoritma Gaussove eliminacije.
    
    :param A: matrika koeficientov  
    :param b: vektor desnih strani
    :param LU: če True, naredi LU razcep
    :param cmap: matplotlib cmap oznaka, default 'PRGn'
    :param f_precision: število decimalnih mest zapisa številskih vrednosti
    :param savepath: pot za sharanjevanje .git animacija
    :param fps: število sliic na sekundo matplotlib animacija
    :return: matplotlib animation
    """
    if LU:
        mat = A
    else:
        mat = np.column_stack((A, b))
        
    if isinstance(mat, np.ndarray) and len(mat.shape)==2 and mat.shape[1] >= mat.shape[0]:
        colors = np.zeros_like(mat).astype(float)
        mat = mat.astype(float)
    else:
        raise Exception('Neustrezni podatki')
        
    color_steps = []
    mat_steps = []
    color_steps.append(colors.copy())
    mat_steps.append(mat.copy())
    L = np.zeros_like(mat) # LU razcep

    for i in range(len(mat)-1):
        colors[i] -= 0.5
        colors[:, i] -= 0.35            
        for j in range(i+1, len(mat)):
            colors[j] += 1
            m = mat[j,i]/mat[i,i]
            mat[j, i:] -= mat[i, i:]*m
            if LU: 
                mat[j, i] = m

            # vrstice nad pivotno naj ne bodo obarvane
            for i_brez in range(i):
                colors[i_brez] = 0

            
            # posebej obarvani naj bodo vsi elementi, ki so bili zamenjani
            colors[np.nonzero(L)] = 0.4
            # v tem koraku naj zamenjan element še ne bo pobarvan, zato barve shranimo zgoraj
            L[j, i] = m 
            mat_steps.append(mat.copy())
            color_steps.append(colors.copy())
            colors[j] -= 1.
            colors[np.nonzero(L)] = 0.4 # to mora vedno veljati
            
        colors[i] += 0.5
        colors[:, i] += 0.35
        colors[np.nonzero(L)] = 0.5 # to mora vedno veljati
    
    # obarvan spdnji trikotnik
    trikot = np.zeros_like(color_steps[0])
    trikot[np.nonzero(L)] = 0.5
    color_steps.append(trikot)

    # pod diagonalo so elementi L
    if LU: 
        zadnji_korak = mat_steps[-1].copy()
        zadnji_korak[np.nonzero(L)] = L[np.nonzero(L)]
        mat_steps.append(zadnji_korak)
    else:
        mat_steps.append(mat_steps[-1])
    
    return visualize(color_steps, mat_steps, cmap, float_precision, savepath, fps, LU), mat_steps[-1]


def visualize(colors, values=None, cmap='PRGn',f_precision=1, savepath='', fps=1, LU=False):
    """
    Vizualizacija algoritma Gaussove eliminacije v matplotlibu.
    
    :param colors: koraki barv elementov matrike, vrednosti [-1, 1]
    :param values: koraki vrednosti v matrikah
    :param cmap: matplotlib cmap oznaka, default 'PRGn'
    :param f_precision: število decimalnih mest zapisa številskih vrednosti
    :param savepath: pot za sharanjevanje .git animacija
    :param fps: število sliic na sekundo matplotlib animacija
    :param LU: če True, naredi LU razcep
    :return: matplotlib animation
    """

    
    fig, ax = plt.subplots(1, 1)

    im = ax.imshow(colors[0], vmin=-1, vmax=1, cmap=cmap, animated=True)
    plt.axis('off')

    # tekst
    m_text = ax.text(-0.6, -0.8, 
                    '',
                    verticalalignment='center', 
                    horizontalalignment='center',
                    fontsize='x-large',
                    fontname='monospace'
                    )
    p_text = ax.text(-0.6, -1, 
                    '',
                    verticalalignment='center', 
                    horizontalalignment='right',
                    fontname='monospace',
                    fontsize='x-large'
                    )
    s_text = ax.text(-0.6, -0.6, 
                    '',
                    verticalalignment='bottom', 
                    horizontalalignment='center',
                    fontname='monospace',
                    fontsize='x-large'
                    )
    v_text = ax.text(-0.6, -1, 
                    '',
                    verticalalignment='center', 
                    horizontalalignment='right',
                    fontname='monospace',
                    fontsize='x-large'
                    )

    tekst_template = '{:.{:d}f}' 
    tekst = []
    for i in range(values[0].shape[0]):
        for j in range(values[0].shape[1]):
            tekst.append(ax.text(j, i, 
                                tekst_template.format(values[0][i, j], f_precision), 
                                verticalalignment='center', 
                                horizontalalignment='center',
                                fontname='monospace',
                                fontsize='large'))

    for yc in np.arange(-0.5, colors[0].shape[0], 1):
        ax.axhline(y=yc, c=(0.75, 0.75, 0.75), lw=2)
    for xc in np.arange(-0.5, colors[0].shape[1], 1):
        ax.axvline(x=xc, c=(0.75, 0.75, 0.75), lw=2)
    if not LU:
        ax.axvline(x=colors[0].shape[0]-0.5, ls='--', c='r', lw=3)

    zg_crta = ax.axhline(y=-0.5, lw=0.5, c='k')
    sp_crta = ax.axhline(y=0.5, lw=0.5, c='k')
    l_crta = ax.axvline(x=-0.5, lw=0.5, c='k')
    d_crta = ax.axvline(x=0.5, lw=0.5, c='k')

    def animate(i):
        im.set_data(colors[i])
        for t_index, t in enumerate(tekst):
            t.set_text(tekst_template.format(values[i-1].flatten()[t_index], f_precision))
        
        pivot = np.argmin(np.sum(colors[i], axis=1))
        vrsta = np.argmax(np.sum(colors[i], axis=1))
        zg_crta.set_ydata(np.array([pivot-0.5, pivot-0.5]))
        sp_crta.set_ydata(np.array([pivot+0.5, pivot+0.5]))
        l_crta.set_xdata(np.array([pivot-0.5, pivot-0.5]))
        d_crta.set_xdata(np.array([pivot+0.5, pivot+0.5]))
        
        if i == len(colors)-1:
            p_text.set_text('')
            s_text.set_text('')
            v_text.set_text('')
            m_text.set_text('')
            zg_crta.set_ydata(np.array([-1.5, -1.5]))
            sp_crta.set_ydata(np.array([-1.5, -1.5]))
            l_crta.set_xdata(np.array([-1.5, -1.5]))
            d_crta.set_xdata(np.array([-1.5, -1.5]))

        else:
            p_text.set_text('i = {}'.format(pivot))
            p_text.set_y(pivot)
            s_text.set_text('i = {}'.format(pivot))
            s_text.set_x(pivot)
            v_text.set_text('j = {}'.format(vrsta))
            v_text.set_y(vrsta)
            m_text.set_text('m = {:.2f}'.format(values[i-1][vrsta, pivot]/values[i-1][pivot, pivot]))
        return im, p_text, s_text, v_text, tekst, m_text, zg_crta, sp_crta, l_crta, d_crta

    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(colors)),
                            interval=1000/fps, blit=True)
    if savepath:
        writer = animation.PillowWriter(fps=fps, loop=0)
        ani.save(savepath, writer)
        
    return