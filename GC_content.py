import sys




def calculate_gc_content(DNA_string):
    counter = 0
    GC_content = 0
    for letter in DNA_string:
         if letter != '\n':
            counter = counter + 1
         if (letter == 'G') or (letter == 'C') and (letter != '\n'):
            GC_content = GC_content + 1
    return (GC_content * 1.0) / counter




def run_prog():
    with open(str(sys.argv[1])) as input_file:
        previous_ID = ""
        previous_string = ""
        max_GC_content = 0
        max_GC_ID = 0
        current_GC_sum = 0
        counter = 0
        current_string = ""
        for line in input_file:
            string_line = str(line)
            if string_line[0] == '>':
                if counter > 0:
                    current_GC_sum = calculate_gc_content(current_string)
                    print "final sum:", current_GC_sum
                counter = counter + 1
                if current_GC_sum > max_GC_content:
                    max_GC_content = current_GC_sum
                    max_GC_ID = previous_ID
                current_GC_sum = 0
                print current_string
                previous_ID = string_line
                current_string = ""
            
            else:
                print "string line", str(line)
                #current_GC_sum = calculate_gc_content(str(line)) + current_GC_sum
                current_string += str(line)
                #if new_GC > max_GC_content:
                 #   max_GC_content = new_GC
                  #  max_GC_ID = previous_ID
        print previous_ID
       
        
        current_GC_sum = calculate_gc_content(current_string)
        if current_GC_sum > max_GC_content:
            max_GC_content = current_GC_sum
            max_GC_ID = previous_ID  
        print "final sum:", current_GC_sum


        print "FINAL MAX VALUE:"
        print max_GC_ID
        print max_GC_content * 100.0



                
