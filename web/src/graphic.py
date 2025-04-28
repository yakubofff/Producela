import plotly
import numpy as np
import plotly.graph_objects as go
import plotly.offline as go_ofline



def create_terrain(mapa):
    x_list = []
    y_list = []
    z_list = []
    for x in range(len(mapa)):
      for y in range(len(mapa[0])):
        x_list.append(x)
        y_list.append(y)
        z_list.append(mapa[x][y])

    #DISTANCE FUNCTION
    def distance(x1,y1,x2,y2):
        d=np.sqrt((x1-x2)**2+(y1-y2)**2)
        return d

    #CREATING IDW FUNCTION
    def idw_npoint(xz,yz,n_point,p):
        r=10 #block radius iteration distance
        nf=0
        while nf<=n_point: #will stop when np reaching at least n_point
            x_block=[]
            y_block=[]
            z_block=[]
            r +=10 # add 10 unit each iteration
            xr_min=xz-r
            xr_max=xz+r
            yr_min=yz-r
            yr_max=yz+r
            for i in range(len(x_list)):
                # condition to test if a point is within the block
                if ((x_list[i]>=xr_min and x_list[i]<=xr_max) and (y_list[i]>=yr_min and y_list[i]<=yr_max)):
                    x_block.append(x_list[i])
                    y_block.append(y_list[i])
                    z_block.append(z_list[i])
            nf=len(x_block) #calculate number of point in the block

        #calculate weight based on distance and p value
        w_list=[]
        for j in range(len(x_block)):
            d=distance(xz,yz,x_block[j],y_block[j])
            if d>0:
                w=1/(d**p)
                w_list.append(w)
                z0=0
            else:
                w_list.append(0) #if meet this condition, it means d<=0, weight is set to 0

        #check if there is 0 in weight list
        w_check=0 in w_list
        if w_check==True:
            idx=w_list.index(0) # find index for weight=0
            z_idw=z_block[idx] # set the value to the current sample value
        else:
            wt=np.transpose(w_list)
            z_idw=np.dot(z_block,wt)/sum(w_list) # idw calculation using dot product
        return z_idw

    # POPULATE INTERPOLATION POINTS
    n=75 #number of interpolation point for x and y axis
    x_min=min(x_list)
    x_max=max(x_list)
    y_min=min(y_list)
    y_max=max(y_list)
    w=x_max-x_min #width
    h=y_max-y_min #length
    wn=w/n #x interval
    hn=h/n #y interval

    #list to store interpolation point and elevation
    y_init=y_min
    x_init=x_min
    x_idw_list=[]
    y_idw_list=[]
    z_head=[]
    for i in range(n):
        xz=x_init+wn*i
        yz=y_init+hn*i
        y_idw_list.append(yz)
        x_idw_list.append(xz)
        z_idw_list=[]
        for j in range(n):
            xz=x_init+wn*j
            z_idw=idw_npoint(xz,yz,5,1.5) #min. point=5, p=1.5
            z_idw_list.append(z_idw)
        z_head.append(z_idw_list)

    # CREATING 3D TERRAIN


    fig=go.Figure()
    colorscale = ['#0318f9','#0393f9', '#25d36d', '#25d36d', '#b5f08a', '#dad085', '#b7a39f', '#b7a39f']
    fig.add_trace(go.Surface(z=z_head,x=x_idw_list,y=y_idw_list,colorscale=colorscale))
    fig.update_layout(scene=dict(aspectratio=dict(x=2, y=2, z=0.5),xaxis = dict(range=[x_min,x_max],),yaxis = dict(range=[y_min,y_max])))
    str_of_html = plotly.io.to_html(fig)
    str_of_html = str_of_html[:52] + "<a href='/'>Back to settings</a>"+ str_of_html [52:]
    return str_of_html