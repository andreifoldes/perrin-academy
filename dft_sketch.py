""" Class for plotting a sketch of the forward / inverse Fourier transform

"""

from __future__ import division

import numpy as np

import matplotlib.pyplot as plt


def cosine_sine_basis(N):
    C = np.zeros((N, N))
    S = np.zeros((N, N))
    ns = np.arange(N)
    for k in range(N):
        t_k = k * 2* np.pi * ns / N
        C[k, :] = np.cos(t_k)
        S[k, :] = np.sin(t_k)
    return C, S


def img_rect(ax, x, y, width, height, border=0, color='k'):
    """ Plot rectangle image coordinates axes """
    lo_x, hi_x, lo_y, hi_y = (x - 0.5 - border,
                              x - 0.5 + width + border,
                              y - 0.5 - border,
                              y - 0.5 + height + border)
    ax.plot([lo_x, lo_x], [lo_y, hi_y], color)
    ax.plot([lo_x, hi_x], [lo_y, lo_y], color)
    ax.plot([hi_x, hi_x], [lo_y, hi_y], color)
    ax.plot([lo_x, hi_x], [hi_y, hi_y], color)


class DFTSketch(object):
    FONT_SIZE = 18
    AXES_PAD = 0.1
    IMAGE_PAD = 1
    TEXT_WIDTH = 3

    def __init__(self, x):
        # Vectors are always column vectors
        x = np.atleast_2d(x)
        if x.shape[0] == 1:
            x = x.T
        self.N = x.shape[0]
        self.x = x
        # DFT works over last dimension
        self.X = np.fft.fft(x.T).T
        # Some housekeeping filled in during sketch method
        self._axes = None
        self._fig = None

    def _get_ax_defs(self, inverse):
        N = self.N
        x = self.x
        if inverse:
            x = x.astype(np.complex)
        X = self.X
        pad = self.IMAGE_PAD * 2
        C, S = cosine_sine_basis(N)
        C = self.scale_array(C)
        S = self.scale_array(S)
        complex_x = np.iscomplexobj(x)
        if complex_x:
            x_real, x_imag = self.scale_complex_vector(x)
        else:
            x_real = self.scale_array(x)
        X_real, X_imag = self.scale_complex_vector(X)
        C_ax = dict(name='C',
                    title=r'$\mathbf{C}$',
                    content=C,
                    width= N + pad)
        S_ax = dict(name='S',
                    title=r'$\mathbf{S}$',
                    content=S,
                    width= N + pad)
        eq_ax = dict(content=r'$=$',
                     width = self.TEXT_WIDTH)
        plus_ax = dict(content=r'$+$',
                       width = self.TEXT_WIDTH)
        if inverse:
            inv_N_ax = dict(content=r'$\frac{1}{N}$',
                            width = self.TEXT_WIDTH)
            x_real_ax = dict(name='x_real_ax',
                             title='$x$',
                             content = x_real,
                             width = 1 + pad)
            x_imag_ax = dict(name='x_imag_ax',
                             content = x_imag,
                             width = 1 + pad)
            X_c_real_ax = dict(name='X_c_real_ax',
                               title='$X$',
                               content = X_real,
                               width = 1 + pad)
            X_c_imag_ax = dict(name='X_c_imag_ax',
                               content = X_imag,
                               width = 1 + pad)
            X_s_real_ax = dict(name='X_s_real_ax',
                               title='$X$',
                               content = X_real,
                               width = 1 + pad)
            X_s_imag_ax = dict(name='X_s_imag_ax',
                               content = X_imag,
                               width = 1 + pad)
            return [x_real_ax, x_imag_ax, eq_ax,
                    inv_N_ax, C_ax, X_c_real_ax, X_c_imag_ax, plus_ax,
                    inv_N_ax, S_ax, X_s_real_ax, X_s_imag_ax]
        X_real_ax = dict(name='X_real_ax',
                         title = '$X$',
                         content = X_real,
                         width = 1 + pad)
        X_imag_ax = dict(name='X_imag_ax',
                         content = X_imag,
                         width = 1 + pad)
        if complex_x:
            x_c_real_ax = dict(name='x_c_real_ax',
                               title = '$x$',
                               content = x_real,
                               width = 1 + pad)
            x_c_imag_ax = dict(name='x_c_imag_ax',
                               content = x_imag,
                               width = 1 + pad)
            x_s_real_ax = dict(name='x_s_real_ax',
                               title='$x$',
                               content = x_real,
                               width = 1 + pad)
            x_s_imag_ax = dict(name='x_s_imag_ax',
                               content = x_imag,
                               width = 1 + pad)
            return [X_real_ax, X_imag_ax, eq_ax,
                    C_ax, x_c_real_ax, x_c_imag_ax, plus_ax,
                    S_ax, x_s_real_ax, x_s_imag_ax]
        x_c_ax = dict(name='x_c_ax',
                      title=r'$x$',
                      content=x_real,
                      width = 1 + pad)
        x_s_ax = dict(name='x_s_ax',
                      title=r'$x$',
                      content=x_real,
                      width = 1 + pad)
        return [X_real_ax, X_imag_ax, eq_ax,
                C_ax, x_c_ax, plus_ax,
                S_ax, x_s_ax]

    def scale_complex_vector(self, x):
        """ Scale real and complex parts at the same time
        """
        N = x.shape[0]
        scaled = np.zeros((N, 2))
        scaled[:, 0] = x[:, 0].real
        scaled[:, 1] = x[:, 0].imag
        scaled = self.scale_array(scaled)
        return scaled[:, 0][:, None, :], scaled[:, 1][:, None, :]

    def scale_array(self, arr):
        """ Return RGB form of 2D array, centering scaling around 0
        """
        mn, mx = arr.min(), arr.max()
        vmax = max(np.abs(mn), np.abs(mx))
        if vmax != 0:
            arr = arr / (vmax * 2)
        return np.tile((arr + 0.5)[..., None], (1, 1, 3))

    def show_array(self, ax, arr, pad=IMAGE_PAD):
        M, N = arr.shape[:2]  # Allow for float scaled data
        ax.imshow(arr, cmap='gray', interpolation='nearest')
        ax.axis('off')
        img_rect(ax, 0, 0, N, M, color='k')
        # Expand axis by 1 unit in each direction
        x_lo, x_hi, y_hi, y_lo = ax.axis()
        ax.axis((x_lo - pad, x_hi + pad, y_hi + pad, y_lo - pad))
        ax.set_clip_on(False)

    def show_text(self, ax, string):
        """ Put text in center of axis
        """
        ax.axis('off')
        ax.text(0.5, 0.5, string,
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=self.FONT_SIZE,
                transform=ax.transAxes)

    def sketch(self, inverse=False, **fig_kw):
        # Draw sketch
        ax_defs = self._get_ax_defs(inverse)
        widths = [ax_def['width'] for ax_def in ax_defs]
        gridspec_kw = dict(width_ratios=widths)
        self.fig, axes = plt.subplots(1, len(ax_defs),
                                      sharey=True,
                                      gridspec_kw=gridspec_kw,
                                      **fig_kw)
        self._axes = {}
        for ax, ax_def in zip(axes, ax_defs):
            content = ax_def['content']
            if not hasattr(content, 'dtype'):  # must be str
                self.show_text(ax, content)
            else:
                self.show_array(ax, content)
            if 'title' in ax_def:
                ax.set_title(ax_def['title'])
            if 'name' in ax_def:
                self._axes[ax_def['name']] = ax