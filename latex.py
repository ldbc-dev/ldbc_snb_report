#This software is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This software is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math

class document:
    def begin_document(self, filename, title):
        self.file_object = open(filename,'w')
        self.file_object.write("\documentclass{article}\n")
        self.file_object.write("\\usepackage{fullpage}\n")
        self.file_object.write("\\usepackage{array}\n")
        self.file_object.write("\\usepackage{amssymb}\n")
        self.file_object.write("\\usepackage{amsmath}\n")
        self.file_object.write("\\usepackage{url}\n")
        self.file_object.write("\\usepackage{cite}\n")
        self.file_object.write("\\usepackage{rotating}\n")
        self.file_object.write("\\usepackage{enumitem}\n")
        self.file_object.write("\\usepackage{xfrac}\n")
        self.file_object.write("\\usepackage{multicol}\n")
        self.file_object.write("\\usepackage{booktabs}\n")
        self.file_object.write("\\usepackage{tabulary}\n")
        self.file_object.write("\\usepackage{float}\n")
        self.file_object.write("\\usepackage[utf8]{inputenc}\n")
        self.file_object.write("\\title{"+title+"}\n")
        self.file_object.write("\\begin{document}\n")
        self.file_object.write("\\maketitle\n")
        return
    
    def end_document(self):
        self.file_object.write("\end{document}")
        self.file_object.close()
        return
    
    def begin_minipage(self,num_figures_per_row):
        self.file_object.write("\\begin{minipage}{"+str(0.98/float(num_figures_per_row))+"\linewidth}\n")
        self.file_object.write("\\centering\n")
        return
    def end_minipage(self):
        self.file_object.write("\end{minipage}\n")
        return
    
    def begin_figure(self):
        self.file_object.write("\\begin{figure}[H]\n")
        return
    def end_figure(self):
        self.file_object.write("\end{figure}\n")
        return
    
    def include_graphics(self, image_file_name,rotate,size=0.7):
        if rotate:
            self.file_object.write("\includegraphics[width="+str(size)+"\linewidth,angle=-90]{"+image_file_name+"}\n")
        else: 
            self.file_object.write("\includegraphics[width="+str(size)+"\linewidth]{"+image_file_name+"}\n")
        return

    def insert_image_grid(self, filenames, num_images_per_row):
        num_figures = int(math.ceil(len(filenames) / num_images_per_row))
        for i in range(0,num_figures):
            self.begin_figure()
            for j in range(i*int(num_images_per_row),(i+1)*int(num_images_per_row)):
                if j < len(filenames):
                   self.begin_minipage(num_images_per_row)
                   self.include_graphics(filenames[j],False,1.0)
                   self.end_minipage()
            self.end_figure()



