import argparse, csv, random
def appendCSV(data, filename, write_headers=False):
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if write_headers:
            writer.writerow(['prompt', 'labels'])
        writer.writerows(data)

def getLabeledData(filename):
    data={}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for line in reader:
            data.setdefault(line[1],[]).append(line)
            
        return data
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outputfile")
    parser.add_argument("-c","--count")
    parser.add_argument("-k","--kfold_count",type=int, default=10)
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()
    data={}

    for file in args.filenames:
        for label,values in getLabeledData(file).items():
            data.setdefault(label,[]).extend(values)
    stratifiedData=[]

    for i in range(args.kfold_count):
        fold=[]
        for _,values in data.items():
            interval=int(len(values)*0.1)
            start=i*interval
            end=start+interval
            fold.extend(values[start:end])
        random.shuffle(fold)
        stratifiedData.extend(fold)

    fold = stratifiedData[:int(len(stratifiedData)*0.1)]
    temp={}
    for line in fold:
        temp.setdefault(line[1],[]).append(line)

    appendCSV(stratifiedData,args.outputfile)


if __name__ == "__main__":
    main()
