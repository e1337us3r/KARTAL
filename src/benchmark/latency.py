
import time, argparse
import pandas as pd
from datasets import load_dataset
from setfit import SetFitModel

N=10

def measure_performance(model, dataset, N=10, name="GPU"):
    time_list=[]

    for i in range(N):
        begin = time.perf_counter()
        model(dataset)
        time_passed=time.perf_counter() - begin
        time_list.append(time_passed)
        print(f"Pass #{i+1} took {round(time_passed,3)}s")
    
    time_series=pd.Series(time_list)

    print(f"---------------{name}-----------------")
    print(time_series.describe())
    print("-----------------------------------")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path",type=str)
    parser.add_argument("dataset_path",type=str)
    args = parser.parse_args()
    
    model = SetFitModel.from_pretrained(args.model_path, out_features=3)
    test_dataset = load_dataset("csv", data_files=args.dataset_path,  split=["train"], delimiter="|")[0]
    test_dataset_1k = test_dataset.select(range(1000))["prompt"]
        
    measure_performance(model, test_dataset_1k, name="GPU")

    model.to("cpu")

    measure_performance(model, test_dataset_1k, name="CPU")

if __name__ == "__main__":
    main()
