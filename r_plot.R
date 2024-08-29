#### Plot bubble

plot_bubble <- function(temp, x_axis, y_axis, bubble_size, c_title, c_subtitle, 
                        c_caption, c_x_axis, c_y_axis){
  p <- ggplot(data=temp, aes(x = x_axis, y = y_axis)) + 
    geom_point(aes(size=bubble_size, color=subject)) +
    # geom_text(aes(label=subject), size=4, position=position_jitter(width=1, height=2)) +
    geom_text_repel(aes(label=subject), min.segment.length=0, seed=42, box.padding = 0.75) +
    # geom_text(aes(label=subject), size=4, nudge_x=0.0, nudge_y=-0.15, position=position_jitter(width=,height=1))+
    
    geom_hline(yintercept=0) + geom_vline(xintercept=0) +
    theme_minimal() +
    
    theme(legend.position="bottom",
          plot.caption=element_text(hjust=0),
          plot.subtitle=element_text(face="italic"),
          plot.title=element_text(size=16, face="bold")) +
    
    labs(x=c_x_axis, y=c_y_axis,
         title=c_title,
         subtitle=c_subtitle,
         caption=c_caption) +
    
    theme(legend.position="none")+
    
    annotate(geom="text", x=max(abs(temp$x_axis))*1.15, y=max(abs(temp$y_axis))*1.25, label="Cooking", color="black",size=4, fontface="italic",hjust = 1)+
    annotate(geom="text", x=max(abs(temp$x_axis))*1.15, y=-max(abs(temp$y_axis))*1.25, label="Fading", color="black",size=4, fontface="italic",hjust = 1)+
    annotate(geom="text", x=-max(abs(temp$x_axis))*1.15, y=-max(abs(temp$y_axis))*1.25, label="In the drawer", color="black",size=4, fontface="italic",hjust = 0)+
    annotate(geom="text", x=-max(abs(temp$x_axis))*1.15, y=max(abs(temp$y_axis))*1.25, label="Up and coming", color="black",size=4, fontface="italic",hjust = 0)
}