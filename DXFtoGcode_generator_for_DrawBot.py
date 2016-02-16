##This program imports .dxf file and extracts Line-elements from it. Further, it generates Gcode that is compatible to RepRap firmware.
import math
import Tkinter, tkFileDialog, dxfgrabber

__author__ = 'Aditya A. Wagh'

#Input appropriate geometric parameters (units in mm) for DrawBot below.

#It's assumed that main origin of the DrawBot is located at top-left pulley.
#First fix position of the arbitrary origin O' for the drawing paper and move gondola to that position.
#B is a horizontal distnce between two pulleys mounted on stepper motors at both ends.
#L1 is a distance between the left-pulley and the O' while, L2 is a distance between right-pulley and the O'.

B = 800
L1 = 1000
L2 = 1080

#Following function converts Cartesian coordinates of any point on the paper in to two relative belt lengths, L1corrected and L2corrected,
#corresponding to those at O'.

def cartesianTodrawbot(x, y, B, L1, L2):
    x0 = (B*B + L1*L1 - L2*L2)/(2*B)
    y0 = math.sqrt(L2*L2 - (B - x0)*(B - x0))
    L1new = math.sqrt((x + x0)*(x + x0) + (y +y0)*(y +y0))
    L2new = math.sqrt((B - (x + x0))*(B - (x + x0)) + (y +y0)*(y +y0))
    L1corrected = - (L1new - L1)
    L2corrected = - (L2new - L2)
    return L1corrected, L2corrected

#This opens a file dialog for choosing a .dxf file to import.

if __name__ == '__main__':
    
    root = Tkinter.Tk() 
    root.withdraw()
    file = tkFileDialog.askopenfilename(filetypes=[("DXF files","*.dxf")], title="Import DXF file",parent=root)
    dxf = dxfgrabber.readfile(file)
    all_lines = [entity for entity in dxf.entities if entity.dxftype == 'LINE']
    NoofLines = len(all_lines)

#Sets the origin and further magnitude of speed for the plotting in units mm/minute.
    
gcode = 'G1 ' + 'X 0.0000 ' + 'Y 0.0000 ' + 'Z 0.0000 F 3000 \n' + 'G1 ' + 'X 0.0000 ' + 'Y 0.0000 ' + 'Z 0.3000 \n'

for x in range(len(all_lines)):
    if x == 0:
        gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].start[0],all_lines[x].start[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].start[0],all_lines[x].start[1],B, L1, L2)[1]) + ' Z 0.3000 \n'
    else:
        if all_lines[x-1].end[0] == all_lines[x].start[0] and all_lines[x-1].end[1] == all_lines[x].start[1]:
            gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].start[0],all_lines[x].start[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].start[0],all_lines[x].start[1],B, L1, L2)[1]) + ' Z 0.0000 \n'
        else:
            gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].start[0],all_lines[x].start[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].start[0],all_lines[x].start[1],B, L1, L2)[1]) + ' Z 0.3000 \n'
            gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[1]) + ' Z ' + str(all_lines[x].end[2]) + '\n'            
    if x == NoofLines - 1:
        gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[1]) + ' Z 0.3000 \n'
    else:
        if all_lines[x+1].start[0] == all_lines[x].end[0] and all_lines[x+1].start[1] == all_lines[x].end[1]:
            gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[1]) + ' Z ' + str(all_lines[x].end[2]) + '\n'
        else:
            gcode = gcode + 'G1 ' + 'X ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[0]) + ' Y ' + str(cartesianTodrawbot(all_lines[x].end[0],all_lines[x].end[1],B, L1, L2)[1]) + ' Z 0.3000 \n'

gcode = gcode + 'G1 ' + 'X 0.0000 ' + 'Y 0.0000 ' + 'Z 0.3000 \n'

#It writes and saves a gcode file in the same folder where python script is stored.

gcode_file = open('output_gcode.gcode','w')
gcode_file.write(gcode)
gcode_file.close()


        
        
