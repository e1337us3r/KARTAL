import os, csv, openai, time, argparse, ai21
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")
ai21.api_key = os.getenv("A21_API_KEY")
ai21.timeout_sec = 180

def getExamples(provider,prompt):
    systemPrompt = "Generate 10 examples based on the template, do not give explanations, label titles or example count, only provide the examples."
    if provider == "openai":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": systemPrompt,
                },
                {"role": "user", "content": prompt},
            ],
        )

        return completion.choices[0]["message"]["content"]
    elif provider == "ai21":
        systemPrompt = "Using the task explanation, template and examples, generate 10 more different examples that follow the format in the template.Dont replicate comments."
        completion = ai21.Completion.execute(
            model="j2-jumbo-instruct",
            prompt=f"{systemPrompt}\n{prompt}",
            numResults=1,
            maxTokens=8096,
            temperature=0.99,
            topKReturn=0,
            topP=1
        )
        return completion["completions"][0]["data"]["text"]

    else:
        raise Exception("Provider must be one of: ['openai', 'ai21']")


def getPrompt(promptFile):
    with open(promptFile) as f:
        return f.read()


def saveToFile(data, filename, write_headers=False):
    with open(filename, "a") as csvfile:
        writer = csv.writer(
            csvfile, delimiter="|", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        if write_headers:
            writer.writerow(["prompt", "labels"])
        writer.writerows(data)

def autogenerate(promptFile, iterationCount=1, provider="openai", filename="data-unknown.csv"):
    print("Reading the prompt...")
    prompt = getPrompt(promptFile)

    label = promptFile.split("_")[1]
    i = 0
    while i < iterationCount:
        try:
            print("Prompting the AI...")
            seconds = time.time()
            examples = getExamples(provider, prompt)
            print(f"Done, took {time.time()-seconds}s")

            print("Labeling the results...")
            content = examples
            contentSplit = content.split("\n")
            contentSplit = filter(lambda content: content not in ["", "Positive label examples:", "Negative label examples:", "Negative label example:", " -", "-","- ", " "], contentSplit)
            labeledExamples = [[example, label] for example in contentSplit]

            print("Saving to file...")
            saveToFile(labeledExamples,filename)
            print("Done.")
            i+=1
        except KeyboardInterrupt:
            exit(1)
        except:
            print("Request failed, trying again...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("promptFile")
    parser.add_argument("iterationCount")
    parser.add_argument("provider")
    parser.add_argument("filename")
    args = parser.parse_args()
    autogenerate(promptFile=args.promptFile,iterationCount=int(args.iterationCount),provider=args.provider,filename=args.filename)



if __name__ == "__main__":
    main()
