
import sys
import matplotlib.pyplot as plt
import os
import latex
import argparse

from optparse import OptionParser
from subprocess import call

colors = ["blue", "red", "green", "yellow"]


def over_point( point, min_point, max_point ):
    other = point + (max_point - min_point)*0.1
    if point > (other - (max_point - min_point)/10) or other >= max_point:
        other = point - (max_point - min_point)*0.1
    return other

def draw_percentiles(plt, l, col):
    l = sorted(l)
    index = 0
    length = len(l)
    max_point = max(l)*0.9
    min_point = 0 
    min_point = min_point + (max_point - min_point)*0.1
    unit = len(l)/100.0
    while(index < length/4):
        index += 1
    if index < length:
        point = l[index]
        other = over_point(point, min_point, max_point)
        plt.plot([index, index], [point, other], color=col)
        plt.text(index-10*unit, other, "25th: "+str(l[index]))

    while(index < length/2):
        index += 1
    if index < length:
        point = l[index]
        other = over_point(point, min_point, max_point)
        plt.plot([index, index], [point, other], color=col)
        plt.text(index-10*unit, other, "50th: "+str(l[index]))

    while(index < length*0.75):
        index += 1
    if index < length:
        point = l[index]
        other = over_point(point, min_point, max_point)
        plt.plot([index, index], [point, other], color=col)
        plt.text(index-10*unit, other, "75th: "+str(l[index]))

    while(index < length*0.9):
        index += 1
    if index < length:
        point = l[index]
        other = over_point(point, min_point, max_point)
        plt.plot([index, index], [point, other], color=col)
        plt.text(index-10*unit, other, "90th: "+str(l[index]))

    while(index < length*0.99):
        index += 1

    if index < length:
        point = l[index]
        other = over_point(point, min_point, max_point)
        plt.plot([index, index], [point, other], color=col)
        plt.text(index, other, "99th: "+str(l[index]))

    


parser = OptionParser()
parser.add_option("-i", "--input", dest="input_filenames",
                          help="Input file name", action="append", metavar="FILE")
parser.add_option("-w", "--workspace_dir", dest="workspace_dir", default="./",
                          help="Workspace folder", metavar="FILE")

parser.add_option("-o", "--output", dest="output_filename", default="./",
                          help="Output file nme", metavar="FILE")


(options, args) = parser.parse_args()

if not options.output_filename:
    parser.error("Missing output file")

if not options.input_filenames:
    parser.error("Missing input files")


if (not options.input_filenames):
    parser.print_help()

queries = {}

current_slice = 1
for f in options.input_filenames:
    input_file = open(f, 'r')
    index = 0
    for line in input_file.readlines():
        if index != 0:
            line = line.split("|")
            query_type = line[0]
            if query_type not in queries:
                queries[query_type] = []
            if len(queries[query_type]) < current_slice:
                queries[query_type].append([])
            (queries[query_type])[current_slice-1].append(int(line[3]))
        index += 1
    input_file.close()
    current_slice += 1
    print("Number of parsed query instances in "+f+" "+str(index))

document = latex.document()
document.begin_document(options.output_filename+".tex", "LDBC SNB Interactive Execution Report")
for i in range(0, len(options.input_filenames)):
    total = 0
    times = []
    labs = []
    for key in queries:
        accum = 0
        l = (queries[key])[i]
        for q in l:
            accum += q
            total += q
        times.append(accum)
        labs.append(key)

    for j in range(0,len(times)):
        times[j] = times[j] / float(total) * 100.0

    plt.close()
    plt.title("Percentage of execution "+str(options.input_filenames[i]))
    plt.pie(times, autopct='%1.1f%%',labels=labs, colors=colors)
    filename = options.workspace_dir+"/pie_"+str(i)+".pdf"
    plt.savefig(filename)
    document.begin_figure()
    document.include_graphics(filename,False)
    document.end_figure()

    


image_filenames = []
for key in queries:
    print("Generating plot for query "+key)
    plt.close()
    plt.title(key)
    plt.ylabel('microseconds')
    min_point = 0
    max_point = 0
    index = 0
    for l in queries[key]:
        s = sorted(l)
        col = colors[index%len(colors)]
        if max(l) > max_point:
            max_point = max(l)
        plt.yscale('log')
        plt.plot(s, color=col)
        draw_percentiles(plt, s, col)
        index+=1

    plt.ylim(ymin=0, ymax=max_point)
    filename = options.workspace_dir+"/"+key+".pdf"
    plt.savefig(filename)
    image_filenames.append(filename)

image_filenames = sorted(image_filenames)

num_images_per_row = 2
document.insert_image_grid( image_filenames, num_images_per_row)
document.end_document()

call(["pdflatex", options.output_filename+".tex"])

