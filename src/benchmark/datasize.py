from datasets import load_dataset, DatasetDict
from setfit import SetFitModel,SetFitTrainer
import numpy as np
import evaluate, sklearn, argparse

accuracy_metric = evaluate.load("accuracy")
recall_metric = evaluate.load("recall")
precision_metric = evaluate.load("precision")
f1_metric = evaluate.load("f1")
matthews_correlation_metric = evaluate.load("matthews_correlation")


def create_datasets(dataset_path, kfold_count=10):
  kfold_size=100//kfold_count
  datasets=[]
  for i in [0.25,0.50,0.75,1]:   
      train = load_dataset("csv", data_files=dataset_path, split=[f"train[:{k}%]+train[{k+kfold_size}%:]" for k in range(0, 100, kfold_size)], delimiter="|")
      validation = load_dataset("csv", data_files=dataset_path,  split=[f"train[{k}%:{k+kfold_size}%]" for k in range(0, 100, kfold_size)], delimiter="|")
      
      train_truncated=[]
      for dataset in train:
          train_truncated.append(dataset.select(range(int(len(dataset)*i))))
      
      datasets.append(DatasetDict({
          'train': train_truncated,
          'validation': validation}))
  return datasets




def compute_metrics(y_pred, y_test):
  metric_dict = {"confusion_matrix":[]}
  metric_dict["accuracy"] = accuracy_metric.compute(references=y_test, predictions=y_pred)["accuracy"]
  metric_dict["recall"] = recall_metric.compute(references=y_test, predictions=y_pred, average="macro")["recall"]
  metric_dict["precision"] = precision_metric.compute(references=y_test, predictions=y_pred,average="macro")["precision"]
  metric_dict["f1"] = f1_metric.compute(references=y_test, predictions=y_pred,average="macro")["f1"]
  metric_dict["matthews"] = matthews_correlation_metric.compute(references=y_test, predictions=y_pred,average="macro")["matthews_correlation"]
  try:
    metric_dict["confusion_matrix"] = sklearn.metrics.confusion_matrix(y_test, y_pred, labels=[0,1,2])
  except:
    pass
  return metric_dict

def getAverageMetrics(metricsList):
    avgMetrics={"accuracy":0,"recall":0,"precision":0,"f1":0,"matthews":0, "confusion_matrix":[]}
    for metricSet in metricsList:
      avgMetrics["accuracy"] += metricSet["accuracy"]
      avgMetrics["recall"] += metricSet["recall"]
      avgMetrics["precision"] += metricSet["precision"]
      avgMetrics["f1"] += metricSet["f1"]
      avgMetrics["matthews"] += metricSet["matthews"]
      avgMetrics["confusion_matrix"].append(metricSet["confusion_matrix"])

    avgMetrics["accuracy"] /= len(metricsList)
    avgMetrics["recall"] /= len(metricsList)
    avgMetrics["precision"] /= len(metricsList)
    avgMetrics["f1"] /= len(metricsList)
    avgMetrics["matthews"] /= len(metricsList)
    avgMetrics["confusion_matrix"] = np.mean(avgMetrics["confusion_matrix"], axis=0)
    
    return avgMetrics



def run_experiment(datasets,model_id,kfold_count=10):
  final_metrics_list=[]
  for dataset in datasets:
      metricsList = []
      for i in range(kfold_count):
        model = SetFitModel.from_pretrained(model_id, out_features=3,params={"head_params":{"solver":"liblinear"}})
        trainer = SetFitTrainer(
            model=model,
            train_dataset=dataset["train"][i],
            eval_dataset=dataset["validation"][i],
            num_iterations=20,
            batch_size=128,
            seed=25,
            num_epochs=3, 
            learning_rate=2e-6,
            warmup_proportion=0.1,
            column_mapping={"prompt": "text", "labels": "label"},
            use_amp=True
        )
        trainer.train()
        trainer.metric = compute_metrics
        metrics = trainer.evaluate()
        metricsList.append(metrics)
        #model.save_pretrained("path-to-folder")
        print(metrics)
      print("---------------------------------------------------------------------------------------------")
      avg_metrics=getAverageMetrics(metricsList)
      final_metrics_list.append(avg_metrics)
      print(avg_metrics)
      print("---------------------------------------------------------------------------------------------")

  print(final_metrics_list) 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_id", type=str)
    parser.add_argument("dataset_path", type=str)
    args = parser.parse_args()

    datasets = create_datasets(args.dataset_path)

    run_experiment(datasets, args.model_id)
    

if __name__ == "__main__":
    main()
