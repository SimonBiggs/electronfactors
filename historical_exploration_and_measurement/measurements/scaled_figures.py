from matplotlib.pyplot import figure, subplots_adjust, axis, xlim, ylim, grid

def scaled_fig_start(w,l):
    figure(figsize=(w/2.54,l/2.54))
    subplots_adjust(left=0, right=1, top=1, bottom=0)
    
def scaled_fig_end(w,l):
    axis('equal')
    xlim([-w/2,w/2])
    ylim([-l/2,l/2])

    grid(True)
