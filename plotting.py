from video import df
from bokeh.plotting import figure,output_file,show

p=figure(x_axis_type="datetime",height=100,width=100,title="Motion_graph")
p.yaxis.minor_tick_line_color=None;
p.ygrid[0].ticker.desired_num_ticks=1
q=p.quad(left=df["Start"],right=df["End"],bottom=0,top=1,color="green")

output_file("graph.html")
show(p)
