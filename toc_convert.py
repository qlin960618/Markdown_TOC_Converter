import argparse
import os

PKG_NAME="TOCProcessor"

GENERATED_MARKING_START='[comment]: # (TOC generator marker start)'
GENERATED_MARKING_END='[comment]: # (TOC generator marker end)'


YES_RESPONSE_VAR = ['Y', 'YES']

HEADING_HEADER=[
'# ',
'## ',
'### ',
'#### ',
'##### ',
'###### ',
]
TOC_HEADING=[
'- ',
'  * ',
'     * ',
'        * ',
'           * ',
'             *',
]

ASCII_TO_REMOVE=[9]\
               +[i for i in range(33, 45)]\
               +[i for i in range(46, 48)]\
               +[i for i in range(58, 65)]\
               +[i for i in range(91, 95)]\
               +[i for i in range(96, 97)]\
               +[i for i in range(123, 127)]

CHR_TO_REMOVE = [chr(n) for n in ASCII_TO_REMOVE]

# # CHR_TO_REMOVE=''
# # for n in ASCII_TO_REMOVE:
# #     CHR_TO_REMOVE += chr(n)
# print(CHR_TO_REMOVE)
#
# oldstr="dslkjfhofew**23_-%%^&*sdklf"
# print(oldstr)
# newstr = ''.join((filter(lambda x: x not in CHR_TO_REMOVE, oldstr)))
# print(newstr)
#
# exit()

class TOCProcessor():
    def __init__(self, input_f_path, output_f_path):
        self.input_f_path = os.path.realpath(input_f_path)
        self.output_f_path = os.path.realpath(output_f_path)

        if not os.path.isfile(self.input_f_path) :
            raise ValueError("["+PKG_NAME+"]::Input is not a file: "+self.input_f_path)

        self.output_dir_path = os.path.dirname(self.output_f_path)

        if not os.path.isdir(self.output_dir_path):
            raise ValueError("["+PKG_NAME+"]::Output directory does not exist: "+self.output_dir_path)

    def read_file(self):
        self.file_data=[]
        # line_num=0
        with open(self.input_f_path, 'r') as in_f:
            line=in_f.readline()
            while line:
                self.file_data.append(line.strip())
                # line_num+=1
                line=in_f.readline()



    def get_toc_line_num(self, identifier_key, enforce_from_zero=False):

        for line_num, line in enumerate(self.file_data):
            index=line.find(identifier_key)
            if index>=0 and not enforce_from_zero:
                return line_num
            if index==0:
                return line_num

        raise RuntimeError("["+PKG_NAME+"]::Specified TOC Marking \""+identifier_key+"\" not found")


    def remove_line_range(self, toc_start_line, toc_end_line):
        self.file_data = self.file_data[:toc_start_line]+self.file_data[toc_end_line:]

        return toc_start_line, toc_start_line


    def generate_toc_table(self):
        #format
        # line_num, heading_level, disp_txt, heading_link, heading_link_dup
        #### heading_link_dup is link accoutn for duplicated header
        self.toc_table=[]

        for line_num, line in enumerate(self.file_data):
            for h_level, h_str in enumerate(HEADING_HEADER):
                if line.find(h_str) == 0:
                    ret = self.process_heading(line_num, h_level)
                    self.toc_table.append([line_num, h_level, *ret])
                    break


    def process_heading(self, line_num, h_level):
        # print("debug:: heading found at", line_num, h_level, self.file_data[line_num])
        line=self.file_data[line_num][len(HEADING_HEADER[h_level]):]

        line_no_l = self.remove_link(line)

        heading_link, heading_link_dup = self.process_string_to_link(line_no_l)
        disp_txt = self.process_string_to_disp_txt(line_no_l)
        # has line in format: [...](...)
        # if line


        return disp_txt, heading_link, heading_link_dup


    def remove_link(self, text):
        link_pattern=['[','](',')']
        mem=-1
        index=[]
        for i in range(3):
            ind = text.find(link_pattern[i])
            if ind<0:
                return text
            #make sure that the search index only increase
            if ind<mem:
                return text
            mem=ind
            index.append(ind)

        outtxt = text[:index[0]]+text[index[0]+1:index[1]]+text[index[2]+1:]
        ##give recurse processing incase there are multiple link in the line
        return self.remove_link(outtxt)



    def process_string_to_disp_txt(self, text):

        # While maybe additional processing is not needed

        return text



    def process_string_to_link(self, text):

        #remove all non alphbet
        link = ''.join((filter(lambda x: x not in CHR_TO_REMOVE, text)))

        #convert to lower case
        link = link.lower()

        #replace space with -
        link = link.replace(" ", '-')

        #replace all double -
        while link.find("--")>=0:
            link = link.replace("--", '-')

        #garantee uniqueness
        append_ind=0
        for ind, entry in enumerate(self.toc_table):
            if entry[3]==link:
                if append_ind:
                    self.toc_table[ind][4] = self.toc_table[ind][3]+"-%d"%(append_ind)
                append_ind+=1

        if append_ind==0:
            return link, link
        else:
            return link, link+"-%d"%(append_ind)


    def build_toc_data(self):
        self.toc_data=[]

        for entry in self.toc_table:
            self.toc_data.append(
                 TOC_HEADING[entry[1]]  \
                +'['                    \
                +entry[2]               \
                +'](#'                   \
                +entry[4]               \
                +')'                    \
            )

        # add marker to TOC data
        self.toc_data.insert(0, GENERATED_MARKING_START)
        self.toc_data.insert(0, '')
        self.toc_data.append('')
        self.toc_data.append(GENERATED_MARKING_END)




    def build_doc_data(self, toc_start_line, toc_end_line):
        self.data_to_write = \
                 self.file_data[:toc_start_line]    \
                +self.toc_data                      \
                +self.file_data[toc_end_line:]


    def write_to_file(self):

        print("Writing file to:", self.output_f_path)

        with open(self.output_f_path, 'w') as f_out:
            for line in self.data_to_write:
                f_out.write(line+"\n")

        print("Done!")




if __name__=='__main__':
    parser = argparse.ArgumentParser(description='This is a TOC processor for github')
    parser.add_argument('--input-file', metavar='path', type=str, required=True,
                help='Set the input file')
    parser.add_argument('--output-file', metavar='path', type=str, required=True,
                help='Set the output file')

    parser.add_argument('--location-identifier', metavar='string', type=str, required=False,
                default="[TOC]",
                help='Set the search string for TOC subsitution location')

    args = parser.parse_args()


    processor = TOCProcessor(args.input_file, args.output_file)

    #read file into memory
    processor.read_file()

    try:
        #find TOC marking
        toc_start_line = processor.get_toc_line_num(args.location_identifier)
        toc_end_line =  toc_start_line+1
    except RuntimeError as re:
        ## TOC marking not found, However, is might because this file has
        ## already been processed. Search for identifier key instead
        try:
            toc_start_line = processor.get_toc_line_num(GENERATED_MARKING_START,
                        enforce_from_zero=True)-1
            toc_end_line =  processor.get_toc_line_num(GENERATED_MARKING_END,
                        enforce_from_zero=True)+1
        except RuntimeError as re:
            #unable to locate any marking, Asking for user input
            print("Err: Unable to locate TOC marking")
            print("Do you want to force insert marking anyway? [Y/N]:", end="")
            response = input().upper()
            if not response in YES_RESPONSE_VAR:
                raise RuntimeError("["+PKG_NAME+"]::Processing terminated")

            print("Insert at line: ", end="")
            toc_end_line = toc_start_line = int(input())

    #removing existing TOC and get the new start, end line
    toc_start_line, toc_end_line = processor.remove_line_range(toc_start_line, toc_end_line)

    #generate a table of heading
    processor.generate_toc_table()

    #building TOC text
    processor.build_toc_data()

    #build document data by inserting TOC
    processor.build_doc_data(toc_start_line, toc_end_line)

    processor.write_to_file()


    # for var in processor.toc_data:
    #     # print("debug::: got", var, "::", processor.file_data[var[0]])
    #     print(" got", var)
    #     # pass

    #
    # print("will be inserted at line:", toc_start_line,"-->", toc_end_line)
    # print()
    # print()
    # print()
    # for num, line in enumerate(processor.data_to_write):
    #     print(num+1, line)
