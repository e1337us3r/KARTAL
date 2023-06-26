import csv, argparse, os, time

def appendCSV(data, filename="labeled.csv", write_headers=False):
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if write_headers:
            writer.writerow(['prompt', 'labels'])
        writer.writerows(data)

def readCSV(filename, start_row=0, label=None, order="asc"):
    data=[]
    if not os.path.isfile(filename):
        return data
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        i = 0
        tmp_storage=[]
        for line in reader:
            tmp_storage.append(line)
        
        iterator = tmp_storage if order == "asc" else reversed(tmp_storage)
        for line in iterator:
            if label == None or line[1] == label:
                if i < start_row:
                    i+=1
                else:
                    data.append(line)
        return data
    
def getLabeledLineCount(filename):
    return len(readCSV(filename))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("label", nargs="?", default=None)
    parser.add_argument("order", nargs="?",default='asc')
    args = parser.parse_args()
    labeledFilename = args.filename.replace(".csv",f"-labeled{args.label}-{args.order}.csv")

    start_row = getLabeledLineCount(labeledFilename)

    data = readCSV(args.filename, start_row, label=args.label, order=args.order)
    begin_time = time.time()
    label_count = 1
    for example in data:
        os.system("clear")
        readableExample = example[0].replace(";","\n")
        readableExample = readableExample.replace("Requests: [", "\n")
        avg_time_per_label = (time.time()-begin_time)/label_count

        print(readableExample)
        print(f"\nTotal labeled: {start_row+label_count-1}")
        print(f"\nAvg. time per label: {avg_time_per_label}")
        selection = input(f"""
        Select label (default={example[1]}):
        0) Not vulnerable
        1) CWE-639: Authorization Bypass Through User-Controlled
        2) CWE-209: Exposure of Sensitive Information
        3) CWE-840: Business Logic
        4) CWE-20: Improper Input Validation
        98) Mark for review
        99) Mark for deletion
        Label: 
        """)

        selection = example[1] if len(selection) == 0 else int(selection)
        example[1] = selection

        appendCSV([example],labeledFilename)
        label_count+=1


if __name__ == "__main__":
    main()
