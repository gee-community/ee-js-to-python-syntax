# Simple conversion of earthengine JavaScript to Python syntax.

import argparse
import glob
import os
import re

def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', dest='js_dir', type=str,
                        help='Path to the directory containing JavaScript files')
    parser.add_argument('-out', dest='out_dir', type=str,
                        help='Path to the directory for saving converted files, this will be created if not available')
    parser.add_argument('-fm','--add-front-matter', dest='add_front_matter', required=False, type=bool, help='Add standard earthengine Python front matter')
    parser.add_argument('-cm','--convert-map', dest='convert_map', required=False, type=bool, help='Convert JS Map. to Python syntax')
    args = parser.parse_args()

    # Set defaults
    if args.add_front_matter:
      add_front_matter = bool(args.add_front_matter)
    else:
      add_front_matter = bool(False)
    if args.convert_map:
      convert_map = bool(args.convert_map)
    else:
      convert_map = bool(False)

    # Set paths
    js_dir = args.js_dir
    out_dir = args.out_dir

    # Create output directory
    if not os.path.isdir(out_dir):
      os.makedirs(out_dir)

    # Get file list
    js_files = glob.glob(js_dir + "*.js")

    # Define regex patterns and replacements
    # see https://regexr.com/
    replacements = {r'\bvar\b\s':'', # remove var
                    r'\blet\b\s':'', # remove let
                    r'\bfunction\b\s':'def ', # function to def
                    r'(\w+) = def ':r'def \1', # format function to def
                    r'\)\s\{':r'):', # format { to :
                    r'^\}':'', # format }
                    r'\/\*\*':'\"\"\"\"', # format multi-line comments
                    r'\s\*\s':' ', # format multi-line comments
                    r'\s\*\/':'\"\"\"', # format multi-line comments
                    r'(\n^\s* {4})':r' \\\n  ', # format chaining of functions
                    r'//\s':r'# ', # format single-line comments
                    r'\b\.and\b':'.And', # captilise .and
                    r'\b\)\.and\b':').And', # captilise .and
                    r'\b\.or\b':'.Or', # captilise .or
                    #r'\b\);\b':')', # remove ;
                    #r'\b\];\b':']', # remove ;
                    #r'\b\};\b':'}' # remove ;
                    }

    # Replace text
    def replace_all(text, replacements):
        for i, j in replacements.items():
            text = re.sub(i, j, text, flags=re.M)
        return text

    # Add ee python front matter
    fm = "#!/usr/bin/env python\n\n# Import earthengine API\nimport ee\nimport ee.mapclient\n\n# Initialise\nee.Initialize()\n\n"
    def add_fm(text, fm):
        return fm + text

    # Convert Map.addlayer syntax
    # FIX ME!!
    def convert_map(text):
        i = r'^Map.addLayer\(.+'
        text = re.findall(i,py_code, flags=re.M)
        text = ''.join(text)
        print(text)
        image = re.findall(r'\((\w+)', text)
        bands = re.findall(r'bands:\s\[.+]', text)
        min = re.findall(r'min:\s\d,', text)
        max = re.findall(r'max:\s.+,', text)
        # return correctly formatted!

    # Convert Map.center syntax
    # FIX ME!!

    # Given a single js file convert it to python
    def js_to_python(js_file, out_dir=out_dir, replacements=replacements, add_front_matter=add_front_matter, convert_map=convert_map):
        # Open js file
        js = open(js_file, 'r')
        # Read js code
        js_code =  js.read()
        # Convert to python
        py_code = replace_all(js_code, replacements)
        # Add front matter
        if add_front_matter == True:
          py_code = add_fm(py_code, fm)
        #FIXME!!!
        #if convert_map == True:
        #  py_code = convert_map(py_code)
        # Open py file to write
        p = os.path.split(js_file)
        n = str.split(p[1],  ".js")
        jspy = open(os.path.join(out_dir, n[0]) + ".py", 'w')
        # Write py code
        jspy.write(py_code)
        print("Conversion written to ", jspy)

    # Convert all js files in directory
    [js_to_python(f) for f in js_files]

if __name__ == "__main__":
    main()
